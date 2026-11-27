# (b) Workflows de n8n: guía de nodos

Los JSON están en `workflows/`. Cada nodo tiene nombre en castellano y una nota visible en el lienzo. Los dos usan zona horaria `America/Argentina/Buenos_Aires` y corren cada 15 minutos (más un disparador manual para pruebas).

## A - Diseño (`A-diseno.json`)

| # | Nodo | Qué hace |
|---|---|---|
| 1 | Notion: buscar piezas aprobadas sin archivo | Estado=Aprobado, "Archivo en Drive" vacío, Tipo ∈ {Carrusel, Post, Flyer, Story}, Error vacío o `ERROR (intento…`. Límite 1 |
| 2 | Preparar pieza y elegir plantilla (Code) | Valida, elige plantilla por Plataforma+Tipo, arma nombre y datos de autofill. **Acá se cargan los IDs de plantilla** |
| 3 | ¿Pieza válida? / Notion: registrar bloqueo | Si falta algo, escribe `BLOQUEADO: motivo` en Error |
| 4 | Notion: marcar en proceso | Escribe `EN PROCESO…` en Error (anti-duplicados) |
| 5 | Drive: buscar / crear carpeta del mes y del tipo | `Contenido/AAAA-MM/Tipo` (nodo nativo de Google Drive) |
| 6 | ¿Va en subcarpeta propia? | Sólo carruseles de imágenes (Instagram) |
| 7 | Canva: pedir autofill → Esperar → consultar → ¿en curso? | `POST /v1/autofills` con `gancho` y `copy`; sondeo cada 5 s |
| 8 | Canva: pedir exportación → Esperar → consultar | `POST /v1/exports`: JPG con ancho/alto de la tabla o PDF (LinkedIn carrusel) |
| 9 | Canva: descargar archivo exportado | Los enlaces de Canva vencen, se bajan enseguida |
| 10 | Drive: subir archivo a la carpeta destino | Nodo nativo; nombre `AAAA-MM-DD_Plataforma_Tipo_titulo-corto` |
| 11 | Notion: guardar enlaces del diseño | "Archivo en Drive", "Enlace Canva", Error=`Diseño OK …` |
| 12 | Registrar fallo → Notion: guardar error | `ERROR (intento n/3)`; al 3º `REINTENTOS AGOTADOS` |

**Plantillas y medidas** (una plantilla de marca por fila, ya con su tamaño; la exportación además fuerza ancho/alto):

| Plataforma | Tipo | Medida | Formato |
|---|---|---|---|
| Instagram | Post, Carrusel, Flyer | 1080×1350 | JPG (carrusel: una imagen por página) |
| Instagram | Story | 1080×1920 | JPG |
| LinkedIn | Carrusel | 1080×1350 | PDF |
| LinkedIn | Post, Flyer | 1200×1200 | JPG |
| X | Post, Flyer | 1200×675 | JPG |

Cada plantilla de Canva necesita dos campos de texto de autofill llamados `gancho` y `copy`. Combinaciones sin fila en la tabla (ej. Carrusel en X) quedan `BLOQUEADO`.

**Sobre el "nodo oficial de Canva":** Canva publicó un nodo de comunidad para n8n, pero no pude confirmar su nombre de paquete ni sus parámetros desde acá. Por eso el flujo usa la **API Connect de Canva con nodos HTTP Request y una credencial OAuth2 genérica**, que se puede reemplazar nodo a nodo por el oficial si el equipo lo instala (*Settings → Community nodes*).

## B - Publicación (`B-publicacion.json`)

| # | Nodo | Qué hace |
|---|---|---|
| 1 | Notion: buscar piezas listas para publicar | Estado=Aprobado, fecha ≤ ahora, 4 casillas, sin "Enlace del post", Plataforma incluye IG/LinkedIn/X. Límite 1 |
| 2 | Validar pieza y elegir ruta (Code) | Revalida todo (incluye fecha en hora BA, límites de caracteres, máx. 3 hashtags y 2 emojis) y elige ruta |
| 3 | ¿Modo prueba? (antes de bloquear) | En modo real marca `EN PROCESO` |
| 4 | Drive: listar imágenes / descargar archivo | Verifica y trae el archivo (carpeta para carrusel de Instagram) |
| 5 | ¿Modo prueba? (antes de publicar) | **Sí:** escribe `PRUEBA OK …` en Error, no cambia Estado. **No:** sigue |
| 6 | Elegir ruta de publicación | `instagram`, `linkedin_imagen`, `linkedin_pdf`, `x_imagen`, `x_hilo` |
| 7 | LinkedIn: publicar imagen | Nodo nativo de LinkedIn |
| 8 | LinkedIn: PDF | HTTP a Documents API (iniciar → subir → crear post): el nodo nativo no sube documentos |
| 9 | X: publicar tuit con imagen / hilo | Nodo nativo de X; el hilo publica un tuit por vuelta respondiendo al anterior |
| 10 | IG: intento 1 (Drive público) → intento 2 (bucket público) → manual | Nodo Facebook Graph API (ver abajo) |
| 11 | Armar resultado → Notion: marcar Publicado | Estado=Publicado, "Enlace del post", Error=`Publicado OK …` |
| 12 | Registrar fallo → Notion: guardar error | Estado sigue Aprobado; 3 intentos; un hilo a medio publicar pasa a `MANUAL X` para no duplicar |

**Instagram, en el orden pedido** (Graph API: contenedor → esperar → `media_publish`):
1. Se comparte cada JPG de Drive con "cualquiera con el enlace" y se usa `https://drive.google.com/uc?export=download&id=<ID>` como `image_url`.
2. Si Meta rechaza alguna imagen, y `IG_PUBLIC_BUCKET` está definido, se descargan de Drive, se suben a un bucket público de Google Cloud Storage y se reintenta con `https://storage.googleapis.com/<bucket>/…`.
3. Si también falla (o no hay bucket): Error=`MANUAL IG: … <enlace de Drive>`, Estado sigue Aprobado. Quien publica a mano pasa Estado a Publicado y pega el enlace.

Story de Instagram, Reel y Video no se publican automáticamente (Story → `MANUAL IG`).
