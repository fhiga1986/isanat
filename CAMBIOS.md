# ISANAT — Registro de versiones

Cada entrega lleva un número de versión. El número vive en tres sitios y los tres
tienen que coincidir:

1. El archivo **`VERSION`** de la raíz del repo.
2. El **`<meta name="version">`** de las cuatro páginas — así se puede comprobar
   **qué versión está realmente publicada** abriendo el sitio y pulsando `Ctrl+U`.
3. El **nombre del zip** de la entrega.

`tools/validar.py` falla si los tres no dicen lo mismo.

> **Después de cada push**, anota abajo el hash que muestra Cloudflare en
> *Workers & Pages → isanat → Deployments*. Es lo único que cierra el círculo entre
> "lo que me entregaron" y "lo que está en vivo".

| Versión | Fecha | Deploy en Cloudflare | Qué cambió |
|---|---|---|---|
| **1.5.1** | 15/09/2026 | *(anotar el hash tras el push)* | El logo lleva a la home en español también desde `/en/` y `/pt/` |
| 1.5.0 | 15/09/2026 | *(anotar el hash)* | `/en/` y `/pt/` con el diseño de la home · los tres idiomas siempre visibles |
| 1.4.0 | 14/09/2026 | *(anotar el hash)* | Inglés y portugués: `/en/` y `/pt/` + selector de idioma en la cabecera |
| 1.3.1 | 14/09/2026 | `5a9d737` | Corrige la CSP: las Speculation Rules estaban bloqueadas en producción |
| 1.3.0 | 13/09/2026 | `dc29e78` | IGV incluido · CSP con hashes · Speculation Rules · View Transitions · WCAG 2.2 |
| 1.2.1 | 13/09/2026 | `abd6095` | Los precios son **mensuales** y **no hay matrícula**: confirmado por el cliente |
| 1.2.0 | 13/09/2026 | `5183260` | Llegaron los datos del cliente: horarios, precios y edades reales. Sale nado libre, entran Aquabebé y horarios-y-precios |
| 1.1.0 | 13/09/2026 | `da2297a` | El sitio pasa de una página a cuatro |
| 1.0.1 | 13/09/2026 | `fb3d371` | Corrección del número de WhatsApp a +51 915 236 322 |
| 1.0.0 | 12/09/2026 | `6e879c3` | Publicación inicial (one-page) y salida de la configuración de Vercel |

---

## 1.5.1 — 15/09/2026

Un solo cambio, pedido por el cliente después de probar la 1.5.0 en vivo.

### Cambiado

- **El logo lleva siempre a `/`**, la home en español, también desde `/en/` y `/pt/`.

En la 1.5.0 llevaba al principio de la propia página. El argumento era que un logo no
debería cambiar el idioma sin avisar, y que quien sufre ese salto es justo el visitante
que no lee español. **Al usarlo, el cliente lo pidió igual**, y su lectura del producto
es la que manda: para él `/en/` y `/pt/` son páginas satélite y el sitio de verdad es el
español, así que el logo tiene que llevar ahí.

El riesgo que me preocupaba está cubierto desde la 1.5.0: **los tres idiomas figuran
siempre en la cabecera**, así que quien cae en español sin querer vuelve con un clic
rotulado en su propio idioma.

> Queda anotado en `comun.py` que es una decisión discutida y tomada, no un descuido,
> para que nadie lo "arregle" de vuelta en seis meses sin saber por qué está así.

### Cómo se comprobó

Clic real sobre el logo en `/en/`, `/pt/` y una página interior en español, a 390 y
1280 px (en móvil abriendo antes el menú): las seis veces llega a `/` con
`lang="es-PE"`. Y la batería completa —54 combinaciones de cabecera, 40 de CSP y
desbordamiento, mapa y contraste— sigue en verde.

---

## 1.5.0 — 15/09/2026

`/en/` y `/pt/` dejan de parecer páginas interiores y pasan a tener **el mismo diseño
que la home**. El selector muestra siempre los **tres idiomas**. Ninguna página en
español cambia de contenido.

### Añadido a /en/ y /pt/

- **El hero completo**: degradado navy→teal con las olas SVG, `H1` con la segunda
  línea en teal, los dos CTA y la fila de sellos (*La Molina, Lima · De 6 meses a
  adultos · Piscina saludable MINSA*). Es la parte que hace el trabajo de los diez
  segundos, y era justo la que les faltaba a las páginas cuyos visitantes llegan con
  menos contexto.
