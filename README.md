# BioXplorer

Es una aplicación de línea de comandos (CLI) que permite buscar secuencias biológicas en la base de datos NCBI y realizar análisis exploratorios básicos como transcripción, traducción y cálculo de contenido GC. También permite guardar los resultados en diferentes formatos.

## Requisitos

- Python 3.x
- Biopython
- dotenv

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/natayadev/bioxplorer.git
    cd bioxplorer
    ```

2. Crea un entorno virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Linux/iOS
    venv\Scripts\activate  # En Windows
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Crea un archivo `.env` en el directorio raíz y agrega tu correo electrónico:
    ```bash
    EMAIL=tu_email@example.com
    ```

## Instrucciones de uso:

1. **Configuración inicial:** Antes de ejecutar el programa, asegúrate de configurar un archivo `.env` en la carpeta raíz del proyecto con tu dirección de correo electrónico.

2. **Ejecución del script:** Para buscar secuencias por una palabra clave y realizar análisis, ejecuta el siguiente comando:

    ```bash
    python bioxplorer.py "melanogaster"
    ```

    Elige la secuencia que desees analizar de las opciones numéricas listadas y sigue las instrucciones en pantalla para realizar el análisis o guardar los resultados.


3. **Guardar los resultados:** Puedes elegir guardar los resultados en formato FASTA, FASTQ, JSON o CSV.
