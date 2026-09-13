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
| **1.1.0** | 13/09/2026 | *(anotar el hash tras el push)* | El sitio pasa de una página a cuatro |
| 1.0.1 | 13/09/2026 | `fb3d371` | Corrección del número de WhatsApp a +51 915 236 322 |
| 1.0.0 | 12/09/2026 | `6e879c3` | Publicación inicial (one-page) y salida de la configuración de Vercel |

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
