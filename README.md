# ISANAT — Escuela de Natación · La Molina, Lima

Sitio web estático (one-page) de ISANAT. Sin build, sin dependencias: son archivos
HTML, CSS y JS planos que se suben tal cual.

Dominio de producción: **https://isanat.pe**

---

## Estructura

```
.
├── index.html              Toda la landing (HTML + CSS inline + JS inline)
├── 404.html                Página de error, la sirve Cloudflare automáticamente
├── robots.txt              Permite indexación + apunta al sitemap
├── sitemap.xml             Una sola URL (one-page). Actualizar <lastmod> al cambiar contenido
├── site.webmanifest        Metadatos de PWA / icono al "agregar a inicio"
├── _headers                Cache de estáticos y headers de seguridad (Cloudflare Pages)
├── favicon.ico
├── fonts/
│   ├── poppins-400.woff2   Subsets latinos, 23 KB en total
│   ├── poppins-500.woff2
│   ├── poppins-700.woff2
│   └── LICENSE-Poppins.txt
└── img/
    ├── logo.webp           Logo con fondo transparente (nav y footer)
    ├── logo.png            Fallback PNG
    ├── logo-192.png        Iconos del manifest
    ├── logo-512.png
    ├── favicon-32.png
    ├── apple-touch-icon.png
    └── og-image.jpg        1200×630, la imagen que se ve al compartir el link
```

### Decisiones técnicas

- **Sin Tailwind CDN.** El CDN de Tailwind compila en el navegador (~400 KB de JS) y
  su propia documentación dice que no es para producción. El CSS está escrito a mano
  e inline dentro de `index.html`: ~14 KB, cero peticiones bloqueantes.
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
- [ ] Validar el HTML en [validator.w3.org](https://validator.w3.org/).
- [ ] Validar los schemas en [search.google.com/test/rich-results](https://search.google.com/test/rich-results).
- [ ] Medir en [PageSpeed Insights](https://pagespeed.web.dev/) — objetivo: >80 en móvil.

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

Valores que puede tomar `origen`: `header`, `menu_movil`, `hero`, `programa_ninos`,
`programa_adultos`, `programa_membresia`, `como_empezar`, `ubicacion`, `footer`, `flotante`.

### Día 1

- [ ] Verificar en **GA4 → Tiempo real** que los clics a WhatsApp aparecen.
- [ ] Verificar el sitio en **Search Console** y enviar `https://isanat.pe/sitemap.xml`.
- [ ] *Inspeccionar URL → Solicitar indexación* para la home.

### Semana 1-4 — Google Business Profile

Para un negocio local esto pesa más que cualquier optimización de código.

- [ ] Crear y **verificar por video** el perfil en [business.google.com](https://business.google.com).
- [ ] NAP idéntico carácter por carácter al del sitio y del schema:
      `ISANAT Escuela de Natación` / `Calle Hurón 409, Urb. Rinconada del Lago, La Molina, Lima, Perú` / `+51 992 705 564`
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
Cada punto está marcado con un comentario `TODO` en el HTML.

| # | Pendiente | Dónde se cambia |
|---|---|---|
| 1 | **Coordenadas GPS reales.** Las actuales son aproximadas de la zona Rinconada del Lago. Sacar las reales de la URL del perfil verificado en Google Maps (los números después de `!3d` y `!4d`). | `index.html`: meta `geo.position`, meta `ICBM` y `geo` dentro del schema |
| 2 | **Horarios de atención.** | Sección Ubicación + `openingHoursSpecification` en el schema (hoy no existe ese bloque, hay que agregarlo) |
| 3 | **Precios / planes.** Referencia de mercado en la zona: S/ 150 a S/ 580 según frecuencia y edad. | Sección Programas y FAQ "horarios y precios" |
| 4 | **Edad mínima** para clases de niños. | FAQ visible **y** bloque `FAQPage` del `<head>` |
| 5 | **Fotos reales** de la piscina y las clases. | Hero, tarjetas de programas y `og-image.jpg` |
| 6 | **URLs de Facebook e Instagram.** | Footer (`href="#"`) y array `sameAs` del schema |
| 7 | **Meta Pixel ID**, si se va a hacer Meta Ads. | `var PIXEL_ID = ''` en el `<head>` |
| 8 | **Proceso real de inscripción.** Los 3 pasos de "Cómo empezar" son una suposición razonable, hay que validarla. | Sección Cómo empezar + FAQ "¿Cómo reservo?" |
| 9 | **Propuesta de valor en una línea.** Quedó pendiente en la ficha del proyecto y es lo que debería ir en el hero. | `<h1>` y párrafo del hero |

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

---

## 7. Probar en local

No hace falta ningún build. Basta con levantar un servidor estático para que las rutas
absolutas (`/img/...`, `/fonts/...`) resuelvan bien:

```bash
python3 -m http.server 8000
# luego abrir http://localhost:8000
```

Abrir el `index.html` con doble clic también funciona, pero las rutas absolutas
fallan y no vas a ver el logo ni las fuentes.
