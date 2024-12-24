from Bio import SeqIO
import json

def save_fasta(record):
    print("\n💾 Guardando en formato FASTA...")
    with open(f"data/{record.id}.fasta", "w") as fasta_file:
        SeqIO.write(record, fasta_file, "fasta")
    print(f"📂 ¡Guardado! El archivo FASTA se guardó en data/{record.id}.fasta")

def save_csv(record):
    print("\n💾 Guardando en formato CSV...")
    with open(f"data/{record.id}.csv", "w") as csv_file:
        csv_file.write("ID,Secuencia\n")
        csv_file.write(f"{record.id},{record.seq}\n")
    print(f"📂 ¡Guardado! El archivo CSV se guardó en data/{record.id}.csv")

def save_fastq(record):
    print("\n💾 Guardando en formato FASTQ...")
    with open(f"data/{record.id}.fastq", "w") as fastq_file:
        fastq_file.write(f"@{record.id}\n")
        fastq_file.write(f"{record.seq}\n")
        fastq_file.write("+\n")
        fastq_file.write("I" * len(record.seq))
    print(f"📂 ¡Guardado! El archivo FASTQ se guardó en data/{record.id}.fastq")

def save_json(record):
    print("\n💾 Guardando en formato JSON...")
    data = {
        "id": record.id,
        "description": record.description,
        "sequence": str(record.seq),
        "organism": record.annotations.get("organism", "Desconocido")
    }
    with open(f"data/{record.id}.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"📂 ¡Guardado! El archivo JSON se guardó en data/{record.id}.json")
