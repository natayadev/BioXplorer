# (c) Casos de prueba

Todos con `MODO_PRUEBA=true` salvo que se indique. Entre pruebas, **borrar el campo Error** de la fila. Estado, fecha pasada y las 4 casillas tildadas salvo lo contrario. Verificar siempre en Notion y en Drive.

## Caso 1 - Carrusel de Instagram
**Fila:** Tipo=Carrusel, Plataforma=Instagram, Fecha pasada, Gancho y Copy con gancho + copy, "Archivo en Drive" vacío.
1. Ejecutar A a mano. **Esperado:** carpeta `Contenido/AAAA-MM/Carrusel/<nombre>/` con `…_p01.jpg … _pNN.jpg` de 1080×1350; "Archivo en Drive" = enlace a esa carpeta; "Enlace Canva" cargado; Error=`Diseño OK …`.
2. Ejecutar B (modo prueba). **Esperado:** Error=`PRUEBA OK … ruta instagram`, Estado sigue Aprobado, nada publicado.
3. Con `MODO_PRUEBA=false` y una cuenta de prueba: **esperado** Estado=Publicado y "Enlace del post" = permalink de Instagram. Si Meta rechaza el enlace de Drive: se prueba el bucket; si tampoco, Error=`MANUAL IG: …` y Estado sigue Aprobado.

## Caso 2 - Post de LinkedIn
**Fila:** Tipo=Post, Plataforma=LinkedIn.
1. A: **esperado** JPG 1200×1200 en `Contenido/AAAA-MM/Post/AAAA-MM-DD_LinkedIn_Post_<titulo>.jpg`, enlaces cargados.
2. B en prueba: `PRUEBA OK … ruta linkedin_imagen`.
3. B real: Estado=Publicado, "Enlace del post" = `https://www.linkedin.com/feed/update/urn:li:…/`. Variante Carrusel: PDF 1080×1350 y ruta `linkedin_pdf`.

## Caso 3 - Hilo de X
**Fila:** Tipo=Hilo, Plataforma=X, Gancho y Copy con 3 tuits (≤280 caracteres c/u) separados por líneas `---`. Sin archivo (A no interviene).
1. B en prueba: `PRUEBA OK … ruta x_hilo` (no publica).
2. B real: 3 tuits encadenados como respuestas; Estado=Publicado; "Enlace del post" = primer tuit.
3. Variante de control: un tuit de 300 caracteres → Error=`BLOQUEADO: el texto supera el límite de X…`, nada publicado.
Depende del plan de la API de X (ver docs/04).

## Caso 4 - Falla controlada
**Fila:** Post de LinkedIn, aprobado, con "Archivo en Drive" válido; en n8n, con `MODO_PRUEBA=false` y la credencial de LinkedIn **inválida** (o sin permisos).
1. Corrida 1: Error=`ERROR (intento 1/3): [LinkedIn: publicar imagen] …`; Estado=Aprobado; "Enlace del post" vacío.
2. Corrida 2 (15 min después, o a mano): `ERROR (intento 2/3)`. Corrida 3: `REINTENTOS AGOTADOS (3/3)…`.
3. Corrida 4: **no** toma la pieza (no hay 4º intento). Restaurar la credencial, borrar Error: publica y pasa a Publicado.
Controles extra, sin publicar nada: casilla de calidad destildada → no la toma; fecha futura → no la toma; sin "Archivo en Drive" → `BLOQUEADO: falta "Archivo en Drive"`; dos ejecuciones simultáneas → sólo una toma la pieza (concurrencia 1 + `EN PROCESO`).

## Ya verificado en este entorno (sin n8n)
Lógica de los nodos Code ejecutada con páginas de Notion simuladas: ruta/bloqueo correctos para carrusel IG (carpeta), post LinkedIn, hilo X (3 partes), sin archivo, casilla faltante, fecha futura, 2 plataformas, 4 hashtags, Story IG (→ MANUAL), WhatsApp (ignorada), 300 caracteres en X; y nombres de archivo `2026-11-20_Instagram_Post_que-lindo-dia-nandu`. No se ejecutó ninguna llamada real a Notion, Canva, Drive, Meta, LinkedIn ni X.
