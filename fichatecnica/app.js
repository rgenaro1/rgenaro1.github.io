/**
 * app.js — Orquesta la UI: búsqueda/autocompletado, render de la ficha en
 * tarjetas, lightbox de imágenes y acciones (PDF, imprimir, compartir, QR,
 * pantalla completa, tema).
 */
(function () {
  var U = window.DantixUtils;
  var Api = window.DantixApi;

  var els = {};
  var state = {
    results: [],
    highlighted: -1,
    currentFicha: null,
    currentCodigo: null
  };

  document.addEventListener('DOMContentLoaded', init);

  function init() {
    cacheEls();
    U.applyTheme(U.getStoredTheme());
    bindEvents();
    var params = new URLSearchParams(window.location.search);
    var codigoParam = params.get('codigo');
    if (codigoParam) {
      els.searchInput.value = codigoParam;
      loadFicha(codigoParam);
    }
  }

  function cacheEls() {
    els.searchInput = document.getElementById('searchInput');
    els.searchBtn = document.getElementById('searchBtn');
    els.autocomplete = document.getElementById('autocomplete');
    els.results = document.getElementById('results');
    els.themeBtn = document.getElementById('themeBtn');
    els.lightbox = document.getElementById('lightbox');
    els.lightboxImg = document.getElementById('lightboxImg');
    els.lightboxClose = document.getElementById('lightboxClose');
    els.fullscreenBtn = document.getElementById('fullscreenBtn');
  }

  function bindEvents() {
    els.searchInput.addEventListener('input', U.debounce(onSearchInput, window.DantixConfig.searchDebounceMs));
    els.searchInput.addEventListener('keydown', onSearchKeydown);
    els.searchBtn.addEventListener('click', function () { loadFicha(els.searchInput.value); });
    document.addEventListener('click', function (e) {
      if (!els.autocomplete.contains(e.target) && e.target !== els.searchInput) {
        closeAutocomplete();
      }
    });
    els.themeBtn.addEventListener('click', cycleTheme);
    els.lightboxClose.addEventListener('click', closeLightbox);
    els.lightbox.addEventListener('click', function (e) { if (e.target === els.lightbox) closeLightbox(); });
    els.fullscreenBtn.addEventListener('click', toggleFullscreen);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLightbox(); });
  }

  // ---------------------------------------------------------------
  // Búsqueda / autocompletado
  // ---------------------------------------------------------------
  function onSearchInput() {
    var q = els.searchInput.value.trim();
    if (q.length < window.DantixConfig.minCharsForAutocomplete) { closeAutocomplete(); return; }
    Api.searchProducts(q).then(function (results) {
      state.results = results || [];
      state.highlighted = -1;
      renderAutocomplete();
    }).catch(function (err) {
      console.error(err);
    });
  }

  function onSearchKeydown(e) {
    if (!els.autocomplete.classList.contains('open')) {
      if (e.key === 'Enter') loadFicha(els.searchInput.value);
      return;
    }
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      state.highlighted = Math.min(state.highlighted + 1, state.results.length - 1);
      renderAutocomplete();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      state.highlighted = Math.max(state.highlighted - 1, 0);
      renderAutocomplete();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      var pick = state.highlighted > -1 ? state.results[state.highlighted] : null;
      loadFicha(pick ? pick.codigo : els.searchInput.value);
    } else if (e.key === 'Escape') {
      closeAutocomplete();
    }
  }

  function renderAutocomplete() {
    if (!state.results.length) { closeAutocomplete(); return; }
    els.autocomplete.innerHTML = state.results.map(function (r, i) {
      var hl = i === state.highlighted ? ' highlighted' : '';
      return '' +
        '<div class="ac-item' + hl + '" data-codigo="' + U.escapeHtml(r.codigo) + '">' +
          '<div class="ac-main">' +
            '<span class="ac-code">' + U.escapeHtml(r.codigo) + '</span> — ' +
            U.escapeHtml(r.modelo) + ' ' + U.escapeHtml(r.color) +
            '<div class="ac-sub">' + U.escapeHtml(r.categoria || '') + '</div>' +
          '</div>' +
          (r.estado ? '<span class="ac-badge">' + U.escapeHtml(r.estado) + '</span>' : '') +
        '</div>';
    }).join('');
    Array.prototype.forEach.call(els.autocomplete.querySelectorAll('.ac-item'), function (el) {
      el.addEventListener('click', function () { loadFicha(el.getAttribute('data-codigo')); });
    });
    els.autocomplete.classList.add('open');
  }

  function closeAutocomplete() {
    els.autocomplete.classList.remove('open');
  }

  // ---------------------------------------------------------------
  // Carga y render de ficha
  // ---------------------------------------------------------------
  function loadFicha(codigo) {
    codigo = (codigo || '').trim();
    if (!codigo) return;
    closeAutocomplete();
    els.searchInput.value = codigo;
    renderLoading();
    Api.getFicha(codigo).then(function (ficha) {
      state.currentFicha = ficha;
      state.currentCodigo = codigo;
      renderFicha(ficha);
      history.replaceState(null, '', '?codigo=' + encodeURIComponent(codigo));
    }).catch(function (err) {
      renderError(err && err.message ? err.message : String(err));
    });
  }

  function renderLoading() {
    els.results.innerHTML =
      '<div class="loading-state"><div class="loading-spinner"></div>Cargando ficha técnica…</div>';
  }

  function renderError(msg) {
    els.results.innerHTML =
      '<div class="empty-state">No se pudo cargar la ficha.<br><small>' + U.escapeHtml(msg) + '</small></div>';
  }

  function renderFicha(f) {
    var g = f.general || {};
    var statusCls = U.statusClass(g.estado);

    var html = '';

    // ---- Tarjeta 1: hero ----
    html += '<div class="card hero-card">';
    html += '<div class="hero-image" data-full="' + (f.imagenPrincipal || '') + '">' +
      (f.imagenPrincipal ? '<img src="' + f.imagenPrincipal + '" alt="' + U.escapeHtml(f.codigo) + '">' : imgPlaceholder()) +
      '</div>';
    html += '<div class="hero-meta">';
    html += '<h2>' + U.escapeHtml(g.modelo || '') + ' ' + U.escapeHtml(g.color || '') + '</h2>';
    html += '<div class="hero-code">' + U.escapeHtml(f.codigo) + '</div>';
    html += '<div class="meta-grid">';
    html += metaItem('Línea', g.categoria);
    html += metaItem('Temporada', g.temporada);
    html += metaItem('Cliente', g.cliente);
    html += metaItem('Tallas', g.tallas);
    html += metaItem('Versión', g.version);
    html += '<div class="meta-item"><div class="meta-label">Estado</div><div class="meta-value">' +
      '<span class="status-pill ' + statusCls + '">' + U.escapeHtml(g.estado || '—') + '</span></div></div>';
    html += '</div></div></div>';

    // ---- Tarjeta 2: información general ----
    html += '<div class="card">' +
      '<div class="card-title">Información general</div>' +
      '<div class="meta-grid">' +
        metaItem('Autor', g.autor) +
        metaItem('Última actualización', U.formatDate(g.ultimaactualizacion)) +
      '</div>' +
      (g.descripcion ? '<p class="desc-text" style="margin-top:14px;">' + U.escapeHtml(g.descripcion) + '</p>' : '') +
    '</div>';

    // ---- Tarjeta 3: BOM ----
    html += '<div class="card"><div class="card-title">BOM de materiales</div>';
    if (f.bom && f.bom.length) {
      html += '<div style="overflow-x:auto"><table class="data-table"><thead><tr>' +
        '<th>Componente</th><th>Material</th><th>Cant.</th><th>Unidad</th><th>Etapa</th><th>Zona</th><th>Obs.</th>' +
        '</tr></thead><tbody>';
      f.bom.forEach(function (row) {
        html += '<tr>' +
          '<td>' + U.escapeHtml(row.componente) + '</td>' +
          '<td>' + U.escapeHtml(row.material) + '</td>' +
          '<td>' + U.escapeHtml(row.cantidad) + '</td>' +
          '<td>' + U.escapeHtml(row.unidad) + '</td>' +
          '<td>' + U.escapeHtml(row.etapa) + '</td>' +
          '<td>' + U.escapeHtml(row.zona) + '</td>' +
          '<td>' + U.escapeHtml(row.descripcion) + '</td>' +
        '</tr>';
      });
      html += '</tbody></table></div>';
    } else {
      html += '<p class="desc-text">Sin materiales registrados.</p>';
    }
    html += '</div>';

    // ---- Tarjeta 4: imágenes ----
    var allImgs = [];
    if (f.imagenPrincipal) allImgs.push(f.imagenPrincipal);
    if (f.imagenes && f.imagenes.detalle) allImgs = allImgs.concat(f.imagenes.detalle);
    html += '<div class="card"><div class="card-title">Imágenes</div>';
    if (allImgs.length) {
      html += '<div class="gallery">' + allImgs.map(function (src) {
        return '<img src="' + src + '" data-full="' + src + '" class="gallery-img">';
      }).join('') + '</div>';
    } else {
      html += '<p class="desc-text">No se encontraron imágenes en esta ficha.</p>';
    }
    html += '</div>';

    // ---- Tarjeta 5: instrucciones ----
    html += '<div class="card"><div class="card-title">Instrucciones</div>';
    var stages = f.instrucciones || {};
    var stageOrder = ['CORTE', 'APARADO', 'ARMADO', 'ALISTADO'];
    var anyStage = false;
    stageOrder.forEach(function (s) {
      var block = stages[s];
      if (!block || (!block.pasos.length && !block.imagenes.length)) return;
      anyStage = true;
      html += '<div class="stage-block"><div class="stage-name">' + U.escapeHtml(s) + '</div>';
      if (block.pasos.length) {
        html += '<ul class="stage-steps">' + block.pasos.map(function (p) { return '<li>' + U.escapeHtml(p) + '</li>'; }).join('') + '</ul>';
      }
      if (block.imagenes.length) {
        html += '<div class="stage-images">' + block.imagenes.map(function (src) {
          return '<img src="' + src + '" data-full="' + src + '" class="gallery-img">';
        }).join('') + '</div>';
      }
      html += '</div>';
    });
    if (!anyStage) html += '<p class="desc-text">Sin instrucciones registradas.</p>';
    html += '</div>';

    // ---- Tarjeta 6: historial ----
    html += '<div class="card"><div class="card-title">Historial de versiones</div>';
    if (f.historial && f.historial.length) {
      html += '<table class="data-table"><thead><tr><th>Versión</th><th>Fecha</th><th>Autor</th><th>Cambio</th></tr></thead><tbody>';
      f.historial.forEach(function (h) {
        html += '<tr><td>' + U.escapeHtml(h.version) + '</td><td>' + U.formatDate(h.fecha) + '</td>' +
          '<td>' + U.escapeHtml(h.autor) + '</td><td>' + U.escapeHtml(h.cambio) + '</td></tr>';
      });
      html += '</tbody></table>';
    } else {
      html += '<p class="desc-text">Sin historial registrado.</p>';
    }
    html += '</div>';

    // ---- Acciones ----
    html += '<div class="action-bar">' +
      actionBtn('pdfBtn', 'Descargar PDF') +
      actionBtn('printBtn', 'Imprimir') +
      actionBtn('shareBtn', 'Compartir enlace') +
      actionBtn('qrBtn', 'Abrir por QR') +
    '</div>';

    els.results.innerHTML = html;
    bindResultEvents();
  }

  function metaItem(label, value) {
    return '<div class="meta-item"><div class="meta-label">' + U.escapeHtml(label) + '</div>' +
      '<div class="meta-value">' + (value ? U.escapeHtml(value) : '—') + '</div></div>';
  }

  function actionBtn(id, label) {
    return '<button class="action-btn" id="' + id + '">' + U.escapeHtml(label) + '</button>';
  }

  function imgPlaceholder() {
    return '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color:var(--text-muted)">' +
      '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>';
  }

  function bindResultEvents() {
    Array.prototype.forEach.call(document.querySelectorAll('.gallery-img'), function (img) {
      img.addEventListener('click', function () { openLightbox(img.getAttribute('data-full') || img.src); });
    });
    var heroImg = document.querySelector('.hero-image');
    if (heroImg && heroImg.getAttribute('data-full')) {
      heroImg.addEventListener('click', function () { openLightbox(heroImg.getAttribute('data-full')); });
    }

    var pdfBtn = document.getElementById('pdfBtn');
    if (pdfBtn) pdfBtn.addEventListener('click', downloadPdf);
    var printBtn = document.getElementById('printBtn');
    if (printBtn) printBtn.addEventListener('click', function () { window.print(); });
    var shareBtn = document.getElementById('shareBtn');
    if (shareBtn) shareBtn.addEventListener('click', shareLink);
    var qrBtn = document.getElementById('qrBtn');
    if (qrBtn) qrBtn.addEventListener('click', showQr);
  }

  // ---------------------------------------------------------------
  // Acciones
  // ---------------------------------------------------------------
  function downloadPdf() {
    U.toast('Generando PDF…');
    var styleTag = document.querySelector('link[rel="stylesheet"]')
      ? '<link rel="stylesheet" href="' + document.querySelector('link[rel="stylesheet"][href*="styles.css"]').href + '">'
      : '';
    var content = '<!doctype html><html><head><meta charset="utf-8">' + styleTag + '</head>' +
      '<body data-theme="light"><div style="max-width:900px;margin:0 auto;">' + els.results.innerHTML + '</div></body></html>';
    Api.generarPdfDesdeHtml(content, state.currentCodigo).then(function (res) {
      U.downloadBase64(res.base64, res.filename, res.mimeType);
      U.toast('PDF descargado');
    }).catch(function (err) {
      console.error(err);
      U.toast('No se pudo generar el PDF');
    });
  }

  function shareLink() {
    var url = window.location.origin + window.location.pathname + '?codigo=' + encodeURIComponent(state.currentCodigo);
    if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(function () { U.toast('Enlace copiado al portapapeles'); });
    } else {
      window.prompt('Copia el enlace:', url);
    }
  }

  function showQr() {
    var url = window.location.origin + window.location.pathname + '?codigo=' + encodeURIComponent(state.currentCodigo);
    openLightbox(U.qrImageUrl(url, 280));
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(function () {});
    } else {
      document.exitFullscreen();
    }
  }

  function cycleTheme() {
    var order = ['light', 'dark', 'auto'];
    var current = U.getStoredTheme();
    var next = order[(order.indexOf(current) + 1) % order.length];
    U.setStoredTheme(next);
    U.applyTheme(next);
    U.toast('Tema: ' + next);
  }

  // ---------------------------------------------------------------
  // Lightbox
  // ---------------------------------------------------------------
  function openLightbox(src) {
    if (!src) return;
    els.lightboxImg.src = src;
    els.lightbox.classList.add('open');
  }
  function closeLightbox() {
    els.lightbox.classList.remove('open');
    els.lightboxImg.src = '';
  }
})();
