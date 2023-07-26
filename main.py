from edp import extrair_informacoes_nota_fiscal_edp as extrair_edp
from CAEMA import extrair_informacoes_nota_fiscal_caema as extrair_caema
from Equatorial import extrair_informacoes_nota_fiscal_Equatorial as extrair_equatorial
from cesan import extrair_informacoes_nota_fiscal_cesan as extrair_cesan
from SAAE import extrair_informacoes_nota_fiscal_saae as extrair_saae
import os
import unicodedata

def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

# Lista dos caminhos das pastas com os arquivos PDF e o nome de cada empresa
pastas_empresas = [
    (r'C:\Users\Vitoria de Freitas\Desktop\projeto_vitoria\Notas\EDP', 'EDP'),
    (r'C:\Users\Vitoria de Freitas\Desktop\projeto_vitoria\Notas\CAEMA', 'CAEMA'),
    (r'C:\Users\Vitoria de Freitas\Desktop\projeto_vitoria\Notas\Equatorial', 'Equatorial'),
    (r'C:\Users\Vitoria de Freitas\Desktop\projeto_vitoria\Notas\CESAN', 'CESAN'),
    (r'C:\Users\Vitoria de Freitas\Desktop\projeto_vitoria\Notas\SAAE', 'SAAE')
]
# Lista para armazenar todas as informações de todos os PDFs
informacoes_todos_pdf = []

# Percorrer todas as pastas e extrair as informações de cada uma
for pasta_pdf, nome_empresa in pastas_empresas:
    if nome_empresa == 'EDP':
        extrair_funcao = extrair_edp
    elif nome_empresa == 'CAEMA':
        extrair_funcao = extrair_caema
    elif nome_empresa == 'Equatorial':
        extrair_funcao = extrair_equatorial
    elif nome_empresa == 'CESAN':
        extrair_funcao = extrair_cesan
    elif nome_empresa == 'SAAE':
        extrair_funcao = extrair_saae
    else:
        print(f"Warning: Unrecognized empresa '{nome_empresa}'. Skipping...")
        continue
    # Percorrer todos os arquivos da pasta
    for nome_arquivo in os.listdir(pasta_pdf):
        if nome_arquivo.endswith(".pdf"):
            pdf_path = os.path.join(pasta_pdf, nome_arquivo)
            informacoes = extrair_funcao(pdf_path)
            try:
                # Check if the informacoes tuple has at least 3 elements before appending it
                if len(informacoes) >= 3:
                    informacoes_todos_pdf.append((nome_arquivo, nome_empresa, informacoes[0], informacoes[1], informacoes[2]))
                else:
                    print(f"Warning: Skipping {pdf_path} due to insufficient information. Contents of 'informacoes': {informacoes}")
            except IndexError:
                print(f"Error: Unable to extract information from {pdf_path}.")
                continue

# Criar e escrever no arquivo de relatório txt
with open("relatorio.txt", "w", encoding='utf-8') as arquivo_relatorio:
    for info in informacoes_todos_pdf:
        nome_arquivo, nome_empresa, data_vencimento, total_pagar, num_pages = info
        arquivo_relatorio.write(f"Informações da empresa {nome_empresa}\n")
        arquivo_relatorio.write(f"Arquivo PDF: {nome_arquivo}\n")
        arquivo_relatorio.write(f"VENCIMENTO: {data_vencimento}\n")
        arquivo_relatorio.write(f"Valor Total a Pagar: R$ {total_pagar}\n")
        arquivo_relatorio.write(f"Número de páginas: {num_pages}\n")
        arquivo_relatorio.write("--------------\n")

print("Relatório gerado com sucesso!")