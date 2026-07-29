/**
 * api.js — Única capa que sabe que el backend es un Apps Script Web App
 * expuesto como API JSON. Si algún día migras a otro backend (Node,
 * PostgreSQL con un endpoint REST propio, etc.), SOLO este archivo cambia;
 * app.js sigue llamando a DantixApi.searchProducts() / DantixApi.getFicha()
 * exactamente igual.
 */
window.DantixApi = (function () {

  function baseUrl() {
    var url = window.DantixConfig.appsScriptUrl;
    if (!url || url.indexOf('PEGA_AQUI_TU_DEPLOYMENT_ID') !== -1) {
      throw new Error('Falta configurar appsScriptUrl en config.js con tu URL de deployment.');
    }
    return url;
  }

  function buildGetUrl(params) {
    var qs = Object.keys(params)
      .filter(function (k) { return params[k] !== undefined && params[k] !== null; })
      .map(function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(params[k]); })
      .join('&');
    return baseUrl() + '?' + qs;
  }

  function unwrap(json) {
    if (!json || json.ok !== true) {
      throw new Error((json && json.error) || 'Respuesta inválida del servidor.');
    }
    return json.data;
  }

  function get(params) {
    return fetch(buildGetUrl(params))
      .then(function (r) { return r.json(); })
      .then(unwrap);
  }

  function post(params) {
    var body = Object.keys(params)
      .map(function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(params[k]); })
      .join('&');
    return fetch(baseUrl(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body
    })
      .then(function (r) { return r.json(); })
      .then(unwrap);
  }

  function searchProducts(query) {
    return get({ action: 'search', q: query });
  }

  function getFicha(codigo) {
    return get({ action: 'ficha', codigo: codigo });
  }

  function generarPdfDesdeHtml(html, filename) {
    return post({ action: 'pdf', html: html, filename: filename });
  }

  function ping() {
    return get({ action: 'ping' });
  }

  return {
    searchProducts: searchProducts,
    getFicha: getFicha,
    generarPdfDesdeHtml: generarPdfDesdeHtml,
    ping: ping
  };
})();
