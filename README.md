# ISANAT — Escuela de Natación · La Molina, Lima

Sitio web estático de ISANAT. Sin build, sin dependencias: son archivos HTML, CSS y
JS planos que se suben tal cual. Cinco páginas indexables.

**Versión actual: `1.3.0`** — ver [`CAMBIOS.md`](CAMBIOS.md).

Dominio de producción: **https://isanat.pe**

---

## Estructura

```
.
├── VERSION                                 Número de versión del sitio. Fuente de verdad
├── CAMBIOS.md                              Qué cambió en cada versión + hash del deploy
├── index.html                              Home · hub comercial
├── natacion-para-ninos-la-molina/
│   └── index.html                          Clases para niños
├── natacion-para-adultos-la-molina/
│   └── index.html                          Clases para adultos
├── natacion-para-bebes-la-molina/
│   └── index.html                          Aquabebé, 6 meses a 2 años
├── horarios-y-precios/
│   └── index.html                          Horarios y tarifas, en tablas HTML
├── en/
│   └── index.html                          TODA la oferta en inglés, en una sola página
├── pt/
│   └── index.html                          TODA la oferta en portugués, en una sola página
├── _redirects                              301 de la URL retirada en la v1.2.0
├── 404.html                                Error, la sirve Cloudflare sola. Autocontenida
├── css/
│   └── site.v3.css                         TODO el CSS del sitio (excepto el 404)
├── js/
│   └── site.v1.js                          TODO el JS del sitio
├── tools/
│   └── validar.py                          Validador. Correr antes de cada push
├── robots.txt                              Permite indexación + apunta al sitemap
├── sitemap.xml                             Las 7 URLs. Actualizar <lastmod> al cambiar contenido
├── site.webmanifest                        Metadatos de PWA / icono al "agregar a inicio"
├── _headers                                Cache de estáticos y headers de seguridad
├── favicon.ico
├── fonts/
│   ├── poppins-400.woff2                   Subsets latinos, 23 KB en total
│   ├── poppins-500.woff2
│   ├── poppins-700.woff2
│   └── LICENSE-Poppins.txt
└── img/
    ├── logo.webp                           Logo con fondo transparente (nav y pie)
    ├── logo.png                            Fallback PNG
    ├── logo-192.png                        Iconos del manifest
    ├── logo-512.png
    ├── favicon-32.png
    ├── apple-touch-icon.png
    └── og-image.jpg                        1200×630, la imagen que se ve al compartir
```

### Cómo se sabe qué versión está publicada

El número de versión vive en **tres sitios que tienen que coincidir**:

1. El archivo **`VERSION`** de la raíz.
2. El **`<meta name="version">`** de las siete páginas y el 404. Abre el sitio publicado,
   pulsa `Ctrl+U` y lo ves en las primeras líneas: **eso es lo que está en vivo de
   verdad**, no lo que creas recordar haber subido.
3. El **nombre del zip** de cada entrega.

`tools/validar.py` falla si los tres no dicen lo mismo. Después de cada push, anota
en `CAMBIOS.md` el hash que muestra Cloudflare en *Deployments*.

> ⚠️ **`css/site.v1.css` y `js/site.v1.js` se cachean UN AÑO** (`_headers`). Si cambias
> el contenido sin cambiar el nombre, quien ya visitó el sitio seguirá viendo la versión
> vieja durante meses. **Al modificarlos hay que renombrarlos a `.v2.`** y actualizar el
> `<link>` y el `<script>` de las cuatro páginas. El validador comprueba que ninguna
> página se quede atrás.

### Decisiones técnicas

- **Sin Tailwind CDN.** El CDN de Tailwind compila en el navegador (~400 KB de JS) y
  su propia documentación dice que no es para producción. El CSS está escrito a mano:
  ~20 KB sin comprimir, ~7 KB con gzip contando también el JS.
- **CSS y JS en archivos compartidos, no inline.** Con una sola página lo inline era
  más rápido; con cuatro significaría cuatro copias del mismo bloque desincronizándose
  a la primera corrección. Ahora hay un solo archivo de cada uno, cacheado un año: la
  primera página cuesta una petición más y las siguientes no cuestan nada.
