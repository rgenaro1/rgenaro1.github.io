/**
 * config.js — Preferencias de la app + endpoint del backend.
 *
 * ⚠️ PASO OBLIGATORIO ANTES DE SUBIR A GITHUB PAGES:
 * Reemplaza appsScriptUrl con la URL de TU deployment de Apps Script
 * (Implementar → Nueva implementación → Aplicación web → copiar URL,
 * termina en /exec).
 */
window.DantixConfig = {
  appName: 'Joli Joli · Technical Sheets',
  appsScriptUrl: 'https://script.google.com/macros/s/PEGA_AQUI_TU_DEPLOYMENT_ID/exec',
  searchDebounceMs: 250,
  minCharsForAutocomplete: 1,
  theme: {
    storageKey: 'dantix-fichas-theme', // 'light' | 'dark' | 'auto'
    default: 'auto'
  }
};
