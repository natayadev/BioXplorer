import argparse
from Bio import Entrez
from config.explorer import search_database, fetch_and_analyze
from config.validations import is_valid_email
from dotenv import load_dotenv
import os
import sys

load_dotenv()

def process_species(keyword):
    """Función que maneja la búsqueda y el análisis para una especie."""
    email = os.getenv("EMAIL")
    
    if email and is_valid_email(email):
        Entrez.email = email
        print(f"\n🔍 Buscando la palabra clave: {keyword}...\n")
    else:
        print("⚠️ Error: El correo electrónico configurado no es válido o no se encontró en el archivo .env. Asegúrate de configurarlo correctamente.")
        sys.exit(1)
    
    id_list = search_database(keyword)

    if id_list:
        print("\nSe encontraron las siguientes secuencias:")
        fetch_and_analyze(id_list)
    else:
        print("\n❌ No se encontraron secuencias para esa palabra clave. Intenta de nuevo.")

def main():
    parser = argparse.ArgumentParser(description="Explorador de secuencias biológicas con Biopython")
    parser.add_argument("keyword", type=str, help="Palabra clave para buscar en la base de datos (ej. homosapiens, sarscov2)")
    args = parser.parse_args()

    current_keyword = args.keyword
    process_species(current_keyword)

    while True:
        action = input("\nEscribe 'exit' para salir o presiona Enter para continuar: ").strip().lower()
        if action == "exit":
            sys.exit(0)
        elif action == "":
            sub_action = input("\n¿Quieres continuar con la misma palabra clave? Escribe 'si' o 'no': ").strip().lower()
            if sub_action == "si":
                process_species(current_keyword)
            elif sub_action == "no":
                current_keyword = input("\nEscribe la nueva palabra clave para buscar: ").strip()
                if current_keyword:
                    process_species(current_keyword)
                else:
                    print("⚠️ No ingresaste una palabra clave válida. Intenta de nuevo.")
            else:
                print("⚠️ Respuesta no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