- **Sin generador de sitios.** Para cuatro páginas, copiar la plantilla es más barato
  que mantener un build. El riesgo de copiar —que la cabecera y el pie se separen entre
  páginas— lo cubre `tools/validar.py`, que compara los bloques compartidos y falla si
  alguno difiere.
- **Fuentes self-hosted.** Poppins va en el repo como subsets woff2. No hay llamada a
  `fonts.googleapis.com`, así que se evitan dos conexiones externas en el render inicial.
- **Sin imagen en el hero.** El fondo es un degradado CSS con olas en SVG, no una foto.
  No hay archivo pesado que descargar y no se muestra una foto de stock que no es la
  piscina real. Cuando haya fotos reales, ahí sí conviene reemplazarlo.
- **Mapa bajo demanda.** El iframe de Google Maps solo se carga cuando el usuario hace
  clic en "Ver mapa". Evita ~700 KB de JS de terceros en la carga inicial.

---

## 1. Subir a GitHub

```bash
cd isanat
git init
git add .
git commit -m "ISANAT: landing inicial con SEO técnico y GA4"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/isanat.git
git push -u origin main
```

## 2. Desplegar en Cloudflare Pages (plan gratuito)

1. Crea la cuenta en [dash.cloudflare.com](https://dash.cloudflare.com).
2. **Compute (Workers & Pages) → Create → Pages → Connect to Git** y autoriza GitHub.
3. Elige el repositorio `isanat`.
4. Configuración del build:
   - Framework preset: **None**
   - Build command: *(vacío)*
   - Build output directory: `/`
   - Root directory: *(vacío)*
5. **Save and Deploy**. En menos de un minuto tienes una URL `isanat.pages.dev`.

Desde ahí, cada `git push` a `main` publica automáticamente. Cada rama distinta genera
su propia URL de preview sin tocar producción.

> **Por qué Cloudflare y no Vercel:** el plan Hobby de Vercel prohíbe el uso comercial,
> y define como comercial cualquier sitio que "publicite la venta de un producto o
> servicio" o por cuyo desarrollo alguien reciba pago. Este sitio cumple las dos. El
> plan Free de Cloudflare no tiene esa restricción.

## 3. Conectar el dominio isanat.pe

Para un dominio apex (sin `www`), Cloudflare exige que el dominio use **sus
nameservers**. No alcanza con crear un registro apuntando desde NIC.pe. El proceso:

**Paso 1 — Agregar el dominio a Cloudflare.** En el dashboard: *Add a domain* →
`isanat.pe` → plan **Free**. Cloudflare escanea los DNS actuales y te entrega dos
nameservers, con la forma `xxxx.ns.cloudflare.com`.

**Paso 2 — Cambiar los nameservers en NIC.pe.** Entra a tu panel de NIC.pe →
*Administrar dominio* → *Servidores DNS* (o *Delegación*), borra los que estén y
carga los dos de Cloudflare. Esto delega todo el DNS del dominio a Cloudflare: a
partir de ahí, cualquier registro futuro (correo, subdominios) se administra desde
el panel de Cloudflare, no desde NIC.pe.

**Paso 3 — Vincular el dominio al proyecto.** Cuando Cloudflare confirme que los
nameservers ya apuntan a ellos (te llega un correo), ve a tu proyecto de Pages →
*Custom domains* → *Set up a domain* → `isanat.pe`. Cloudflare crea el registro
CNAME y emite el certificado SSL solo. Repite con `www.isanat.pe`.

**Paso 4 — Redirect de www al dominio principal.** Esto en Cloudflare **no** va en
un archivo del repo: el `_redirects` de Pages no sabe distinguir hostnames. Se
configura en el dashboard, en *Rules → Redirect Rules → Create rule*:

| Campo | Valor |
|---|---|
| Nombre | `www a apex` |
| Si... | *Hostname* · *equals* · `www.isanat.pe` |
| Entonces | *Dynamic* · `concat("https://isanat.pe", http.request.uri.path)` |
| Código | **301** (Permanent Redirect) |
| Preserve query string | activado |

La propagación de nameservers en `.pe` suele tardar entre 2 y 24 horas. Hasta que
termine, el sitio sigue accesible por la URL `isanat.pages.dev`.

---

## 4. Checklist post-deploy

Orden exacto, cada paso depende del anterior.

### Día 0 — al publicar

- [ ] Abrir el sitio en móvil y desktop y probar **todos** los botones de WhatsApp.
- [ ] **Correr `python3 tools/validar.py`** (esto va ANTES del push, en realidad).
- [ ] Validar el HTML en [validator.w3.org](https://validator.w3.org/).
- [ ] Validar los schemas en [search.google.com/test/rich-results](https://search.google.com/test/rich-results).
- [ ] Medir en [PageSpeed Insights](https://pagespeed.web.dev/) — objetivo: >80 en móvil.
      **Las cuatro páginas**, no solo la home. Guardar el resultado como línea base.

### Día 0 — GA4 (`G-2J8YN9N4J3`)

El código ya está instalado y dispara `whatsapp_click` con el parámetro `origen`.
Falta la configuración del lado de GA4, que **no** se hace desde el código:

- [ ] **Marcar `whatsapp_click` como evento clave.** `Administrar → Eventos → Eventos
      recientes → estrella ☆`. Sin esto GA4 registra el evento pero no lo cuenta como
      conversión, y todos los informes de atribución quedan vacíos. Solo cuenta desde
      el día que se activa: no recalcula histórico.
- [ ] **Crear la dimensión personalizada `origen`.** `Administrar → Definiciones
      personalizadas → Crear`. Nombre: `Origen Conversión`, ámbito: `Evento`,
      parámetro: `origen`. Tarda 24-48 h en poblarse.
- [ ] **Zona horaria** de la propiedad en `(GMT-05:00) Lima`.

**Eventos que dispara el sitio** (todos con el parámetro `origen`; GA4 registra la URL
por separado, así que `origen` dice *qué parte de la página*, no *qué página*):

| Evento | Dónde | ¿Conversión? |
|---|---|---|
| `whatsapp_click` | los 7 CTA de cada página | **Sí** — márcalo como evento clave |
| `tel_click` | teléfono del pie y de Ubicación | **Sí** — márcalo también |
| `como_llegar_click` | enlace a Google Maps | No |
| `waze_click` | enlace a Waze | No |
| `maps_click` | botón "Ver mapa" de la home | No |
| `ver_programa_click` | tarjetas de la home y enlaces cruzados | No |
| `ver_programas_click` | botón secundario del hero | No |
| `faq_open` | al abrir una pregunta; manda `pregunta` | No |

`faq_open` es investigación de contenido gratis: dice qué duda tiene la gente antes de
escribir. Si una pregunta se abre mucho, esa respuesta merece su propia sección.

Valores de `origen`: `header`, `menu_movil`, `hero`, `cierre`, `cta_bar`, `flotante`,
`footer`, `ubicacion`, `como_empezar`, `tarjeta_ninos`, `tarjeta_adultos`,
`tarjeta_membresia`, `crosslink_ninos`, `crosslink_adultos`, `crosslink_nado_libre`,
`error_404`.

### Día 1

- [ ] Verificar en **GA4 → Tiempo real** que los clics a WhatsApp aparecen.
- [ ] Verificar el sitio en **Search Console** y enviar `https://isanat.pe/sitemap.xml`.
- [ ] *Inspeccionar URL → Solicitar indexación* para **cada una de las 4 URLs**.

### Semana 1-4 — Google Business Profile

Para un negocio local esto pesa más que cualquier optimización de código.

- [ ] Crear y **verificar por video** el perfil en [business.google.com](https://business.google.com).
- [ ] NAP idéntico carácter por carácter al del sitio y del schema:
      `ISANAT Escuela de Natación` / `Calle Hurón 409, Urb. Rinconada del Lago, La Molina, Lima, Perú` / `+51 915 236 322`
- [ ] Cargar 5+ fotos, descripción, horarios y los tres programas.
- [ ] Meta: **10 reseñas de 5 estrellas en 30 días**, pedidas por WhatsApp a clientes recientes.
- [ ] Copiar las coordenadas reales del perfil verificado y reemplazarlas en el sitio
      (ver el primer TODO de abajo).

> ⚠️ **Ojo con esto:** en esa misma dirección (Colegio Villa Caritas, Calle Hurón 409)
> ya opera y rankea otra academia de natación, Aquaxtreme. Al crear la ficha de Google
> es probable que aparezca una sugerencia de "este negocio ya existe". **No reclames esa
> ficha**: crea una nueva a nombre de ISANAT. Y vale la pena confirmar con el cliente
> cómo es el acuerdo con el colegio y con esa academia, porque dos negocios en una misma
> dirección compiten por el mismo pack de mapas.

---

## 5. TODO — datos pendientes de confirmar con el cliente

Nada de esto está inventado en el sitio: donde falta el dato, la web deriva a WhatsApp.
Los puntos que tocan el HTML llevan un comentario `TODO` en el archivo.

**Esto es el cuello de botella del proyecto.** Buena parte de lo que la auditoría
recomienda no se puede ejecutar sin estos datos, y ninguno depende de programar.

| # | Pendiente | Qué desbloquea | Dónde se cambia |
|---|---|---|---|
| 1 | ⚠️ **Discrepancia flyer ↔ WhatsApp en los niños.** El flyer separa "Menores 3-5" e "Infantiles 6-15" y da sábado desde las 06:00; el mensaje de WhatsApp los junta en 3-15 con sábados de 9 a 12. **Se publicó el WhatsApp** por ser más reciente y más conservador. | Que los horarios de niños sean exactos | Tabla de niños en `datos` y en las 2 páginas |
| 2 | **Duración de las clases** de niños y de adultos. Solo consta la de aquabebé (45 min, del flyer). | Una respuesta que los padres preguntan siempre | FAQ de niños y adultos |
| 3 | **Aquabebé: ¿entra mamá o papá al agua?** y qué llevar (pañal de agua, gorro). | Cerrar el aviso de la página de bebés | `/natacion-para-bebes-la-molina/` |
| 4 | **Calificación MINSA:** número de resolución y fecha. Hoy se publica la afirmación tal como está en el flyer del cliente. | Poder respaldarla si alguien pregunta | Home, bloque "Por qué elegir" |
| 5 | **Coordenadas GPS reales.** Salen de la URL de la ficha verificada en Google Maps: los números tras `!3d` y `!4d`. | Que el mapa apunte a la puerta y no a la manzana | Las 5 páginas: `geo.position`, `ICBM` y `geo` del schema |
| 6 | **Instructores**: nombres, foto, certificaciones y **consentimiento por escrito**. | `/instructores/`, donde vive el E-E-A-T. Ningún competidor nombra a los suyos | Página nueva + schema `Person` |
| 7 | **Fotos reales** de la piscina y las clases (15+). | Hero, tarjetas, `og-image.jpg`, ficha de Google y `image[]` del schema | Todas |
| 8 | **Datos de la piscina**: temperada, techada, medidas, carriles, vestuarios, estacionamiento. | Ventajas verificables y `/piscina-villa-caritas/` | Home + página nueva |
| 9 | **¿Hay clases particulares?** No se mencionan en ninguna fuente. | `/clases-particulares-natacion-la-molina/` | Página nueva |
| 10 | **Política de reprogramación** si el alumno falta. | Una FAQ que la competencia tampoco responde | `/horarios-y-precios/` |
| 11 | **URLs de Facebook e Instagram.** | El `sameAs` del schema y los iconos del pie | Pie + schema |
| 12 | **Meta Pixel ID**, si se va a hacer Meta Ads. | El píxel, hoy apagado a propósito | `var PIXEL_ID = ''` del `<head>` |
| 13 | **Relación contractual con el colegio** y con AquaXtreme, que opera en la misma dirección. | La ficha de Google: dos negocios en una dirección compiten por el mismo pack de mapas | Ficha de Google |
| 14 | **Código postal.** Se quitó del schema por no estar verificado. | `postalCode` del `PostalAddress` | Schema de las 5 páginas |

### Resuelto con los datos del cliente (v1.2.0 · v1.2.1 · v1.3.0)

Horarios por programa · **precios mensuales** por frecuencia · **sin matrícula** ·
**IGV incluido** · edades exactas (6 m–2 a, 3–15, 16+) · que **sí** se atienden bebés ·
el descuento del 40 % de la comunidad VCSP · el proceso real de matrícula · las formas
de pago · el RUC · el segundo teléfono · la calificación MINSA · y que **no** existe
nado libre.

**Nada de lo que está publicado depende ya de un dato sin confirmar**, salvo la
discrepancia del sábado de niños, donde se publicó la versión conservadora.

### Páginas que ya están diseñadas y NO se publicaron

Se decidió no crearlas porque **serían páginas vacías**, y una página delgada posiciona
peor que ninguna y arrastra al resto del sitio:

`/instructores/` · `/clases-particulares-natacion-la-molina/` ·
`/piscina-villa-caritas/` · `/verano/` · `/blog/` · `/libro-de-reclamaciones/`

El orden de impacto, si los datos llegan en partes: **6 (instructores) → 7 y 8
(fotos y datos de la piscina) → 9 (particulares)**.

---

## 6. Reglas al editar

- **El `<title>` no se toca por 6 meses.** Cada cambio reinicia parte del aprendizaje
  de Google y genera 1 a 3 semanas de volatilidad en posiciones.
- **FAQ visible = FAQ del schema.** Si editas una pregunta o respuesta en el cuerpo
  del HTML, tienes que editarla idéntica en el bloque `FAQPage` del `<head>`. Si solo
  está en el JSON-LD, Google lo considera contenido engañoso.
- **Nunca prometer un servicio que no se presta.** Antes de agregar un término porque
  aparece en Search Console, confirmar con el cliente que efectivamente lo ofrece.
- **Nada de texto oculto con keywords.** Está listado explícitamente en las políticas
  de spam de Google y arriesga una acción manual.
- Al cambiar contenido, actualizar `<lastmod>` en `sitemap.xml`.
- Imágenes nuevas: WebP, con `width` y `height` explícitos y `loading="lazy"`
  (menos la primera visible, que va con `fetchpriority="high"`).
- **Una URL publicada no cambia.** Si es imprescindible, 301 en `_redirects` y
  actualizar sitemap, enlaces internos y canonical el mismo día.
- **Toda página nueva entra en el menú o en el pie y recibe al menos 2 enlaces desde
  el cuerpo de otras páginas.** Una página huérfana es una página que Google no visita.
- **No repetir las mismas FAQ en varias páginas.** El NAP repetido está bien; seis
  preguntas idénticas en cuatro URLs, no. Cada página con las suyas.
- **Al tocar `css/site.vN.css` o `js/site.vN.js`, subir el número del nombre** y
  actualizar las **siete** páginas. Están cacheados un año.

### Idiomas (desde la v1.4.0)

- **`/en/` y `/pt/` son UNA página cada una, no un espejo del sitio.** Llevan toda la
  oferta: programas, horarios, precios, ubicación y FAQ. El objetivo es que un lead que
  no habla español y **ya llegó** pueda leerlo todo, no posicionar en esos idiomas.
- **El `hreflang` recíproco vive solo entre `/`, `/en/` y `/pt/`**, más `x-default` al
  español. Las páginas interiores en español **no** declaran alternativas porque no las
  tienen: eso es correcto, no un olvido. `tools/validar.py` comprueba la reciprocidad.
- **El hreflang no se duplica en el `sitemap.xml`.** Google acepta cualquiera de los
  dos sitios; tenerlo en uno solo evita que las dos copias se contradigan.
- **El selector de idioma es un único bloque** dentro de `<nav id="nav">`: en escritorio
  cae a la izquierda del CTA de WhatsApp y en móvil entra en el menú desplegado. No se
  duplica el marcado. Palabras y nunca banderas: una bandera es un país, no un idioma.
- **Si cambias un horario o un precio en `datos.py`, hay que traducirlo también.** Los
  diccionarios `DIAS`, `HORAS` y `FREQ` de `intl.py` hacen fallar la construcción si
  aparece una etiqueta sin traducción — mejor un error que media tabla en español.
- ⚠️ **La cabecera colapsa a 960 px, no a 768.** Con el selector dentro, entre 769 y
  940 px la fila no cabía y el botón de WhatsApp del header quedaba fuera de pantalla.
  Si añades algo más a la cabecera, mide de nuevo ese rango.
- **Correr `python3 tools/validar.py` antes de cada push.** Falla si el HTML no parsea,
  si el schema no coincide con las FAQ visibles, si un enlace interno apunta a un
  archivo que no existe, si el title se pasa de 60 caracteres, si queda un `TODO`
  visible, si la cabecera o el pie se desincronizaron **dentro de un mismo idioma**, o
  si una anotación `hreflang` no es recíproca.

---

## 7. Probar en local

No hace falta ningún build. Basta con levantar un servidor estático para que las rutas
absolutas (`/img/...`, `/fonts/...`) resuelvan bien:

```bash
python3 -m http.server 8000
# luego abrir http://localhost:8000
```

Y antes de subir nada:

```bash
pip install html5lib beautifulsoup4   # solo la primera vez
python3 tools/validar.py
```

---

## 8. Cómo se instala una entrega nueva

Cada entrega llega como un zip con la versión en el nombre
(`isanat-v1.1.0-2026-09-13.zip`) y trae **el repositorio completo**, no solo los
archivos que cambiaron. Eso significa que se reemplaza la carpeta entera.

> ⚠️ **Descomprimir encima NO borra lo que sobra.** El 12/09 `vercel.json` y
> `GUIA-GIT-VERCEL.md` llegaron al repo justamente así. Hay que vaciar la carpeta
> primero, **conservando `.git`**, que es donde vive el historial.

> ⚠️ **Y la comprobación después de instalar NO es `git status`: es contar los
> archivos.** El 13/09 la carpeta `nado-libre-la-molina/` sobrevivió a dos
> instalaciones y a un push, y `git status` nunca dijo nada — el archivo estaba
> *tracked* y no había cambiado, así que para git no pasaba nada. Lo cazó
> `tools/validar.py` contando 7 páginas donde debía haber 6.

### Opción A — símbolo del sistema (`cmd.exe`), el que se abre por defecto

Si la ventana negra empieza con `D:\isanatgit>`, es esta. `Get-ChildItem` **no
existe** aquí: da *"no se reconoce como un comando interno o externo"*.

```bat
cd /d D:\isanatgit

REM 1 - Vaciar la carpeta SIN tocar .git.
REM     Se llama a PowerShell para esta linea: en cmd hacerlo a mano es
REM     largo y facil de equivocar, y equivocarse aqui borra el historial.
powershell -NoProfile -Command "Get-ChildItem -Force -Exclude .git | Remove-Item -Recurse -Force"

REM 2 - Descomprimir el zip nuevo aqui dentro, con el explorador de Windows.
REM     Comprobar que quedaron VISIBLES index.html, VERSION y la carpeta css.

REM 3 - Contar los archivos: tienen que ser los que trae el paquete
dir /s /b /a-d | find /c /v ""

REM 4 - Validar y subir
git status
python tools\validar.py
git add -A
git commit -m "v1.3.1 corrige la csp que bloqueaba las speculation rules"
git push origin main
```

> ⚠️ Si el paso 1 deja la carpeta vacía y el paso 2 no llega a hacerse, `git status`
> mostrará **decenas de archivos borrados**. No hay que commitear eso: se descomprime
> el zip y vuelve a la normalidad. Y si hace falta deshacerlo todo, `git restore .`.

### Opción B — PowerShell

Si la ventana empieza con `PS D:\isanatgit>`, es esta:

```powershell
cd D:\isanatgit

# 1 · Vaciar la carpeta SIN tocar .git
Get-ChildItem -Force -Exclude .git | Remove-Item -Recurse -Force

# 2 · Descomprimir el zip nuevo aquí dentro
#     (con el explorador de Windows, o:)
Expand-Archive -Path "$env:USERPROFILE\Downloads\isanat-v1.1.0-2026-09-13.zip" -DestinationPath . -Force

# 3 · Comprobar que git ve lo mismo que trae el paquete
git status

# 4 · Validar antes de subir
python tools/validar.py

# 5 · Subir
git add -A
git commit -m "v1.1.0 sitio multipagina con paginas por programa"
git push origin main
```

`git add -A` es la parte importante: registra también los archivos **borrados**. Con
`git add .` a secas, lo que se eliminó seguiría vivo en el repo y, por lo tanto, en el
sitio publicado.

Después del push: abrir Cloudflare → *Deployments*, esperar el verde, abrir el sitio
en incógnito, hacer `Ctrl+U` y confirmar que el marcador dice `1.1.0`. Luego anotar el
hash del deploy en `CAMBIOS.md`.

Abrir el `index.html` con doble clic también funciona, pero las rutas absolutas
fallan y no vas a ver el logo ni las fuentes.