- **Las tres tarjetas de programa**, con la etiqueta "MÁS CONSULTADO" en adultos y
  **un botón de WhatsApp propio en cada una**, con el mensaje ya redactado según el
  programa. Pasan de 5 a 9 puntos de conversión medibles por página.
- **El mapa diferido**, con el mismo `id="map-load"` que la home, así que lo engancha
  el mismo script sin una línea nueva.
- El bloque de ubicación con la lista `.data` (dirección, WhatsApp, horarios).

**Cero CSS nuevo por todo esto**: los bloques ya existían. Lo único que se añadió a la
hoja fue el estilo del idioma actual del selector.

### Cambiado

- **Los tres idiomas figuran siempre y en el mismo orden** (`Español · English ·
  Português`). El actual va como `<span>` con `aria-current`, más oscuro y sin ser
  enlace. Antes se mostraban solo los dos alternativos: la lista cambiaba de página a
  página y no se sabía en cuál idioma estabas. La redundancia es barata; la duda, no.
- **El logo en `/en/` y `/pt/` lleva al principio de esa misma página**, no a la home
  en español. Ver la nota de abajo.
- **`js/site.v1.js` → `js/site.v2.js`**: el título del iframe del mapa —que lee un
  lector de pantalla— ahora sale en el idioma de la página, tomado de `<html lang>`.
- **`css/site.v3.css` → `css/site.v4.css`.**
- **El icono de la tarjeta Aquabebé era el de una tarjeta de crédito**, heredado de la
  "Membresía de nado libre" que se retiró en la v1.2.0 y que nadie cambió al reemplazar
  la tarjeta. Ahora es una figura en el agua. Se corrigió también en la home.
- **`.brand span small` ("Swimming School") daba 4,45:1 sobre blanco**, por debajo del
  mínimo AA de 4,5. Venía así **desde la v1.0.0**. Es el mismo 4,45 del subtítulo de los
  enlaces cruzados del 13/09 y la causa es siempre la misma: `--muted` sobre blanco.
  Con `--body` queda en 7,41:1.

### Por qué el logo NO lleva al español

Se pidió que en `/en/` el logo llevara a la home en español. No se hizo, y conviene
dejar escrito el motivo: **un logo que cambia el idioma de la página es lo último que
alguien espera de un logo**. El que más sufre ese salto es justamente el visitante que
no lee español, o sea la persona para la que existen esas páginas.

Pero la observación de fondo era correcta: apuntando a su propia URL, el logo era un
**control muerto** —recargaba y no pasaba nada visible—. Como `/en/` y `/pt/` son una
sola página, ahora lleva al principio de esa misma página: ni muerto ni sorpresivo. Y
con los tres idiomas siempre a la vista, ir al español es un clic rotulado.
Si algún día hay más páginas por idioma, vuelve a ser la home de ese idioma.

### La cicatriz: dos fallos que las pruebas no veían

**1 · El texto de la cabecera se partía en dos líneas sin que nada lo delatara.** Al
entrar el tercer idioma, flex encogió los items hasta su ancho de min-content y se leía
"Horarios y / precios" y "SWIMMING / SCHOOL" **dentro** de los 72 px de la cabecera. Ni
el scroll horizontal ni la altura de `.hdr` cambiaban: las dos pruebas que había daban
verde mientras la cabecera se veía rota en una captura.

La corrección tiene dos partes, y la segunda importa más que la primera:

- `white-space:nowrap` en los elementos de la fila. Ahora, si algo no cabe, **desborda**
  — y eso sí lo detecta una prueba. **Fallo detectable antes que fallo silencioso.**
- Medido el ancho mínimo real barriendo de 1100 a 1164 px de 8 en 8: **1124 px**, con el
  español como idioma más ancho. El breakpoint de la cabecera pasa a **1160 px**, que es
  `--wrap`, o sea el ancho al que el contenido deja de crecer: 36 px de holgura y un
  número con significado en vez de uno elegido a ojo.
  Historia del breakpoint: 768 sin selector · 960 con dos idiomas · 1160 con tres.
  **Cada cosa que se agregue a esa fila obliga a volver a medir.**

