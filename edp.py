import pdfplumber
import re
import os

def extrair_informacoes_nota_fiscal(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        primeira_pagina = pdf.pages[0]
        texto_pagina = primeira_pagina.extract_text()

        # Procurar por data no formato dd/mm/aaaa
        data_vencimento = re.search(r'\b\d{2}/\d{2}/\d{4}\b', texto_pagina)
        data_vencimento = data_vencimento.group() if data_vencimento else "Não encontrado"

        # Procurar por valor monetário no formato R$ 999.999,99
        total_pagar = re.search(r'R\$ (\d{1,3}(?:\.\d{3})*(?:,\d{2}))', texto_pagina)
        total_pagar = total_pagar.group(1).replace(".", "").replace(",", ".") if total_pagar else "Não encontrado"

        return data_vencimento, total_pagar, len(pdf.pages)


# Caminho da pasta com os arquivos PDF
pasta_pdf = r'C:\Users\Vitoria de Freitas\Desktop\projeto_vitoria\Notas\EDP'

# Lista para armazenar as informações de todos os PDFs
informacoes_todos_pdf = []

# Percorrer todos os arquivos da pasta
for nome_arquivo in os.listdir(pasta_pdf):
    if nome_arquivo.endswith(".pdf"):
        pdf_path = os.path.join(pasta_pdf, nome_arquivo)
        data_vencimento, total_pagar, num_pages = extrair_informacoes_nota_fiscal(pdf_path)
        informacoes_todos_pdf.append((nome_arquivo, data_vencimento, total_pagar, num_pages))

