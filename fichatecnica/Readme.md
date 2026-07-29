# Joli Joli · Technical Sheets

Arquitectura: **frontend estático en GitHub Pages** + **Google Apps Script
como API JSON** sobre tu Google Sheet (el mismo patrón que ya usas en tus
otros proyectos JOLI JOLI).

```
apps-script/          → Se pega en el editor de Apps Script del Sheet
  Config.gs
  Code.gs               doGet/doPost → API JSON (?action=search|ficha|pdf)
  SheetService.gs        Auto-detección de hojas/celdas + lectura de ficha
  ImageService.gs         Extracción de imágenes insertadas en celda
  appsscript.json

web/                   → Se sube tal cual a tu repo de GitHub Pages
  index.html
  styles.css
  config.js              ⚠️ aquí pegas la URL de tu deployment
  utils.js
  api.js                  Habla con la API vía fetch()
  app.js                   Lógica de la UI (búsqueda, render, acciones)
```

## Paso 1 — Backend (Apps Script)

1. Abre tu Google Sheet → **Extensiones → Apps Script**.
2. Crea los 4 archivos `.gs` y `appsscript.json` con el contenido de `apps-script/`.
3. **Implementar → Nueva implementación → Aplicación web**:
   - Ejecutar como: **Yo**.
   - Quién tiene acceso: **Cualquier usuario** (necesario para que
     GitHub Pages pueda llamarlo sin login).
4. Copia la URL, termina en `/exec`.
5. Pruébala directo en el navegador:
   `TU_URL/exec?action=ping` → debe responder `{"ok":true,"data":"pong"}`
   `TU_URL/exec?action=search&q=zoe` → debe listar productos.

## Paso 2 — Frontend (GitHub Pages)

1. En `web/config.js`, reemplaza `appsScriptUrl` con la URL del paso 1.
2. Sube la carpeta `web/` a tu repo (por ejemplo dentro de
   `rgenaro1.github.io/jolijoli/fichas/`, junto a tus otros módulos).
3. Abre `https://rgenaro1.github.io/jolijoli/fichas/` — listo.

Yo no tengo forma de hacer el push por ti (no tengo acceso a tu GitHub);
si más adelante conectas el conector de GitHub aquí en el chat, puedo
subir los commits directamente. Mientras tanto, descarga esta carpeta y
súbela tú (arrastrando los archivos en github.com o con `git push`).

## Por qué esta arquitectura funciona sin configurar CORS a mano

Un Apps Script Web App desplegado con acceso "Cualquier usuario" agrega
automáticamente `Access-Control-Allow-Origin: *` a las respuestas de
`doGet`/`doPost`, **siempre que la petición sea "simple"** (sin headers
custom, `Content-Type: application/x-www-form-urlencoded` o sin body).
Por eso:
- Las lecturas (`search`, `ficha`) van por **GET** con parámetros en la URL.
- El PDF va por **POST** con `application/x-www-form-urlencoded` (para no
  chocar con el límite de longitud de una URL de GET al mandar HTML).

No hace falta ningún `doOptions()` ni configuración adicional.

## Auto-detección de hojas y celdas (sin tocar tu Sheet)

- **Hoja "Ficha Técnica"**: primera hoja con una celda `CODIGO` y otra que
  contenga `Datos generales` en sus primeras 25 filas. Se cachea 6 h.
- **Celda de entrada del código**: la celda justo debajo de `CODIGO`.
- **Hoja de base de datos de productos** (autocompletado): la que tenga
  `Codigo, Modelo, Color, Categoria` en su fila de encabezados.
- **Secciones** (Datos generales, Imágenes, BOM, Instrucciones, Historial):
  se ubican por el texto de cada título (ignorando el emoji).

Si cambias el texto de una etiqueta, ajusta `SECTION_LABELS` en
**Config.gs** — el resto del código no se toca.

## Imágenes insertadas en la celda

Tus imágenes están insertadas dentro de la celda (no flotando encima).
`ImageService.gs` lee esto como un objeto `CellImage` (`range.getValue()`),
descarga los bytes con `UrlFetchApp` y los convierte a
`data:image/...;base64,...` para que no dependan de una URL temporal que
caduca. `getFicha()` cachea el resultado 30 s (`CACHE_SECONDS`) para no
repetir esa descarga en búsquedas seguidas.

## Cosas a verificar en tu Sheet real

El Sheet es muy grande para exportarlo completo desde aquí, así que trabajé
sobre una lectura de texto. Antes de dar el despliegue por cerrado:

- [ ] La celda de código está **una fila debajo** de la etiqueta `CODIGO`
      (si está a la derecha, cambia `codeCell.row + 1` por
      `codeCell.col + 1` en `getFicha()`, SheetService.gs).
- [ ] Cada celda bajo "IMAGEN PRINCIPAL"/"Detalle N" tiene **una sola
      imagen** (Apps Script solo puede leer la última si hay varias
      apiladas en la misma celda).
- [ ] Los nombres exactos de etapas (`CORTE`, `APARADO`, `ARMADO`,
      `ALISTADO`) coinciden con tu Sheet.

## Roadmap a PostgreSQL

`app.js` solo conoce `DantixApi.searchProducts()` y `DantixApi.getFicha()`.
El día que cambies de origen de datos, reimplementas esas dos funciones
(en `SheetService.gs`, o en un backend nuevo) manteniendo el mismo
contrato JSON — `api.js`/`app.js` no cambian.