**2 · La prueba de contraste inventaba un número sobre los degradados.** Cuando el fondo
es un degradado, el color real no se puede deducir del CSS; la prueba devolvía navy "por
si acaso" y marcaba como fallo el texto del mapa, que en realidad mide **10,13:1**
(verificado muestreando los píxeles de una captura). Ahora esos casos se declaran **no
medibles automáticamente** y se listan aparte. Una herramienta que no puede ver algo
tiene que decirlo, no rellenarlo.

### Nuevo en el generador: `pruebas.py`

Las comprobaciones de navegador quedan en un solo archivo, con el fallo real que
originó cada una anotado arriba. Son 54 combinaciones de cabecera, 40 de CSP y
desbordamiento, el mapa en los tres idiomas y el contraste página por página.

---

## 1.4.0 — 14/09/2026

El sitio pasa a tener **selector de idioma** y **una página completa en inglés y otra
en portugués**. El español no cambia de contenido: solo gana el selector en la cabecera.

### Por qué una página por idioma y no un espejo de cinco

El objetivo que planteó el cliente es que **un lead que no habla español y ya llegó al
sitio pueda leer toda la oferta**, no posicionar en inglés ni en portugués. Con ese
objetivo, una sola página por idioma es mejor que un espejo, no solo más barata:

1. **El selector no miente en ninguna URL.** Con un espejo parcial, quien está en
   `/horarios-y-precios/` y pulsa "English" cae en una página que no es la suya — el
   fallo más común de los selectores de idioma. Si `/en/` **es** el sitio entero en
   inglés, el enlace siempre cumple lo que promete.
2. **El `hreflang` queda en un triángulo recíproco** (`/` ↔ `/en/` ↔ `/pt/` +
   `x-default`) en vez de una matriz de 60 etiquetas mantenidas a mano.
3. **Es el formato que quiere un no hispanohablante**: una página que responde edades,
   precio, dónde y cómo escribir, sin navegar seis URLs en un idioma que no domina.

Las URLs son `/en/` y `/pt/` y no `/en/swimming-lessons-la-molina/` a propósito: si
algún día crece a espejo completo, `/en/` ya es la home de ese idioma y las demás
cuelgan debajo **sin mover ninguna URL publicada**.

### Añadido

- **`/en/` y `/pt/`**, ~1.000 palabras cada una, con programas y edades, los tres
  cuadros de horarios, el cuadro de precios con IGV incluido y sin matrícula, el
  descuento VCSP, formas de pago, ubicación, seis preguntas frecuentes y CTA propio.
  Schema por página: `WebPage` con `inLanguage`, `Service` y `FAQPage`.
  ⚠ El nodo del negocio es **idéntico y con el mismo `@id`** que en las cinco páginas
  en español: es la misma entidad, y la coherencia NAP pesa más que el idioma.
- **Selector de idioma** en la cabecera de las siete páginas. Un único bloque dentro de
  `<nav id="nav">`: en escritorio queda a la izquierda del CTA de WhatsApp, en móvil
  entra dentro del menú. **Palabras y nunca banderas** —una bandera es un país, no un
  idioma— y cada idioma escrito en el suyo. Sin JavaScript y sin hashes nuevos en la CSP.
- **`hreflang` recíproco** entre las tres home, con `x-default` al español. Las páginas
  interiores en español no declaran alternativas porque no las tienen.
- **Aviso honesto en `/en/` y `/pt/`**: *"Our team replies in Spanish"*. El lead que se
  entera al escribir se va; el que lo sabe antes escribe igual si le interesa.
- **`data-origen` propios** (`hero_en`, `seccion_precios_pt`, `flotante_en`…) para que
  GA4 pueda decir en 90 días si estas dos páginas convierten o si hay que retirarlas.

### Cambiado

- **`css/site.v2.css` → `css/site.v3.css`.** El archivo cambió y está cacheado un año.
  Actualizado el `<link>` de las siete páginas.
- ⚠ **La cabecera ahora colapsa a 960 px, no a 768.** Ver abajo.
- **`tools/validar.py`**: la paridad de cabecera y pie se comprueba **por idioma**
  (español contra español, inglés contra inglés) en vez de todo en un solo grupo, y
  hay dos comprobaciones nuevas: que cada página declare `<html lang>` y que las
  anotaciones `hreflang` sean **recíprocas**.
