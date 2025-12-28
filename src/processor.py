import shutil
import os
from extractor import extract_data_from_pdf
from database_manager import DatabaseManager

INPUT_DIR = r"faturas\input"
PROCESSING_DIR = r"faturas\processing"
ARCHIVE_DIR = r"faturas\processing\archive"
ERROR_DIR = r"faturas\processing\error"

def process_invoices():
    # 1. Listar arquivos PDF na pasta input
    for i in os.listdir(INPUT_DIR):
        if i.lower().endswith(".pdf"):
            full_path_input = os.path.join(INPUT_DIR, i)
        # 2. Para cada arquivo:
        #    a. Mover para processing
            full_path_processing = shutil.move(full_path_input, os.path.join(PROCESSING_DIR, i))
        #    b. Extrair dados
            try:
                data = extract_data_from_pdf(full_path_processing) 

                #    c. Salvar no banco de dados
                db = DatabaseManager("faturas.db")
                db.connect()
                db.insert_fatura(
                    nif_emissor = data['nif_emissor'] ,
                    nome_emissor = data['nome_cliente'] ,
                    data_emissao = data['data_emissao'] ,
                    data_vencimento = data['data_vencimento'] ,
                    valor_total = data['valor_total'] ,
                    status  = "Processado" ,
                    arquivo_path = full_path_processing
                )

                #    d. Se sucesso → mover para archive
                shutil.move(full_path_processing, os.path.join(ARCHIVE_DIR, i))
                print(f"Data extracted:\n{data}")
 
            except Exception as e:
                #    e. Se erro → mover para error
                print(f"Erro to processs {i}: {e}")
                shutil.move(full_path_processing, os.path.join(ERROR_DIR, i))
    pass



if __name__ == "__main__":
    process_invoices()