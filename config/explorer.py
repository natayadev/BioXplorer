from Bio import Entrez, SeqIO
from Bio.SeqUtils import gc_fraction
from config.saver import save_fasta, save_csv, save_fastq, save_json
from dotenv import load_dotenv

load_dotenv()

def search_database(keyword):
    """Busca secuencias en la base de datos 'nucleotide' usando la palabra clave."""
    handle = Entrez.esearch(db="nucleotide", term=keyword, retmax=5)
    record = Entrez.read(handle)
    return record["IdList"]


def complete_sequence(seq):
    """Asegura que la secuencia tenga una longitud múltiplo de tres completando con 'N'."""
    remainder = len(seq) % 3
    if remainder != 0:
        seq += "N" * (3 - remainder) 
        print(f"⚠️ La longitud de la secuencia no es un múltiplo de tres. Se ha completado con 'N' al final.")
    return seq


def fetch_and_analyze(id_list):
    """Obtiene y analiza las secuencias a partir de una lista de IDs."""
    print("Eligiendo secuencia... 🧐\n")
    valid_ids = []

    for idx, seq_id in enumerate(id_list, 1):
        try:
            handle = Entrez.efetch(db="nucleotide", id=seq_id, rettype="gb", retmode="text")
            record = SeqIO.read(handle, "genbank")
            
            valid_ids.append((seq_id, record))  # Agregar solo secuencias válidas
            print(f"{idx}. ID de secuencia: {seq_id}")
            print(f"   Descripción: {record.description}")
            print(f"   Organismo: {record.annotations.get('organism', 'Desconocido')}")
            print(f"   Longitud: {len(record.seq)} nucleótidos")
            print(f"   Fecha de actualización: {record.annotations.get('date', 'Desconocida')}")
            print(f"   Fuente: {record.annotations.get('source', 'Desconocida')}\n")
        except Exception as e:
            # Si la secuencia no es válida, se muestra un mensaje de error y no se agrega
            print(f"⚠️ Error al obtener la secuencia con ID {seq_id}. Error: {e}\nSaltando...\n")
            continue

    if valid_ids:
        while True:
            try:
                choice = input("\nElige el número de la secuencia que deseas analizar: ")
                choice = int(choice)
                
                if choice < 1 or choice > len(valid_ids):
                    print("❌ Selección fuera de rango. Debes elegir un número entre 1 y", len(valid_ids))
                    continue  # Volver a mostrar la lista si la opción está fuera de rango

                selected_id, selected_record = valid_ids[choice - 1]
                
                print(f"\n📚 Descripción: {selected_record.description}")
                print(f"🧬 Secuencia: {selected_record.seq[:50]}...") 
                print(f"🔢 Longitud de la secuencia: {len(selected_record.seq)} nucleótidos")

                rna_seq = selected_record.seq.transcribe()
                protein_seq = selected_record.seq.translate()

                print("\n🔬 Análisis de la secuencia:")
                print(f"🌱 Transcripción (ARN): {rna_seq[:50]}...") 
                print(f"🥩 Traducción (Proteína): {protein_seq[:50]}...")

                gc_content = gc_fraction(selected_record.seq)
                print(f"🧪 Contenido de GC: {gc_content:.2f}%")

                try:
                    save_choice = input("\n¿Te gustaría guardar los resultados? (fasta/csv/fastq/json/no): ").lower()
                    if save_choice == "fasta":
                        save_fasta(selected_record)
                    elif save_choice == "csv":
                        save_csv(selected_record)
                    elif save_choice == "fastq":
                        save_fastq(selected_record)
                    elif save_choice == "json":
                        save_json(selected_record)
                    
                    break 

                except ValueError:
                    print("❌ Selección inválida. Debes ingresar un número entero válido.")
            except Exception as e:
                print(f"⚠️ Hubo un error al procesar la secuencia. Error: {e}\nVolviendo a intentar...\n")
                continue  # Volver a intentar la selección si ocurre un error

    else:
        print("❌ No se encontraron secuencias válidas para analizar.")