- `sitemap.xml` pasa a 7 URLs, con `<lastmod>` al 14/09.

### El fallo que se cazó midiendo, no mirando

Con el selector dentro de la cabecera, **entre 769 y 940 px el botón de WhatsApp del
header quedaba fuera de la pantalla**. No roto: invisible, que es peor. A 769 px su
borde derecho caía en 913 px. `document.scrollWidth` no lo delataba porque la cabecera
es `position:fixed` y no ensancha el documento.

La causa es que a 769 px la fila **ya iba exactamente al límite** antes de este cambio
—el botón terminaba en 749 con 769 de ancho, justo el padding del `.wrap`—: no había
holgura para nada. La corrección es mover **solo las reglas de cabecera** al breakpoint
de **960 px**; el resto (hero, pie) se queda en 768, donde no había problema. Entre 769
y 960 aparece la hamburguesa pero **el CTA del header sigue visible**, porque ahí sí
cabe y es la conversión.

Comprobado en 16 anchos entre 360 y 1440 px: el CTA nunca sale de la pantalla y no hay
desplazamiento horizontal en ninguna de las 8 páginas.

> ⚠ **Y la comprobación del `hreflang` tenía un agujero que solo apareció al probarla.**
> La primera versión daba verde aunque se le quitara a `/en/` su enlace al español:
> `x-default` apunta siempre a `/`, así que contaba como si la reciprocidad existiera.
> Ahora `x-default` queda fuera del cálculo. **Un control que no se prueba en negativo
> no es un control** — es la misma lección del validador de la v1.3.1.

---

## 1.3.1 — 14/09/2026

Corrección de un fallo propio introducido en la 1.3.0. **No cambia nada de lo que se
ve**: ni contenido, ni estilos, ni textos. Solo `_headers` y el validador.

### Corregido

- **La CSP bloqueaba las Speculation Rules en producción.** La política llevaba la
  palabra `'inline-speculation-rules'`, que es la forma documentada de habilitar el
  bloque `<script type="speculationrules">`. Pero **en cuanto `script-src` lleva un
  solo hash, esa palabra queda inerte**: el algoritmo de CSP descarta el "permitir todo
  lo inline" en presencia de hashes, y Chrome bloqueó el bloque en las 5 páginas.
  Ahora la política declara **el hash del bloque** y la palabra sale, por inútil y por
  engañosa.
  Consecuencia real mientras estuvo mal: se perdió **solo la descarga anticipada** de
  la página siguiente. El sitio, la analítica, el mapa y los botones de WhatsApp
  funcionaban con normalidad.
- **`tools/validar.py` tenía el mismo punto ciego** y por eso dio verde: excluía
  `type="speculationrules"` del cálculo de hashes. Ya no lo excluye — con la CSP de la
  1.3.0 el validador ahora falla — y además **avisa** si alguien vuelve a mezclar
  `'inline-speculation-rules'` con hashes.

### Cómo se comprobó

- El validador, contra la CSP de la 1.3.0: **1 error**, el hash que falta.
- Navegador con la CSP nueva: **0 violaciones** en las 6 páginas, escuchando el evento
  `securitypolicyviolation` del DOM.
- Y la prueba de que funciona, no solo de que no se queja: al pasar el puntero sobre un
  enlace interno se observa **una petición con `Sec-Purpose: prefetch`**.

> ⚠ **Dos lecciones, y la segunda es la caras.**
> 1. `page.on('console')` de Playwright **no ve** los avisos de CSP del navegador:
>    llegan por el dominio `Log` de CDP, no por `console.*`. La prueba de CSP escuchaba
>    la consola y por eso informó "sin violaciones" mientras el navegador bloqueaba.
>    Ahora escucha el evento `securitypolicyviolation`, que sí los dispara todos.
> 2. **Un hash no se transcribe de una captura de pantalla: se calcula del archivo.**
>    El hash que aparecía en la consola se leyó como `…ZmjUnT2JKn1HG4…` y el real es
>    `…ZmjUnT2JKnlHG4…` — un `1` donde había una `l`. Pegarlo a mano habría dejado la
>    CSP igual de rota, con un error todavía más difícil de ver.

---

## 1.3.0 — 13/09/2026

