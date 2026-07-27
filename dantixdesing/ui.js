// ui.js — small shared DOM helpers, toasts and modal utility

function qs(sel, root = document) {
  return root.querySelector(sel);
}
function qsa(sel, root = document) {
  return Array.from(root.querySelectorAll(sel));
}
function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === 'class') node.className = v;
    else if (k === 'html') node.innerHTML = v;
    else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  });
  (Array.isArray(children) ? children : [children]).forEach((c) => {
    if (c == null) return;
    node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
  });
  return node;
}
function escapeHtml(str = '') {
  return str.replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
}

let toastTimer = null;
function toast(message) {
  let host = qs('.toast-host');
  if (!host) {
    host = el('div', { class: 'toast-host' });
    document.body.appendChild(host);
  }
  host.innerHTML = '';
  const node = el('div', { class: 'toast' }, message);
  host.appendChild(node);
  requestAnimationFrame(() => node.classList.add('is-visible'));
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    node.classList.remove('is-visible');
    setTimeout(() => node.remove(), 250);
  }, 2600);
}

function openModal({ title, bodyNode, actions = [] }) {
  const overlay = el('div', { class: 'modal-overlay' });
  const modal = el('div', { class: 'modal' });
  const header = el('div', { class: 'modal-header' }, [
    el('h3', {}, title),
    el('button', { class: 'icon-btn', 'aria-label': 'Cerrar', onclick: () => close() }, '×'),
  ]);
  const body = el('div', { class: 'modal-body' }, bodyNode);
  const footer = el('div', { class: 'modal-footer' });
  actions.forEach((a) => {
    const btn = el('button', { class: a.primary ? 'btn btn-primary' : 'btn btn-ghost', onclick: () => a.onClick(close) }, a.label);
    footer.appendChild(btn);
  });
  modal.append(header, body, footer);
  overlay.appendChild(modal);
  overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
  document.body.appendChild(overlay);
  requestAnimationFrame(() => overlay.classList.add('is-visible'));
  function close() {
    overlay.classList.remove('is-visible');
    setTimeout(() => overlay.remove(), 200);
  }
  return { close };
}

export { qs, qsa, el, escapeHtml, toast, openModal };
