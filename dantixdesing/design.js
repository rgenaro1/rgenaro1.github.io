// design.js — ADN de la colección + Concepto actual (ficha técnica, vistas, favoritos)

import { el, toast, openModal, escapeHtml } from './ui.js';
import { uid } from './data.js';

function renderDNA(collection, onChange) {
  const principiosEl = document.getElementById('dna-principios');
  const personalidadEl = document.getElementById('dna-personalidad');
  const keywordsEl = document.getElementById('dna-keywords');

  principiosEl.innerHTML = '';
  collection.dna.principios.forEach((p) => {
    principiosEl.appendChild(el('li', { class: 'principio-item' }, [
      el('span', { class: 'check-icon' }, '✓'),
      el('span', {}, p),
    ]));
  });

  personalidadEl.innerHTML = '';
  collection.dna.personalidad.forEach((trait) => {
    const pct = Math.min(100, (trait.value / 10) * 100);
    personalidadEl.appendChild(el('div', { class: 'trait-row' }, [
      el('div', { class: 'trait-label' }, [
        el('span', {}, trait.label),
        el('span', { class: 'trait-value' }, trait.value.toFixed(1)),
      ]),
      el('div', { class: 'trait-bar' }, el('div', { class: 'trait-bar-fill', style: `width:${pct}%` })),
    ]));
  });

  keywordsEl.innerHTML = '';
  collection.dna.keywords.forEach((kw) => {
    keywordsEl.appendChild(el('span', { class: 'chip' }, kw));
  });

  document.getElementById('edit-dna-btn').onclick = () => openDnaEditor(collection, onChange);
}

function openDnaEditor(collection, onChange) {
  const body = el('div', { class: 'dna-editor' });
  const traitsWrap = el('div', {}, []);
  collection.dna.personalidad.forEach((trait, idx) => {
    const row = el('label', { class: 'field-row' }, [
      el('span', {}, trait.label),
      el('input', {
        type: 'range', min: '0', max: '10', step: '0.1', value: trait.value,
        oninput: (e) => { collection.dna.personalidad[idx].value = parseFloat(e.target.value); valOut.textContent = e.target.value; },
      }),
    ]);
    const valOut = el('span', { class: 'muted' }, trait.value.toFixed(1));
    row.appendChild(valOut);
    traitsWrap.appendChild(row);
  });

  const keywordsInput = el('input', {
    type: 'text', class: 'text-input', value: collection.dna.keywords.join(', '),
    placeholder: 'minimal, timeless, premium…',
  });

  body.append(
    el('p', { class: 'muted' }, 'Personalidad de la colección'),
    traitsWrap,
    el('p', { class: 'muted', style: 'margin-top:16px' }, 'Palabras clave (separadas por coma)'),
    keywordsInput,
  );

  openModal({
    title: 'Editar ADN de la colección',
    bodyNode: body,
    actions: [
      { label: 'Cancelar', onClick: (close) => close() },
      {
        label: 'Guardar cambios', primary: true,
        onClick: (close) => {
          collection.dna.keywords = keywordsInput.value.split(',').map((k) => k.trim()).filter(Boolean);
          onChange();
          toast('ADN actualizado');
          close();
        },
      },
    ],
  });
}

function getConcept(collection) {
  return collection.concepts.find((c) => c.id === collection.selectedConceptId) || collection.concepts[0];
}

