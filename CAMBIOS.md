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
| **1.2.1** | 13/09/2026 | *(anotar el hash tras el push)* | Los precios son **mensuales** y **no hay matrícula**: confirmado por el cliente |
| 1.2.0 | 13/09/2026 | *(no desplegada)* | Llegaron los datos del cliente: horarios, precios y edades reales. Sale nado libre, entran Aquabebé y horarios-y-precios |
| 1.1.0 | 13/09/2026 | *(anotar el hash tras el push)* | El sitio pasa de una página a cuatro |
| 1.0.1 | 13/09/2026 | `fb3d371` | Corrección del número de WhatsApp a +51 915 236 322 |
| 1.0.0 | 12/09/2026 | `6e879c3` | Publicación inicial (one-page) y salida de la configuración de Vercel |

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
