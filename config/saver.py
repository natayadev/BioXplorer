from Bio import SeqIO
import json
import os

def data_directory():
    if not os.path.exists("data"):
        os.makedirs("data")
        print("📂 Carpeta 'data' creada con éxito.")

def save_all(record):
    save_json(record)
    save_csv(record)
    save_fastq(record)
    save_fasta(record)

def save_fasta(record):
    with open(f"data/{record.id}.fasta", "w") as fasta_file:
        SeqIO.write(record, fasta_file, "fasta")
    print(f"💾 ¡Guardado! El archivo FASTA se guardó en data/{record.id}.fasta")

def save_csv(record):
    with open(f"data/{record.id}.csv", "w") as csv_file:
        csv_file.write("ID,Secuencia\n")
        csv_file.write(f"{record.id},{record.seq}\n")
    print(f"💾 ¡Guardado! El archivo CSV se guardó en data/{record.id}.csv")

def save_fastq(record):
    with open(f"data/{record.id}.fastq", "w") as fastq_file:
        fastq_file.write(f"@{record.id}\n")
        fastq_file.write(f"{record.seq}\n")
        fastq_file.write("+\n")
        fastq_file.write("I" * len(record.seq))
    print(f"💾 ¡Guardado! El archivo FASTQ se guardó en data/{record.id}.fastq")

def save_json(record):
    data = {
        "id": record.id,
        "description": record.description,
        "sequence": str(record.seq),
        "organism": record.annotations.get("organism", "Desconocido")
    }
    with open(f"data/{record.id}.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"💾 ¡Guardado! El archivo JSON se guardó en data/{record.id}.json")

def generate_report(record, gc_content, orfs):
    """Genera un reporte HTML de los resultados del análisis con estilo."""
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 20px;
                color: #333;
            }}
            h1 {{
                color: #4CAF50;
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #333;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
                color: #333;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .content {{
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .section {{
                margin-bottom: 30px;
            }}
            .highlight {{
                color: #ff6347;
                font-weight: bold;
            }}
            .gc-content {{
                color: #4CAF50;
                font-size: 1.2em;
            }}
        </style>
    </head>
    <body>
        <div class="content">
            <h1>Análisis de {record.description}</h1>
            <div class="section">
                <p><b>ID:</b> {record.id}</p>
                <p><b>Longitud de la secuencia:</b> {len(record.seq)} nucleótidos</p>
                <p><b>Organismo:</b> {record.annotations.get('organism', 'Desconocido')}</p>
                <p><b>Fuente:</b> {record.annotations.get('source', 'Desconocida')}</p>
                <p><b>Fecha de actualización:</b> {record.annotations.get('date', 'Desconocida')}</p>
            </div>

            <div class="section">
                <h2>Contenido de GC</h2>
                <p class="gc-content">El contenido de GC en esta secuencia es: <span class="highlight">{gc_content:.2f}%</span></p>
            </div>

            <div class="section">
                <h2>ORFs Encontrados</h2>
                {generate_orf_table(orfs)}
            </div>
        </div>
    </body>
    </html>
    """

    with open(f"data/{record.id}_analysis_report.html", "w") as report_file:
        report_file.write(html_content)

    print(f"✅ Reporte guardado en 'data/{record.id}_analysis_report.html'")

def generate_orf_table(orfs):
    """Genera una tabla HTML con los ORFs encontrados."""
    if not orfs:
        return "<p>No se encontraron ORFs en esta secuencia.</p>"

    table_html = """
    <table>
        <tr>
            <th>Marco</th>
            <th>Cadena</th>
            <th>Inicio</th>
            <th>Fin</th>
        </tr>
    """
    
    for orf in orfs:
        table_html += f"""
        <tr>
            <td>{orf[0]}</td>
            <td>{orf[1]}</td>
            <td>{orf[2]}</td>
            <td>{orf[3]}</td>
        </tr>
        """
    
    table_html += "</table>"
    return table_html
