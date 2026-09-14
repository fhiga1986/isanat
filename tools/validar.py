#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador del sitio de ISANAT.  Uso:  python3 tools/validar.py

Se corre ANTES de cada push. Comprueba lo que un despliegue verde no comprueba:
HTML válido, schema que parsea, paridad entre las FAQ visibles y las del JSON-LD,
límites de title y description, enlaces internos que existen, y que la cabecera y
el pie no se hayan desincronizado entre páginas (el riesgo real de un sitio sin
generador: cuatro copias del mismo bloque que se van separando).

Sale con código 1 si algo falla, para poder engancharlo a un hook de git.
"""
import base64, hashlib, json, os, re, sys, unicodedata
from html import unescape

try:
    import html5lib
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Falta instalar: pip install html5lib beautifulsoup4")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://isanat.pe"
MAX_TITLE, MAX_DESC, MARCA_ANTES_DE = 60, 155, 40

errores, avisos = [], []

VERSION = None
_vf = os.path.join(RAIZ, "VERSION")
if os.path.exists(_vf):
    VERSION = open(_vf, encoding="utf-8").read().strip()

def error(pag, msg): errores.append(f"{pag}: {msg}")
def aviso(pag, msg): avisos.append(f"{pag}: {msg}")

def paginas():
    out = []
    for base, _, files in os.walk(RAIZ):
        if os.sep + ".git" in base:
            continue
        for f in files:
            if f.endswith(".html"):
                p = os.path.join(base, f)
                out.append((os.path.relpath(p, RAIZ).replace(os.sep, "/"), p))
    return sorted(out)

def norm(s):
    s = unicodedata.normalize("NFC", unescape(s or ""))
    return re.sub(r"\s+", " ", s).strip()

# --------------------------------------------------------------------------
chrome = {}
for rel, ruta in paginas():
    crudo = open(ruta, encoding="utf-8").read()

    # 1 · Parseo estricto
    try:
        html5lib.HTMLParser(strict=True).parse(crudo)
    except Exception as e:
        error(rel, f"HTML inválido — {str(e)[:160]}")
    s = BeautifulSoup(crudo, "html5lib")

    es404 = rel == "404.html"

    # 0 · Marcador de versión: tiene que estar en TODAS las páginas y coincidir
    #     con el archivo VERSION. Es lo que permite saber, con Ctrl+U en el sitio
    #     publicado, qué versión está realmente desplegada.
    mv = s.find("meta", attrs={"name": "version"}) if False else BeautifulSoup(crudo, "html5lib").find("meta", attrs={"name": "version"})
    if VERSION is None:
        aviso(rel, "no existe el archivo VERSION en la raíz del repo")
    elif not mv or not mv.get("content"):
        error(rel, "sin <meta name=\"version\">")
    elif mv["content"] != VERSION:
        error(rel, f"marcador de versión {mv['content']!r} no coincide con VERSION ({VERSION!r})")

    # 2 · Metadatos
    t = s.title.string if s.title else ""
    if not t:
        error(rel, "sin <title>")
    else:
        if len(t) > MAX_TITLE:
            error(rel, f"title de {len(t)} caracteres (máximo {MAX_TITLE}): {t!r}")
        i = t.find("ISANAT")
        if i < 0:
            error(rel, "el title no lleva la marca ISANAT")
        elif i + 1 > MARCA_ANTES_DE:
            error(rel, f"la marca aparece en el carácter {i+1}, debe estar antes del {MARCA_ANTES_DE}")

    d = s.find("meta", attrs={"name": "description"})
    if not es404:
        if not d or not d.get("content"):
            error(rel, "sin meta description")
        elif len(d["content"]) > MAX_DESC:
            error(rel, f"description de {len(d['content'])} caracteres (máximo {MAX_DESC})")

        # 3 · Canonical propio y con barra final
        c = s.find("link", rel="canonical")
        if not c or not c.get("href"):
            error(rel, "sin canonical")
        else:
            esperado = SITIO + "/" + (os.path.dirname(rel) + "/" if os.path.dirname(rel) else "")
            if c["href"] != esperado:
                error(rel, f"canonical {c['href']} — debería ser {esperado}")

    # 4 · Encabezados
    h1s = s.find_all("h1")
    if len(h1s) != 1:
        error(rel, f"{len(h1s)} etiquetas <h1> (debe haber exactamente 1)")
    niveles = [int(h.name[1]) for h in s.find_all(re.compile(r"^h[1-6]$"))]
    for a, b in zip(niveles, niveles[1:]):
        if b > a + 1:
            error(rel, f"salto de encabezado h{a} → h{b}")
            break

    # 5 · Imágenes
    for img in s.find_all("img"):
        falta = [a for a in ("alt", "width", "height") if not img.get(a)]
        if img.get("alt") == "":
            falta = [a for a in falta if a != "alt"]
        if falta:
            error(rel, f"<img src={img.get('src')}> sin {', '.join(falta)}")
        if not (img.get("loading") or img.get("fetchpriority")):
            aviso(rel, f"<img src={img.get('src')}> sin loading ni fetchpriority")

    # 6 · Marcadores sin resolver en el texto visible
    for tag in s(["script", "style"]):
        tag.extract()
    visible = norm(s.get_text(" "))
    for patron, que in ((r"\[[A-ZÁÉÍÓÚÑ_ ]{2,}\]", "marcador entre corchetes"),
                        (r"\bTODO\b", "TODO"),
                        (r"\bLorem ipsum\b", "Lorem ipsum")):
        m = re.search(patron, visible)
        if m:
            error(rel, f"{que} visible en la página: {m.group(0)!r}")

    # 7 · Enlaces
    origenes = {}
    for a in BeautifulSoup(crudo, "html5lib").find_all("a"):
        href = a.get("href", "")
        if href == "#":
            error(rel, "enlace muerto href=\"#\"")
        if href.startswith("http") and "isanat.pe" not in href:
            if "noopener" not in (a.get("rel") or []):
                error(rel, f"enlace externo sin rel=noopener: {href[:60]}")
        if href.startswith("/") and not href.startswith("//"):
            destino = href.split("#")[0].split("?")[0]
            if destino and destino != "/":
                fs = os.path.join(RAIZ, destino.lstrip("/"))
                if os.path.isdir(fs):
                    fs = os.path.join(fs, "index.html")
                if not os.path.exists(fs):
                    error(rel, f"enlace interno roto: {href}")
        if a.get("data-event"):
            clave = (a["data-event"], a.get("data-origen", ""))
            if not a.get("data-origen"):
                error(rel, f"data-event={a['data-event']} sin data-origen")
            elif clave in origenes:
                error(rel, f"data-origen repetido en la misma página: {clave}")
            origenes[clave] = 1
        if "wa.me" in href and not a.get("data-event"):
            error(rel, f"enlace de WhatsApp sin data-event: {href[:60]}")

    # 8 · JSON-LD y paridad de las FAQ
    s2 = BeautifulSoup(crudo, "html5lib")
    bloques = s2.find_all("script", attrs={"type": "application/ld+json"})
    if not es404 and not bloques:
        error(rel, "sin JSON-LD")
    if len(bloques) > 1:
        aviso(rel, f"{len(bloques)} bloques JSON-LD — es preferible un único @graph")
    for b in bloques:
        try:
            datos = json.loads(b.string)
        except Exception as e:
            error(rel, f"JSON-LD no parsea — {e}")
            continue
        nodos = datos.get("@graph", [datos])

        def vacios(o, ruta=""):
            if isinstance(o, dict):
                for k, v in o.items():
                    if v in ("", [], {}, None):
                        error(rel, f"campo vacío en el schema: {ruta}{k}")
                    vacios(v, f"{ruta}{k}.")
            elif isinstance(o, list):
                for x in o:
                    vacios(x, ruta)
        vacios(nodos)

        faqs = [n for n in nodos if n.get("@type") == "FAQPage"]
        if faqs:
            esquema = [(norm(q["name"]), norm(q["acceptedAnswer"]["text"]))
                       for q in faqs[0]["mainEntity"]]
            visibles = []
            for det in s2.select(".faq details"):
                visibles.append((norm(det.summary.get_text()),
                                 norm(det.select_one(".faq__a").get_text())))
            if esquema != visibles:
                error(rel, f"la FAQ del schema NO coincide con la visible "
                           f"({len(esquema)} en schema, {len(visibles)} visibles)")
                for i, (e, v) in enumerate(zip(esquema, visibles)):
                    if e != v:
                        error(rel, f"  FAQ #{i+1} difiere:\n    schema:  {e[0][:70]}\n    visible: {v[0][:70]}")

    # 9 · Cabecera y pie compartidos: que no se hayan desincronizado
    if not es404:
        nav = s2.find("nav", id="nav")
        pie = s2.find("footer", class_="ft")
        for nombre, nodo in (("nav", nav), ("footer", pie)):
            if not nodo:
                error(rel, f"falta el bloque compartido <{nombre}>")
                continue
            # se ignoran los aria-current, que sí cambian por página
            texto = re.sub(r'\s*aria-current="page"', "", str(nodo))
            chrome.setdefault(nombre, {}).setdefault(norm(texto), []).append(rel)

    # 10 · Assets compartidos
    if not es404:
        if not s2.find("link", href=re.compile(r"^/css/site\.v\d+\.css$")):
            error(rel, "no enlaza la hoja de estilos compartida /css/site.vN.css")
        if not s2.find("script", src=re.compile(r"^/js/site\.v\d+\.js$")):
            error(rel, "no carga el script compartido /js/site.vN.js")

# --------------------------------------------------------------------------
for nombre, variantes in chrome.items():
    if len(variantes) > 1:
        error("(varias)", f"el bloque <{nombre}> tiene {len(variantes)} versiones distintas: "
                          + " | ".join(", ".join(v) for v in variantes.values()))

# 12 · CSP: los hashes de _headers tienen que ser los de los scripts y estilos
#      en línea que hay HOY. Si no, el navegador los bloquea sin decir nada en la
#      página y el sitio se rompe en silencio (GA4 deja de medir, el menú deja de
#      abrirse) — es la clase de fallo que solo se ve abriendo la consola.
hdr = os.path.join(RAIZ, "_headers")
if os.path.exists(hdr):
    csp = ""
    for linea in open(hdr, encoding="utf-8"):
        if linea.strip().startswith("Content-Security-Policy:"):
            csp = linea.split(":", 1)[1].strip()
    if csp:
        reales = {"script": set(), "style": set()}
        for rel, ruta in paginas():
            s3 = BeautifulSoup(open(ruta, encoding="utf-8").read(), "html5lib")
            for sc in s3.find_all("script"):
                # Solo se excluyen los <script src> (los cubre 'self') y el JSON-LD,
                # que es DATO: el navegador nunca lo ejecuta.
                # ⚠ El bloque <script type="speculationrules"> SÍ necesita su hash.
                # En cuanto la CSP lleva un solo hash en script-src, la palabra
                # 'inline-speculation-rules' deja de aplicar y Chrome bloquea el
                # bloque. Excluirlo de aquí fue el fallo de la v1.3.0: el validador
                # daba verde y el navegador bloqueaba.
                if sc.get("src") or sc.get("type") == "application/ld+json":
                    continue
                reales["script"].add("'sha256-" + base64.b64encode(
                    hashlib.sha256((sc.string or "").encode()).digest()).decode() + "'")
            for st in s3.find_all("style"):
                reales["style"].add("'sha256-" + base64.b64encode(
                    hashlib.sha256((st.string or "").encode()).digest()).decode() + "'")
        for clase in ("script", "style"):
            declarados = set(re.findall(r"'sha256-[A-Za-z0-9+/=]+'",
                             (re.search(clase + r"-src ([^;]+)", csp) or
                              type("x", (), {"group": lambda s, n: ""})()).group(1)))
            for h in reales[clase] - declarados:
                error("_headers", f"la CSP no declara el hash de un <{clase}> en línea que sí existe: {h}")
            for h in declarados - reales[clase]:
                aviso("_headers", f"la CSP declara un hash de <{clase}> que ya no corresponde a ningún bloque: {h}")
        script_src = (re.search(r"script-src ([^;]+)", csp) or
                      type("x", (), {"group": lambda s, n: ""})()).group(1)
        if "'inline-speculation-rules'" in script_src and "'sha256-" in script_src:
            aviso("_headers", "script-src mezcla 'inline-speculation-rules' con hashes: "
                              "la palabra queda INERTE y el bloque speculationrules "
                              "necesita su propio hash")
        for atr in ("style-src", "script-src"):
            if "'unsafe-inline'" in (re.search(atr + r" ([^;]+)", csp) or
                                     type("x", (), {"group": lambda s, n: ""})()).group(1):
                aviso("_headers", f"{atr} usa 'unsafe-inline': se puede evitar con hashes")
        # ningún atributo style= en línea, que obligaría a abrir la política
        for rel, ruta in paginas():
            crudo2 = open(ruta, encoding="utf-8").read()
            for m in re.finditer(r'<[^>]+\sstyle="', crudo2):
                error(rel, "atributo style= en línea: la CSP no lo permite sin 'unsafe-inline'")
                break

# 11 · Sitemap
sm = os.path.join(RAIZ, "sitemap.xml")
if os.path.exists(sm):
    urls = re.findall(r"<loc>([^<]+)</loc>", open(sm, encoding="utf-8").read())
    indexables = set()
    for rel, ruta in paginas():
        if rel == "404.html":
            continue
        crudo = open(ruta, encoding="utf-8").read()
        if "noindex" in crudo:
            continue
        indexables.add(SITIO + "/" + (os.path.dirname(rel) + "/" if os.path.dirname(rel) else ""))
    for u in urls:
        if u not in indexables:
            error("sitemap.xml", f"{u} está en el sitemap y no existe como página indexable")
    for u in sorted(indexables - set(urls)):
        error("sitemap.xml", f"{u} es indexable y NO está en el sitemap")

# --------------------------------------------------------------------------
print(f"Páginas revisadas: {len(paginas())}" + (f"  ·  versión {VERSION}" if VERSION else ""))
for a in avisos:
    print("  aviso  ·", a)
if errores:
    print(f"\n{len(errores)} ERROR(ES):")
    for e in errores:
        print("  ✗", e)
    sys.exit(1)
print("\nTodo correcto.")
