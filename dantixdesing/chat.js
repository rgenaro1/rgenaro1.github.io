// chat.js — simulated "Director Creativo IA" chat, responses derived from the collection's own data

import { el, escapeHtml } from './ui.js';
import { uid } from './data.js';
import { getConcept } from './design.js';

function now() {
  return new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' });
}

function renderChat(collection) {
  const thread = document.getElementById('chat-thread');
  thread.innerHTML = '';
  collection.chat.forEach((msg) => {
    thread.appendChild(el('div', { class: `chat-bubble chat-bubble--${msg.role}` }, [
      el('p', { html: escapeHtml(msg.text).replace(/\n/g, '<br>') }),
      el('span', { class: 'chat-time' }, msg.time),
    ]));
  });
  thread.scrollTop = thread.scrollHeight;
}

function showTyping(collection) {
  const thread = document.getElementById('chat-thread');
  const typing = el('div', { class: 'chat-bubble chat-bubble--ai chat-bubble--typing', id: 'typing-indicator' }, [
    el('span', { class: 'dot-flash' }), el('span', { class: 'dot-flash' }), el('span', { class: 'dot-flash' }),
  ]);
  thread.appendChild(typing);
  thread.scrollTop = thread.scrollHeight;
}

function clearTyping() {
  document.getElementById('typing-indicator')?.remove();
}

/** Produce a grounded reply by reading the concept/DNA JSON, tweaking it when relevant. */
function craftReply(collection, userText) {
  const text = userText.toLowerCase();
  const concept = getConcept(collection);

  if (/suela/.test(text)) {
    const lowered = /baj|reduc|menos/.test(text);
    concept.ficha.tipoSuela = concept.ficha.tipoSuela; // unchanged type, adjust narrative only
    return `Entendido. He tomado nota sobre la suela del Concepto ${concept.code}${lowered ? ', reduciendo su altura visual' : ''}. Tipo actual: ${concept.ficha.tipoSuela}.`;
  }
  if (/materia/.test(text)) {
    return `El material principal del Concepto ${concept.code} es ${concept.ficha.materialPrincipal}, combinado con ${concept.ficha.materialSecundario} como secundario. ¿Quieres que explore una alternativa más artesanal o más técnica?`;
  }
  if (/pieza|complej/.test(text)) {
    return `Este concepto tiene ${concept.ficha.piezas} piezas con una dificultad de construcción ${concept.ficha.dificultad}/5 (${concept.ficha.construccion}). Puedo simplificarlo si buscas reducir costo de producción.`;
  }
  if (/precio|costo/.test(text)) {
    return `El costo estimado del Concepto ${concept.code} es "${concept.ficha.costoEstimado}", alineado al precio objetivo de ${collection.meta.precio} para ${collection.meta.publico}.`;
  }
  if (/adn|principio|estilo|elegan/.test(text)) {
    const top = [...collection.dna.personalidad].sort((a, b) => b.value - a.value)[0];
    return `El ADN de "${collection.name}" está liderado por ${top.label.toLowerCase()} (${top.value.toFixed(1)}/10), con palabras clave como ${collection.dna.keywords.slice(0, 3).join(', ')}. Puedo reforzar ese carácter en el próximo concepto.`;
  }
  if (/largo|puntera|forma|silueta/.test(text)) {
    return `He ajustado la lectura de la silueta del Concepto ${concept.code} según tu indicación. Los cambios se reflejarán en la próxima iteración de render.`;
  }
  // generic reflective fallback grounded in the brand meta
  return `Tomo en cuenta tu indicación para "${collection.name}" (${collection.meta.marca}, ${collection.meta.temporada}). ¿Deseas que lo aplique sobre el Concepto ${concept.code} o prefieres generar una variante nueva?`;
}

function sendMessage(collection, text, onChange) {
  if (!text.trim()) return;
  collection.chat.push({ id: uid('msg'), role: 'user', text: text.trim(), time: now() });
  onChange();
  showTyping(collection);
  setTimeout(() => {
    clearTyping();
    const reply = craftReply(collection, text);
    collection.chat.push({ id: uid('msg'), role: 'ai', text: reply, time: now() });
    onChange();
  }, 700 + Math.random() * 500);
}

function bindChat(collectionRef, onChange) {
  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send-btn');
  const submit = () => {
    const value = input.value;
    if (!value.trim()) return;
    input.value = '';
    sendMessage(collectionRef(), value, onChange);
  };
  sendBtn.addEventListener('click', submit);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit(); }
  });
}

export { renderChat, bindChat, sendMessage };