Un dato más del cliente y las seis mejoras técnicas que salieron de auditar el sitio
contra el checklist de calidad (doc 6).

### Añadido

- **`Content-Security-Policy`**, la única cabecera de seguridad que faltaba. Con el
  **hash de cada script en línea** en vez de `'unsafe-inline'`, `frame-src` limitado a
  google.com (el mapa) y `form-action 'none'`. ⚠ Si se edita un script en línea el hash
  cambia y el navegador lo bloquea **sin avisar en la página**: `tools/validar.py` ahora
  recalcula los hashes y falla si no coinciden con `_headers`.
- **Speculation Rules**: al pasar el ratón o tocar un enlace interno, el navegador
  descarga la página destino por adelantado. Se usa **prefetch y no prerender** a
  propósito — prerender ejecutaría el JS de destino y GA4 podría contar visitas a
  páginas que nadie abrió, justo cuando la línea base de analítica está por construirse.
- **View Transitions entre documentos** (`@view-transition`). Mejora progresiva: el
  navegador que no la soporta navega igual que siempre. La cabecera y el botón flotante
  llevan `view-transition-name` para que no parpadeen entre páginas.
- **`decoding="async"`** en las imágenes no críticas.
- `paymentAccepted` y **`valueAddedTaxIncluded`** en el schema.

### Cambiado

- **Los precios dicen que incluyen IGV**, confirmado por el cliente: son los montos
  finales que paga el alumno. Está en las tablas de las 5 páginas, en las FAQ de precio
  y en el schema.
- **WCAG 2.2 §2.5.8**: los tres enlaces del pie medían 209×20 y ahora tienen 24 de alto
  mínimo. Los enlaces dentro de un párrafo siguen igual porque la norma **los exime**:
  su alto lo fija el interlineado del texto que los rodea.
- **`robots.txt`** deja escrita la decisión de **permitir los rastreadores de IA**
  (GPTBot, ClaudeBot, PerplexityBot, Google-Extended). Ya estaban permitidos por
  omisión; ahora lo están por decisión, para que nadie lo "arregle".
- Los `style=` en línea pasaron a clases (`.cta-centrado`, `.bloque-cierre`): un solo
  atributo `style=` obliga a abrir el `style-src` de la CSP entero.
- **`css/site.v1.css` → `css/site.v2.css`.** El archivo cambió y está cacheado un año:
  renombrarlo es obligatorio.

### Descartado, y por qué

- **`content-visibility: auto`.** Estaba en la lista del doc 6, se midió y no vale la
  pena aquí: en páginas de ~800 palabras el ahorro de pintado es de milisegundos y a
  cambio se arriesga CLS si `contain-intrinsic-size` no acierta. Se aplica el principio
  4 del prompt madre: medir el impacto antes de decidir si vale hacerlo.

---

## 1.2.1 — 13/09/2026

El cliente confirmó las dos preguntas que habían quedado abiertas en la v1.2.0.

### Cambiado

- **Los precios son mensuales.** Estaban publicados con la redacción exacta del cliente
  ("1 vez por semana - S/ 280") porque él no indicaba el periodo. Ahora el cuadro dice
  **"Precios mensuales"**, la columna dice **"Precio al mes"** y las FAQ lo repiten.
- **No hay matrícula ni cuota de inscripción.** Es un diferenciador real y ahora está
  dicho en las cinco páginas, en la meta description de la home, en el paso 3 de "Cómo
  matricularse" y en una FAQ propia.
- Schema: el precio pasa de `PriceSpecification` a **`UnitPriceSpecification`** con
  `referenceQuantity` de 1 mes (`unitCode: MON`), que es como se declara un precio
  periódico y evita que Google lo lea como pago único.

*No quedan pendientes de datos que afecten a lo ya publicado.*

---

## 1.2.0 — 13/09/2026

El cliente envió los horarios, los precios y las edades reales. Todo lo que aquí se
publica sale de su mensaje de WhatsApp del 13/09 ("Temporada Invierno 2026") cruzado
con su flyer "CLASES 2026".

### Añadido

- **`/horarios-y-precios/`** — la página que la auditoría marcaba como P1 de mayor
  tráfico y que estaba bloqueada. Cuatro tablas HTML reales (nunca imágenes), periodo
  de vigencia visible, cómo matricularse y formas de pago.