function renderConcept(collection, onChange) {
  const concept = getConcept(collection);
  const view = collection.activeView;

  document.getElementById('concept-main-image').src = concept.views[view];
  document.getElementById('concept-fav-btn').classList.toggle('is-active', concept.favorite);
  document.getElementById('concept-label').textContent = `Concepto ${concept.code}`;

  // view tabs
  document.querySelectorAll('.view-tab').forEach((btn) => {
    btn.classList.toggle('is-active', btn.dataset.view === view);
    btn.onclick = () => { collection.activeView = btn.dataset.view; onChange(); };
  });

  // concept thumbnails (A/B/C/D)
  const thumbsEl = document.getElementById('concept-thumbs');
  thumbsEl.innerHTML = '';
  collection.concepts.forEach((c) => {
    const thumb = el('button', {
      class: `concept-thumb${c.id === concept.id ? ' is-active' : ''}`,
      onclick: () => { collection.selectedConceptId = c.id; onChange(); },
    }, [
      el('img', { src: c.views.lateral, alt: `Concepto ${c.code}` }),
      el('span', {}, c.code),
    ]);
    thumbsEl.appendChild(thumb);
  });

  // ficha técnica
  const f = concept.ficha;
  document.getElementById('ficha-dificultad').innerHTML = renderDifficultyDots(f.dificultad);
  document.getElementById('ficha-piezas').textContent = f.piezas;
  document.getElementById('ficha-construccion').textContent = f.construccion;
  document.getElementById('ficha-tipo-suela').textContent = f.tipoSuela;
  document.getElementById('ficha-material-principal').textContent = f.materialPrincipal;
  document.getElementById('ficha-material-secundario').textContent = f.materialSecundario;
  document.getElementById('ficha-costo').textContent = f.costoEstimado;

  document.getElementById('concept-fav-btn').onclick = () => {
    concept.favorite = !concept.favorite;
    onChange();
  };
  document.getElementById('duplicate-concept-btn').onclick = () => duplicateConcept(collection, onChange);
  document.getElementById('compare-concept-btn').onclick = () => openCompareModal(collection);
  document.getElementById('more-actions-btn').onclick = (e) => openMoreMenu(e, collection, onChange);
}

function renderDifficultyDots(level) {
  return Array.from({ length: 5 }, (_, i) => `<span class="dot${i < level ? ' is-filled' : ''}"></span>`).join('');
}

function duplicateConcept(collection, onChange) {
  const source = getConcept(collection);
  const usedCodes = collection.concepts.map((c) => c.code);
  const nextCode = 'ABCDEFGH'.split('').find((c) => !usedCodes.includes(c)) || `${usedCodes.length + 1}`;
  const copy = JSON.parse(JSON.stringify(source));
  copy.id = uid('concept');
  copy.code = nextCode;
  copy.favorite = false;
  collection.concepts.push(copy);
  collection.selectedConceptId = copy.id;
  onChange();
  toast(`Concepto ${nextCode} creado a partir de ${source.code}`);
}

function openCompareModal(collection) {
  const a = collection.concepts[0];
  const b = collection.concepts[1] || collection.concepts[0];
  const body = el('div', { class: 'compare-grid' }, [
    conceptCompareCard(a), conceptCompareCard(b),
  ]);
  openModal({ title: 'Comparar conceptos', bodyNode: body, actions: [{ label: 'Cerrar', primary: true, onClick: (c) => c() }] });
}

function conceptCompareCard(concept) {
  return el('div', { class: 'compare-card' }, [
    el('img', { src: concept.views.lateral, alt: `Concepto ${concept.code}` }),
    el('h4', {}, `Concepto ${concept.code}`),
    el('ul', { class: 'compare-list' }, [
      el('li', {}, `Piezas: ${concept.ficha.piezas}`),
      el('li', {}, `Construcción: ${concept.ficha.construccion}`),
      el('li', {}, `Suela: ${concept.ficha.tipoSuela}`),
      el('li', {}, `Material: ${concept.ficha.materialPrincipal}`),
      el('li', {}, `Costo estimado: ${concept.ficha.costoEstimado}`),
    ]),
  ]);
}

function openMoreMenu(evt, collection, onChange) {
  const body = el('div', { class: 'menu-list' }, [
    el('button', {
      class: 'menu-item',
      onclick: (e) => {
        const concept = getConcept(collection);
        if (collection.concepts.length <= 1) { toast('Debe existir al menos un concepto'); return; }
        collection.concepts = collection.concepts.filter((c) => c.id !== concept.id);
        collection.selectedConceptId = collection.concepts[0].id;
        onChange();
        toast(`Concepto ${concept.code} eliminado`);
        modalHandle.close();
      },
    }, 'Eliminar concepto'),
  ]);
  const modalHandle = openModal({ title: 'Más acciones', bodyNode: body, actions: [{ label: 'Cerrar', onClick: (c) => c() }] });
}

export { renderDNA, renderConcept, getConcept };
