/* ISANAT — site.v1.js
   Un solo archivo para todas las páginas. Se cachea un año (ver _headers),
   así que al cambiarlo hay que subir el número de versión del NOMBRE del
   archivo (site.v2.js) y actualizar el <script src> de todas las páginas. */
(function () {
  'use strict';

  /* ---- Año del footer ---- */
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  /* ---- Menú móvil ---- */
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');

  function cerrarSubmenus() {
    var abiertos = document.querySelectorAll('.nav__group[open]');
    for (var i = 0; i < abiertos.length; i++) abiertos[i].removeAttribute('open');
  }

  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.getAttribute('data-open') === 'true';
      nav.setAttribute('data-open', String(!open));
      burger.setAttribute('aria-expanded', String(!open));
      burger.setAttribute('aria-label', !open ? 'Cerrar menú' : 'Abrir menú');
      if (open) cerrarSubmenus();
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.setAttribute('data-open', 'false');
        burger.setAttribute('aria-expanded', 'false');
        cerrarSubmenus();
      }
    });
  }

  /* ---- Desplegable "Programas": abre y cierra solo (<details>).
         Esto únicamente lo cierra al hacer clic fuera o con Escape. ---- */
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav__group')) cerrarSubmenus();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') cerrarSubmenus();
  });

  /* ---- Mapa bajo demanda: no descarga Google Maps hasta que se pide ---- */
  var mapBtn = document.getElementById('map-load');
  if (mapBtn) {
    mapBtn.addEventListener('click', function () {
      var box = document.getElementById('map');
      var f = document.createElement('iframe');
      f.src = 'https://www.google.com/maps?q=' +
        encodeURIComponent('Calle Hurón 409, Urb. Rinconada del Lago, La Molina, Lima, Perú') +
        '&z=16&output=embed';
      /* El titulo del iframe lo lee un lector de pantalla: tiene que ir en el
         idioma de la pagina, no siempre en espanol. Se toma de <html lang>. */
      var TITULO = {
        es: 'Mapa de la ubicación de ISANAT en La Molina',
        en: 'Map of the ISANAT location in La Molina, Lima',
        pt: 'Mapa da localização da ISANAT em La Molina, Lima'
      };
      var idi = (document.documentElement.lang || 'es').slice(0, 2).toLowerCase();
      f.title = TITULO[idi] || TITULO.es;
      f.loading = 'lazy';
      f.referrerPolicy = 'no-referrer-when-downgrade';
      f.setAttribute('allowfullscreen', '');
      box.innerHTML = '';
      box.appendChild(f);
    });
  }

  /* ---- Tracking de conversiones ----
     Un nombre de evento por acción + parámetro "origen" para segmentar.
     RECORDATORIO: en GA4 hay que marcar "whatsapp_click" como EVENTO CLAVE y
     crear la dimensión personalizada "origen" (ámbito Evento). Sin eso no se
     cuenta como conversión y los informes de origen salen vacíos.

     Eventos en uso: whatsapp_click · tel_click · como_llegar_click ·
     waze_click · maps_click · ver_programa_click · ver_programas_click ·
     faq_open                                                              */
  var CONVERSIONES = { whatsapp_click: 1, tel_click: 1 };

  function enviar(nombre, params) {
    if (typeof gtag !== 'undefined') gtag('event', nombre, params);
  }

  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-event]');
    if (!el) return;
    var name = el.getAttribute('data-event');
    var origen = el.getAttribute('data-origen') || 'general';

    enviar(name, {
      event_category: CONVERSIONES[name] ? 'conversion' : 'engagement',
      origen: origen
    });

    if (CONVERSIONES[name] && typeof fbq !== 'undefined') {
      fbq('track', 'Contact', { origen: origen });
      fbq('track', 'Lead', { origen: origen });
    }
  }, { passive: true });

  /* ---- Qué preguntas abre la gente: investigación de contenido gratis ---- */
  var faqs = document.querySelectorAll('.faq details');
  for (var i = 0; i < faqs.length; i++) {
    faqs[i].addEventListener('toggle', function () {
      if (!this.open) return;
      var s = this.querySelector('summary');
      enviar('faq_open', {
        event_category: 'engagement',
        origen: document.body.getAttribute('data-pagina') || 'general',
        pregunta: s ? s.textContent.trim().slice(0, 100) : ''
      });
    });
  }
})();
