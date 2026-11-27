# Automatización de contenido (prototipo): Notion → n8n → Canva / Drive → LinkedIn, X, Instagram

Notion es la única fuente de verdad. n8n sólo lee Notion y ejecuta. Todo archivo generado vive en Google Drive.

| Qué | Dónde |
|---|---|
| (a) Configuración de Notion y Drive (permisos incluidos) | [docs/01-configuracion-notion-drive.md](docs/01-configuracion-notion-drive.md) |
| (b) Workflows importables | [workflows/A-diseno.json](workflows/A-diseno.json), [workflows/B-publicacion.json](workflows/B-publicacion.json) · guía de nodos: [docs/02-workflows.md](docs/02-workflows.md) |
| (c) Casos de prueba | [docs/03-casos-de-prueba.md](docs/03-casos-de-prueba.md) |
| (d) Lo que no se pudo verificar | [docs/04-no-verificado.md](docs/04-no-verificado.md) |

## Levantar n8n local con Docker

```bash
cd n8n-social
cp .env.example .env
openssl rand -hex 32            # pegar el resultado en N8N_ENCRYPTION_KEY y guardarlo en el gestor de contraseñas
# completar NOTION_DATABASE_ID, DRIVE_*, etc. (MODO_PRUEBA queda en true)
docker compose up -d
```

1. Abrir http://127.0.0.1:5678 y crear el usuario propietario (usá `127.0.0.1`, no `localhost`, para que los callbacks OAuth coincidan con `N8N_EDITOR_BASE_URL`).
2. Importar los workflows (quedan **inactivos**):
   ```bash
   docker compose exec n8n n8n import:workflow --input=/workflows/A-diseno.json
   docker compose exec n8n n8n import:workflow --input=/workflows/B-publicacion.json
   ```
   (o desde la interfaz: *Workflows → Import from file*).
3. Crear las credenciales en n8n (nunca en Notion ni en el repo) y asignarlas en cada nodo que muestre el aviso rojo: Notion, Google Drive, Canva (OAuth2 genérico), LinkedIn, X, Facebook Graph API, y opcionalmente Google Cloud Storage.
4. En el nodo Code **"Preparar pieza y elegir plantilla"** (flujo A) reemplazar los `REEMPLAZAR_*` por los IDs de plantilla de marca de Canva.
5. Probar con *Ejecutar a mano* y los casos de [docs/03-casos-de-prueba.md](docs/03-casos-de-prueba.md). Sólo después activar los dos workflows. **Seguir en `MODO_PRUEBA=true` hasta que los 4 casos den el resultado esperado.**
6. Para publicar de verdad: `MODO_PRUEBA=false` en `.env` y `docker compose up -d` (recrea el contenedor con el nuevo valor).

Los OAuth de Meta, LinkedIn y X suelen pedir una URL de callback registrada en cada consola de desarrollador: usar `http://127.0.0.1:5678/rest/oauth2-credential/callback` (si alguna consola exige https, hace falta un túnel; ver docs/04).

## Reglas de diseño (por qué está armado así)

- **Una pieza por corrida** de 15 min y concurrencia 1: evita publicaciones dobles sin lógica de locks compleja.
- **Bloqueo anti-duplicados:** antes de publicar se escribe `EN PROCESO …` en **Error**; el filtro nunca toma una pieza con ese texto. Además se exige "Enlace del post" vacío.
- **Campo Error como estado del robot:** vacío / `ERROR (intento n/3)` / `Diseño OK` se procesan; `EN PROCESO`, `BLOQUEADO`, `MANUAL …`, `REINTENTOS AGOTADOS` y (en modo prueba) `PRUEBA OK` no. Para reintentar: corregir la pieza y **borrar Error**.
- **Reintentos:** 3 intentos en total (1 + 2 reintentos), uno por corrida; Estado se mantiene en Aprobado.
- **Una pieza = una plataforma:** si una fila tiene más de una de Instagram/LinkedIn/X queda `BLOQUEADO` (duplicar la fila por plataforma), porque el archivo y el enlace del post son uno solo por fila.
- **Sin texto inventado:** n8n no genera copy; publica "Gancho y Copy" tal cual. Valida máximo 3 hashtags y 2 emojis.
