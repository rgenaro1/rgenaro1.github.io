/**
 * utils.js — Helpers puros de UI, sin lógica de negocio ni llamadas de red
 * (eso vive en api.js).
 */
window.DantixUtils = (function () {

  function debounce(fn, wait) {
    var t;
    return function () {
      var args = arguments, ctx = this;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(ctx, args); }, wait);
    };
  }

  function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function statusClass(estado) {
    var n = String(estado || '').toLowerCase();
    if (n.indexOf('aprob') !== -1) return 'status-aprobado';
    if (n.indexOf('revis') !== -1) return 'status-revision';
    if (n.indexOf('desarroll') !== -1) return 'status-desarrollo';
    return '';
  }

  function formatDate(val) {
    if (!val) return '—';
    try {
      var d = new Date(val);
      if (isNaN(d.getTime())) return String(val);
      return d.toLocaleDateString('es-PE', { day: '2-digit', month: '2-digit', year: 'numeric' });
    } catch (e) { return String(val); }
  }

  var toastEl;
  function toast(msg, ms) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'toast';
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(function () { toastEl.classList.remove('show'); }, ms || 2400);
  }

  function applyTheme(mode) {
    var root = document.documentElement;
    var effective = mode;
    if (mode === 'auto') {
      effective = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    root.setAttribute('data-theme', effective);
  }

  function getStoredTheme() {
    try {
      return localStorage.getItem(window.DantixConfig.theme.storageKey) || window.DantixConfig.theme.default;
    } catch (e) { return window.DantixConfig.theme.default; }
  }

  function setStoredTheme(mode) {
    try { localStorage.setItem(window.DantixConfig.theme.storageKey, mode); } catch (e) {}
  }

  function downloadBase64(base64, filename, mimeType) {
    var link = document.createElement('a');
    link.href = 'data:' + mimeType + ';base64,' + base64;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  function qrImageUrl(text, size) {
    var s = size || 220;
    return 'https://api.qrserver.com/v1/create-qr-code/?size=' + s + 'x' + s + '&data=' + encodeURIComponent(text);
  }

  return {
    debounce: debounce,
    escapeHtml: escapeHtml,
    statusClass: statusClass,
    formatDate: formatDate,
    toast: toast,
    applyTheme: applyTheme,
    getStoredTheme: getStoredTheme,
    setStoredTheme: setStoredTheme,
    downloadBase64: downloadBase64,
    qrImageUrl: qrImageUrl
  };
})();
