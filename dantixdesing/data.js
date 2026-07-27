// data.js — persistence layer and seed content for Dantix Design Studio
// No backend: everything lives in localStorage under a single namespaced key.

const STORAGE_KEY = 'dantix.collections.v1';
const CURRENT_KEY = 'dantix.currentId.v1';

function uid(prefix = 'id') {
  return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`;
}

/**
 * Generates an elegant abstract shoe-silhouette placeholder as an inline SVG.
 * Tint varies slightly per seed so a grid of placeholders doesn't feel identical.
 */
function placeholderImage(seed = 0, label = '') {
  const hueShift = (seed * 37) % 18 - 9;
  const base = 42 + hueShift; // muted sand tone
  const fill = `hsl(${34 + hueShift}, ${18}%, ${86 - (seed % 3) * 3}%)`;
  const line = `hsl(${34 + hueShift}, 20%, 40%)`;
  const svg = `
  <svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
    <rect width="480" height="360" fill="${fill}"/>
    <g fill="none" stroke="${line}" stroke-width="1.4" opacity="0.55">
      <path d="M70 230 C 140 190, 210 190, 260 205 C 320 222, 360 200, 410 215 C 420 235, 415 255, 390 260 L 100 260 C 78 260, 66 248, 70 230 Z"/>
      <path d="M150 205 C 175 185, 205 178, 230 188"/>
      <line x1="120" y1="248" x2="120" y2="230"/>
      <line x1="150" y1="252" x2="150" y2="232"/>
      <line x1="180" y1="254" x2="180" y2="234"/>
    </g>
    <text x="24" y="336" font-family="Inter, sans-serif" font-size="12" letter-spacing="2" fill="${line}" opacity="0.7">${label.toUpperCase()}</text>
  </svg>`;
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
}

function defaultConcept(code, overrides = {}) {
  return Object.assign({
    id: uid('concept'),
    code,
    favorite: code === 'A',
    views: {
      lateral: placeholderImage(code.charCodeAt(0), `Vista lateral ${code}`),
      frontal: placeholderImage(code.charCodeAt(0) + 1, `Vista frontal ${code}`),
      posterior: placeholderImage(code.charCodeAt(0) + 2, `Vista posterior ${code}`),
      superior: placeholderImage(code.charCodeAt(0) + 3, `Vista superior ${code}`),
    },
    ficha: {
      dificultad: 3,
      piezas: 11,
      construccion: 'Strobel',
      materialPrincipal: 'Cuero floater',
      materialSecundario: 'Gamuza',
      tipoSuela: 'Cupsole',
      costoEstimado: 'Medio',
    },
  }, overrides);
}

function seedCollection() {
  return {
    id: uid('col'),
    name: 'Colección Primavera 2027',
    createdAt: Date.now(),
    meta: {
      marca: 'Nova',
      mercado: 'Perú',
      precio: 'S/ 220',
      publico: 'Mujer 25–40',
      temporada: 'Primavera / Verano 2027',
    },
    inspiration: [0, 1, 2, 3, 4, 5, 6, 7].map((i) => ({
      id: uid('img'),
      src: placeholderImage(i, `Ref ${i + 1}`),
    })),
    dna: {
      principios: [
        'Lujo silencioso',
        'Paneles grandes y limpios',
        'Pocas costuras',
        'Siluetas estilizadas',
        'Suela baja (28–32 mm)',
        'Materiales naturales',
        'Estética europea',
        'Colores neutros y suaves',
      ],
      personalidad: [
        { label: 'Elegancia', value: 9.0 },
        { label: 'Minimalismo', value: 8.5 },
        { label: 'Artesanal', value: 7.5 },
        { label: 'Deportivo', value: 2.0 },
        { label: 'Urbano', value: 6.0 },
      ],
      keywords: ['minimal', 'timeless', 'premium', 'soft', 'european', 'crafted', 'refined', 'natural'],
    },
    selectedConceptId: null,
    activeView: 'lateral',
    concepts: [
      defaultConcept('A'),
      defaultConcept('B', { favorite: false }),
      defaultConcept('C', { favorite: false }),
      defaultConcept('D', { favorite: false }),
    ],
    chat: [
      {
        id: uid('msg'),
        role: 'ai',
        text: 'He analizado tu inspiración y el ADN de la colección. Este es el Concepto A. ¿Cómo te gustaría refinarlo?',
        time: '10:42',
      },
    ],
  };
}

// wire selectedConceptId after concepts exist
function withDefaults(col) {
  if (!col.selectedConceptId && col.concepts?.length) {
    col.selectedConceptId = col.concepts[0].id;
  }
  if (!col.activeView) col.activeView = 'lateral';
  return col;
}

const Store = {
  load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return this.seed();
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed) || parsed.length === 0) return this.seed();
      return parsed.map(withDefaults);
    } catch (e) {
      console.error('Dantix: fallo al leer almacenamiento, reiniciando.', e);
      return this.seed();
    }
  },
  seed() {
    const cols = [seedCollection()];
    this.saveAll(cols);
    localStorage.setItem(CURRENT_KEY, cols[0].id);
    return cols;
  },
  saveAll(collections) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(collections));
  },
  getCurrentId(collections) {
    const id = localStorage.getItem(CURRENT_KEY);
    if (id && collections.some((c) => c.id === id)) return id;
    const fallback = collections[0]?.id;
    if (fallback) localStorage.setItem(CURRENT_KEY, fallback);
    return fallback;
  },
  setCurrentId(id) {
    localStorage.setItem(CURRENT_KEY, id);
  },
  newCollection(name) {
    const col = seedCollection();
    col.name = name || 'Nueva colección';
    col.inspiration = [];
    col.chat = [{
      id: uid('msg'),
      role: 'ai',
      text: `He creado "${col.name}". Sube imágenes de inspiración para comenzar a definir el ADN de la colección.`,
      time: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' }),
    }];
    return col;
  },
};

export { Store, uid, placeholderImage };
