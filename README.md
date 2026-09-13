# ISANAT — Escuela de Natación · La Molina, Lima

Sitio web estático de ISANAT. Sin build, sin dependencias: son archivos HTML, CSS y
JS planos que se suben tal cual. Cuatro páginas indexables.

**Versión actual: `1.1.0`** — ver [`CAMBIOS.md`](CAMBIOS.md).

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
├── nado-libre-la-molina/
│   └── index.html                          Membresía de nado libre
├── 404.html                                Error, la sirve Cloudflare sola. Autocontenida
├── css/
│   └── site.v1.css                         TODO el CSS del sitio (excepto el 404)
├── js/
│   └── site.v1.js                          TODO el JS del sitio
├── tools/
│   └── validar.py                          Validador. Correr antes de cada push
├── robots.txt                              Permite indexación + apunta al sitemap
├── sitemap.xml                             Las 4 URLs. Actualizar <lastmod> al cambiar contenido
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
2. El **`<meta name="version">`** de las cinco páginas. Abre el sitio publicado,
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
| 1 | **Coordenadas GPS reales.** Las actuales son aproximadas de la zona Rinconada del Lago. Salen de la URL de la ficha verificada en Google Maps: los números tras `!3d` (latitud) y `!4d` (longitud). | Que el mapa y el schema apunten a la puerta y no a la manzana | Las 4 páginas: meta `geo.position`, meta `ICBM` y `geo` del schema |
| 2 | **Horarios de atención.** | La página `/horarios-y-precios/`, el bloque `openingHoursSpecification` y la ficha de Google | Sección Ubicación + schema |
| 3 | **Horarios por programa** (niños, adultos, nado libre), con periodo de vigencia. | La página `/horarios-y-precios/` con tablas reales, que es la P1 que más tráfico capta | Página nueva |
| 4 | **Precios por frecuencia semanal.** Referencia de mercado en la zona: S/ 150 a S/ 580 según frecuencia y edad — **es referencia, no el precio de ISANAT**. | Lo mismo, más `priceRange` en el schema | Página nueva + schema |
| 5 | **Edad mínima** de las clases de niños, y cómo quedan armados los niveles. | Las FAQ de `/natacion-para-ninos-la-molina/` y el `audience` del schema | FAQ visible **y** `FAQPage` del `<head>` — las dos, idénticas |
| 6 | **¿Se atienden bebés?** Si sí: edad mínima, si va acompañado, temperatura del agua. | La página `/natacion-para-bebes-la-molina/`. Es el hueco de contenido más limpio del distrito | Página nueva |
| 7 | **¿Hay clases particulares?** | La página `/clases-particulares-natacion-la-molina/` | Página nueva |
| 8 | **Requisitos del nado libre**: edad mínima y nivel exigido. | Las FAQ de `/nado-libre-la-molina/`, hoy contestadas con "consúltanos" | FAQ visible y schema |
| 9 | **Instructores**: nombres, foto, certificaciones verificables y **consentimiento por escrito**. | La página `/instructores/`, que es donde vive el E-E-A-T. Ningún competidor nombra a los suyos: es la ventaja más grande disponible | Página nueva + schema `Person` |
| 10 | **Fotos reales** de la piscina y de las clases (15+). | El hero, las tarjetas, `og-image.jpg`, la ficha de Google y el `image[]` del schema | Todas |
| 11 | **Datos de la piscina**: si es temperada, techada, medidas, carriles, vestuarios, estacionamiento. | El bloque "Por qué elegir" con ventajas reales y la página de la piscina | Home + página nueva |
| 12 | **URLs de Facebook e Instagram.** | El `sameAs` del schema y los iconos del pie, hoy eliminados por no tener destino | Pie + schema |
| 13 | **Meta Pixel ID**, si se va a hacer Meta Ads. | El píxel, hoy apagado a propósito | `var PIXEL_ID = ''` del `<head>` |
| 14 | **Proceso real de inscripción.** Los 3 pasos de "Cómo empezar" son una suposición razonable sin validar. | Que la home no describa un proceso que no existe | Sección Cómo empezar + FAQ "¿Cómo reservo?" |
| 15 | **Política de reprogramación** y formas de pago. | Dos FAQ que la competencia tampoco responde | FAQ + página de precios |
| 16 | **Relación contractual con el colegio** y con AquaXtreme, que opera en la misma dirección. | La ficha de Google: dos negocios en una dirección compiten por el mismo pack de mapas, y la verificación puede exigir cartelería física con el nombre ISANAT | Ficha de Google |
| 17 | **Código postal** de la dirección. Se quitó del schema por no estar verificado: un NAP con un dato inventado es peor que sin él. | `postalCode` del `PostalAddress` | Schema de las 4 páginas |

### Páginas que ya están diseñadas y NO se publicaron

Se decidió no crearlas porque **serían páginas vacías**, y una página delgada posiciona
peor que ninguna y arrastra al resto del sitio:

`/horarios-y-precios/` · `/instructores/` · `/natacion-para-bebes-la-molina/` ·
`/clases-particulares-natacion-la-molina/` · `/piscina-villa-caritas/` · `/verano/` ·
`/blog/` · `/libro-de-reclamaciones/`

El orden de impacto, si los datos llegan en partes: **9 (instructores) → 3 y 4
(horarios y precios) → 6 (bebés) → 10 y 11 (fotos y piscina)**.

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
  actualizar las cuatro páginas. Están cacheados un año.
- **Correr `python3 tools/validar.py` antes de cada push.** Falla si el HTML no parsea,
  si el schema no coincide con las FAQ visibles, si un enlace interno apunta a un
  archivo que no existe, si el title se pasa de 60 caracteres, si queda un `TODO`
  visible o si la cabecera y el pie se desincronizaron entre páginas.

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

En PowerShell, desde `D:\isanatgit`:

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
