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

/**
 * Reads an image file and re-encodes it at a smaller size/quality.
 * Phone photos can be several MB as base64, which quickly exceeds localStorage's
 * ~5MB quota — resizing keeps each image around 80–250KB so many can be stored.
 */
function resizeImageFile(file, maxDim = 1600, quality = 0.82) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(new Error('No se pudo leer el archivo'));
    reader.onload = () => {
      const img = new Image();
      img.onerror = () => reject(new Error('Archivo de imagen inválido'));
      img.onload = () => {
        let { width, height } = img;
        if (width > maxDim || height > maxDim) {
          const scale = maxDim / Math.max(width, height);
          width = Math.round(width * scale);
          height = Math.round(height * scale);
        }
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d').drawImage(img, 0, 0, width, height);
        resolve(canvas.toDataURL('image/jpeg', quality));
      };
      img.src = reader.result;
    };
    reader.readAsDataURL(file);
  });
}

async function handleFiles(fileList, collection, onChange) {
  const files = Array.from(fileList).filter((f) => f.type.startsWith('image/'));
  if (files.length === 0) return;
  toast(files.length > 1 ? 'Procesando imágenes…' : 'Procesando imagen…');
  try {
    const sources = await Promise.all(files.map((f) => resizeImageFile(f)));
    sources.forEach((src) => collection.inspiration.push({ id: uid('img'), src }));
    const ok = onChange();
    if (ok !== false) {
      toast(files.length > 1 ? `${files.length} imágenes agregadas` : 'Imagen agregada');
    }
  } catch (e) {
    console.error('Dantix: fallo al procesar imágenes', e);
    toast('No se pudieron procesar las imágenes. Intenta con fotos más pequeñas.');
  }
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
