// inspiration.js — inspiration board: upload, reorder, delete images

import { el, toast } from './ui.js';
import { uid } from './data.js';

let dragSrcId = null;

function renderInspiration(collection, onChange) {
  const grid = document.getElementById('inspiration-grid');
  const count = document.getElementById('inspiration-count');
  grid.innerHTML = '';
  count.textContent = `${collection.inspiration.length} imágenes`;

  if (collection.inspiration.length === 0) {
    grid.appendChild(el('div', { class: 'empty-state' }, [
      el('p', {}, 'Aún no hay imágenes de inspiración.'),
      el('p', { class: 'muted' }, 'Arrastra fotos aquí o usa "Agregar".'),
    ]));
  }

  collection.inspiration.forEach((img) => {
    const tile = el('div', {
      class: 'insp-tile',
      draggable: 'true',
      'data-id': img.id,
      ondragstart: (e) => {
        dragSrcId = img.id;
        e.dataTransfer.effectAllowed = 'move';
        tile.classList.add('is-dragging');
      },
      ondragend: () => tile.classList.remove('is-dragging'),
      ondragover: (e) => e.preventDefault(),
      ondrop: (e) => {
        e.preventDefault();
        if (!dragSrcId || dragSrcId === img.id) return;
        reorder(collection, dragSrcId, img.id);
        onChange();
      },
    }, [
      el('img', { src: img.src, alt: 'Referencia de inspiración', loading: 'lazy' }),
      el('button', {
        class: 'insp-remove',
        'aria-label': 'Eliminar imagen',
        onclick: () => {
          collection.inspiration = collection.inspiration.filter((i) => i.id !== img.id);
          onChange();
          toast('Imagen eliminada');
        },
      }, '×'),
    ]);
    grid.appendChild(tile);
  });

  // Drop zone on the grid container itself (for files dragged from the OS)
  grid.addEventListener('dragover', (e) => e.preventDefault());
  grid.addEventListener('drop', (e) => {
    e.preventDefault();
    if (e.dataTransfer.files?.length) {
      handleFiles(e.dataTransfer.files, collection, onChange);
    }
  });
}

function reorder(collection, srcId, targetId) {
  const list = collection.inspiration;
  const srcIdx = list.findIndex((i) => i.id === srcId);
  const targetIdx = list.findIndex((i) => i.id === targetId);
  if (srcIdx === -1 || targetIdx === -1) return;
  const [moved] = list.splice(srcIdx, 1);
  list.splice(targetIdx, 0, moved);
}

function handleFiles(fileList, collection, onChange) {
  const files = Array.from(fileList).filter((f) => f.type.startsWith('image/'));
  if (files.length === 0) return;
  let pending = files.length;
  files.forEach((file) => {
    const reader = new FileReader();
    reader.onload = () => {
      collection.inspiration.push({ id: uid('img'), src: reader.result });
      pending -= 1;
      if (pending === 0) {
        onChange();
        toast(files.length > 1 ? `${files.length} imágenes agregadas` : 'Imagen agregada');
      }
    };
    reader.readAsDataURL(file);
  });
}

function bindInspirationUpload(collectionRef, onChange) {
  const input = document.getElementById('inspiration-file-input');
  const addBtn = document.getElementById('add-inspiration-btn');
  addBtn.addEventListener('click', () => input.click());
  input.addEventListener('change', () => {
    if (input.files?.length) handleFiles(input.files, collectionRef(), onChange);
    input.value = '';
  });
}

export { renderInspiration, bindInspirationUpload };