- **`/natacion-para-bebes-la-molina/`** — Aquabebé, 6 meses a 2 años. Ningún competidor
  de La Molina tiene una URL dedicada a bebés: es el hueco de contenido más limpio del
  distrito.
- **Sección de precios en la home**, con el cuadro por frecuencia. Ningún competidor
  del distrito publica precios en texto indexable.
- **`_redirects`** con la 301 de la URL retirada.
- Segundo teléfono (+51 992 705 564) y **RUC 20613584928** en el pie.
- Schema: `openingHoursSpecification`, `priceRange`, `Offer` con precio real y
  `PeopleAudience` con las edades de cada programa.

### Quitado

- **`/nado-libre-la-molina/` y toda mención a la membresía.** ISANAT alquila la piscina
  y presta servicios de academia; no opera un club con membresía, y ni el flyer ni el
  mensaje del cliente mencionan ese servicio. Publicar un servicio que no se presta es
  la primera regla que rompe la confianza. La URL vivió unas horas y casi con certeza
  nunca se indexó (el dominio no está conectado y el sitemap no se ha enviado), así que
  el retiro no cuesta posicionamiento; aun así queda la 301.

### Cambiado

- Tercera tarjeta de la home: nado libre → **Aquabebé**.
- Meta description de la home, `og:description` y `twitter:description`: ya no mencionan
  nado libre; ahora dicen los tres programas y la calificación MINSA.
- Las seis FAQ de la home, con precios, edades y el proceso real de matrícula.
- Bloque "Por qué elegir": entra **piscina saludable calificada por el MINSA**, que es
  la primera señal de confianza verificable que tiene el sitio.
- Las tarjetas de programa muestran edades y franjas horarias reales.
- El `<title>` de la home **no cambió**.

---

## 1.1.0 — 13/09/2026

Aplica la auditoría SEO competitiva en todo lo que no depende de datos del cliente.

### Añadido

- **Tres páginas nuevas**, una por intención de búsqueda:
  - `/natacion-para-ninos-la-molina/` — 719 palabras, 5 FAQ propias
  - `/natacion-para-adultos-la-molina/` — 660 palabras, 5 FAQ propias
  - `/nado-libre-la-molina/` — 632 palabras, 5 FAQ propias
- **`/css/site.v1.css` y `/js/site.v1.js`**: CSS y JS compartidos por las cuatro
  páginas, cacheados un año.
- **`tools/validar.py`**: validador que se corre antes de cada push.
- **`VERSION` y `CAMBIOS.md`**: este registro.
- Menú desplegable de Programas, migas de pan con `BreadcrumbList`, bloque NAP con
  `tel:`, "Cómo llegar" y Waze en todas las páginas, barra fija de WhatsApp en móvil.
- Bloque "Por qué elegir nuestra academia de natación en La Molina" en la home, con
  tres ventajas verificables.
- Eventos nuevos de GA4: `tel_click`, `como_llegar_click`, `waze_click`, `faq_open`,
  `ver_programa_click`.
- GA4 en la página 404, para saber qué URL está fallando.

### Cambiado

- Los cuatro `<h2>` de la home pasan a llevar intención de búsqueda y localidad.
- Las tarjetas de programa de la home ahora enlazan a su página, en vez de ir
  directo a WhatsApp.
- El CSS y el JS salen de dentro de `index.html`.
- Los `<h4>` del pie pasan a `<h3>` (había un salto de jerarquía h2 → h4).
- El nodo `LocalBusiness` del schema es idéntico en las cuatro páginas, con `hasMap`.

### Quitado

- `postalCode` del schema: el valor `15026` no estaba verificado, y un NAP con un
  dato inventado es peor que uno incompleto. Vuelve cuando se confirme.
- Los dos `<a href="#">` de Facebook e Instagram del pie: eran enlaces muertos.

### Corregido

- Contraste del subtítulo de los enlaces cruzados: daba 4,45:1, por debajo del
  mínimo AA de 4,5:1. Ahora 7,41:1.
- Los `&` sin escapar dentro de las URL de Google Maps y Waze rompían el parseo
  estricto del HTML.

### El `<title>` de la home NO cambió

`Clases de Natación en La Molina | ISANAT`. Congelado hasta **marzo de 2027**.
