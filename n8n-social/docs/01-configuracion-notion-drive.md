# (a) Configuración en Notion y Google Drive

## Notion

1. **Base "Calendario de contenidos"** con las propiedades indicadas. Tipos de propiedad que asumen los workflows:
   - Contenido: *Título* · Estado: *Estado (Status)* · Tipo: *Selección* · Plataforma: *Selección múltiple*
   - Fecha de publicación: *Fecha* (con hora) · Gancho y Copy: *Texto* · Enlace Canva: *URL*
   - Revisora, Responsable: *Persona* · 4 casillas de calidad: *Casilla* (nombres exactos, con tildes)
2. **Agregar 3 propiedades:** `Archivo en Drive` (URL), `Enlace del post` (URL), `Error` (Texto).
3. **Estados** (en este orden): Backlog, Por hacer, Pendiente de aprobación, Aprobado, Publicado. No hace falta un estado "En proceso": el bloqueo usa el campo Error.
4. **Convención de "Gancho y Copy":** primera línea = gancho; el resto = copy. En **Hilo** de X, separar los tuits con una línea que contenga sólo `---`.
5. **Una fila por plataforma** (ver README). Plataformas WhatsApp, YouTube y Luma se ignoran.
6. **Integración interna** (https://www.notion.so/profile/integrations → *Nueva integración*, tipo interna):
   - Capacidades: *Read content*, *Update content*. No hace falta *Insert* ni acceso a usuarios.
   - Copiar el token **sólo** a la credencial de n8n (y al gestor de contraseñas).
   - En la base: *⋯ → Conexiones → agregar la integración*. Es la única base que ve n8n.
7. **ID de la base:** de la URL `notion.so/<workspace>/<ID de 32 caracteres>?v=…` → `NOTION_DATABASE_ID`.
8. **Vistas recomendadas:** "Para revisar" = Error contiene `MANUAL` o `BLOQUEADO` o `ERROR` o `REINTENTOS`; así la gente ve qué requiere acción. Se puede sumar una automatización nativa de Notion que avise por Slack/mail cuando Error contenga `MANUAL IG`.
9. **Quién aprueba:** cambiar Estado a *Aprobado* y tildar las casillas es acción humana (Revisora). n8n nunca las toca.

## Google Drive

1. **Unidad compartida del equipo** (no "Mi unidad" de una cuenta personal): Drive → *Unidades compartidas → Nueva*. Así los archivos no dependen de una persona. Requiere Google Workspace.
2. Dentro, crear la carpeta **`Contenido`**. El flujo A crea solo `AAAA-MM/Tipo` (y una subcarpeta por carrusel de Instagram, que son varias imágenes).
3. **Permisos:**
   - Cuenta de servicio / cuenta técnica de n8n (ej. `n8n-contenido@…`): **Colaborador** (puede subir y compartir) en la unidad. No Administrador de contenido.
   - Equipo de contenido: Editor o Colaborador. Revisoras: Lector o Comentarista.
   - Para el **intento 1 de Instagram** se comparte cada imagen con "cualquier persona con el enlace" (lector). Eso exige que la configuración de uso compartido del dominio/unidad lo permita (*Admin de Google Workspace → Drive → Uso compartido*). Si no se permite, el intento falla y se pasa al hosting alternativo o a manual.
4. **Credencial en n8n:** *Google Drive OAuth2 API* (Cloud Console: habilitar *Google Drive API*, pantalla de consentimiento, cliente OAuth tipo Web con redirect `http://127.0.0.1:5678/rest/oauth2-credential/callback`). El usuario que autoriza debe ser miembro de la unidad.
5. IDs para `.env`: `DRIVE_SHARED_DRIVE_ID` (URL `drive.google.com/drive/folders/<ID>` estando en la raíz de la unidad) y `DRIVE_ROOT_FOLDER_ID` (ID de `Contenido`).
6. **Nombre de archivo:** `AAAA-MM-DD_Plataforma_Tipo_titulo-corto` (fecha = Fecha de publicación en hora de Buenos Aires; título sin tildes, minúsculas, máx. 40 caracteres). Carruseles de imágenes: sufijo `_p01`, `_p02`…

## Credenciales (todas en n8n + gestor de contraseñas compartido)

| Servicio | Credencial de n8n | Notas |
|---|---|---|
| Notion | Notion API | token de integración interna |
| Google Drive | Google Drive OAuth2 | ver arriba |
| Canva | OAuth2 API (genérica) | Auth URL `https://www.canva.com/api/oauth/authorize`, token URL `https://api.canva.com/rest/v1/oauth/token`, grant *PKCE*, autenticación *Header (Basic)*, scopes `design:content:read design:content:write design:meta:read brandtemplate:content:read brandtemplate:meta:read asset:read` |
| LinkedIn | LinkedIn OAuth2 | scope `w_member_social` (persona) o `w_organization_social` (página, requiere aprobación de LinkedIn) |
| X | X OAuth2 | scopes `tweet.read tweet.write users.read media.write offline.access` |
| Instagram | Facebook Graph API | token de página/usuario con `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`; cuenta de Instagram **profesional vinculada a una página** |
| (opcional) Google Cloud Storage | GCS OAuth2 | sólo intento 2 de Instagram |

Rotación y custodia: el token vive en n8n (cifrado con `N8N_ENCRYPTION_KEY`) y la fuente de respaldo es el gestor de contraseñas. Nunca en Notion, `.env` versionado ni prompts.
