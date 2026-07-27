// app.js — bootstraps the app, owns the render loop, wires every module together

import { Store, uid } from './data.js';
import { el, toast, escapeHtml } from './ui.js';
import { renderInspiration, bindInspirationUpload } from './inspiration.js';
import { renderDNA, renderConcept, getConcept } from './design.js';
import { renderChat, bindChat, sendMessage } from './chat.js';

let collections = Store.load();
let currentId = Store.getCurrentId(collections);

function current() {
  return collections.find((c) => c.id === currentId) || collections[0];
}

function persist() {
  Store.saveAll(collections);
}

function renderAll() {
  const col = current();
  persist();
  renderSidebarCollections();
  renderHeader(col);
  renderInspiration(col, renderAll);
  renderDNA(col, renderAll);
  renderConcept(col, renderAll);
  renderChat(col);
}

// ---------- Sidebar: collections list ----------
function renderSidebarCollections() {
  const host = document.getElementById('collections-list');
  host.innerHTML = '';
  collections.forEach((col) => {
    const item = el('button', {
      class: `collection-item${col.id === currentId ? ' is-active' : ''}`,
      onclick: () => { currentId = col.id; Store.setCurrentId(col.id); renderAll(); },
    }, [
      el('span', { class: 'collection-dot' }),
      el('span', { class: 'collection-name' }, col.name),
    ]);
    host.appendChild(item);
  });
}

// ---------- Header: title + meta fields ----------
function renderHeader(col) {
  const titleEl = document.getElementById('collection-title');
  titleEl.textContent = col.name;

  const metaRow = document.getElementById('meta-row');
  metaRow.innerHTML = '';
  const fields = [
    ['marca', 'Marca'], ['mercado', 'Mercado'], ['precio', 'Precio objetivo'],
    ['publico', 'Público'], ['temporada', 'Temporada'],
  ];
  fields.forEach(([key, label]) => {
    const valueEl = el('span', {
      class: 'meta-value', contenteditable: 'true', spellcheck: 'false',
      onblur: (e) => {
        col.meta[key] = e.target.textContent.trim() || col.meta[key];
        persist();
      },
      onkeydown: (e) => { if (e.key === 'Enter') { e.preventDefault(); e.target.blur(); } },
    }, col.meta[key]);
    metaRow.appendChild(el('div', { class: 'meta-field' }, [
      el('span', { class: 'meta-label' }, label),
      valueEl,
    ]));
  });
}

function bindTitleEditing() {
  const titleEl = document.getElementById('collection-title');
  const editBtn = document.getElementById('edit-title-btn');
  editBtn.addEventListener('click', () => {
    titleEl.contentEditable = 'true';
    titleEl.focus();
    document.getSelection().selectAllChildren(titleEl);
  });
  titleEl.addEventListener('blur', () => {
    titleEl.contentEditable = 'false';
    const newName = titleEl.textContent.trim();
    if (newName) { current().name = newName; persist(); renderSidebarCollections(); }
    else titleEl.textContent = current().name;
  });
  titleEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); titleEl.blur(); }
  });
}

// ---------- New collection ----------
function bindNewCollection() {
  document.getElementById('new-collection-btn').addEventListener('click', () => {
    const name = window.prompt('Nombre de la nueva colección', 'Nueva colección');
    if (name === null) return;
    const col = Store.newCollection(name);
    collections.push(col);
    currentId = col.id;
    Store.setCurrentId(col.id);
    renderAll();
    toast(`"${col.name}" creada`);
  });
}

// ---------- Export JSON ----------
function bindExport() {
  const doExport = () => {
    const col = current();
    const blob = new Blob([JSON.stringify(col, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${col.name.replace(/\s+/g, '-').toLowerCase()}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    toast('Colección exportada como JSON');
  };
  document.getElementById('export-json-btn').addEventListener('click', doExport);
  document.getElementById('export-nav-btn').addEventListener('click', doExport);
}

function bindShare() {
  document.getElementById('share-btn').addEventListener('click', () => {
    toast('Enlace de colaboración copiado (simulado)');
  });
}

// ---------- Refinar con IA ----------
function bindRefineAI() {
  document.getElementById('refine-ai-btn').addEventListener('click', () => {
    const col = current();
    const concept = getConcept(col);
    // small, visible tweak so the action feels consequential
    concept.ficha.dificultad = Math.max(1, Math.min(5, concept.ficha.dificultad));
    sendMessage(col, `Refina el Concepto ${concept.code}: equilibra proporciones y simplifica costuras.`, renderAll);
  });
}

// ---------- Sidebar nav: scroll to section ----------
function bindSidebarNav() {
  document.querySelectorAll('.nav-item[data-target]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetId = btn.dataset.target;
      document.querySelectorAll('.nav-item').forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      if (!targetId) return;
      const targetEl = document.getElementById(targetId);
      targetEl?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
}

// ---------- Theme toggle (prepared, not activated) ----------
function bindThemeToggle() {
  document.getElementById('theme-toggle-btn').addEventListener('click', () => {
    toast('Modo oscuro disponible próximamente');
  });
}

// ---------- Boot ----------
function boot() {
  bindTitleEditing();
  bindNewCollection();
  bindExport();
  bindShare();
  bindRefineAI();
  bindSidebarNav();
  bindThemeToggle();
  bindInspirationUpload(() => current(), renderAll);
  bindChat(() => current(), renderAll);
  document.getElementById('view-all-inspiration-btn').addEventListener('click', () => toast('Vista completa de inspiración — próximamente'));
  renderAll();
}

document.addEventListener('DOMContentLoaded', boot);
