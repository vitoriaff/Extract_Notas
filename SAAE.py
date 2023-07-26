import pdfplumber
import re
import os

def extrair_informacoes_nota_fiscal_saae(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        primeira_pagina = pdf.pages[0]
        texto_pagina = primeira_pagina.extract_text()

        # Procurar por qualquer formato de moeda R$ 999.999,99 (flexible spacing and characters)
        valor_a_pagar = re.search(r'R\s*\$\s*([\d.,]+)', texto_pagina)
        valor_a_pagar = valor_a_pagar.group(1).replace(".", "").replace(",", ".") if valor_a_pagar else "Não encontrado"

        # Procurar por data no formato dd/mm/aaaa
        data_vencimento = re.search(r'\b\d{2}/\d{2}/\d{4}\b', texto_pagina)
        data_vencimento = data_vencimento.group() if data_vencimento else "Não encontrado"

        num_pages = len(pdf.pages)

        return valor_a_pagar, data_vencimento, num_pages

# Resto do código permanece o mesmo

# Caminho da pasta com os arquivos PDF
pasta_pdf = r'C:\Users\Vitoria de Freitas\Desktop\projeto_vitoria\Notas\SAAE'

# Lista para armazenar as informações de todos os PDFs
informacoes_todos_pdf = []

# Percorrer todos os arquivos da pasta
for nome_arquivo in os.listdir(pasta_pdf):
    if nome_arquivo.endswith(".pdf"):
        pdf_path = os.path.join(pasta_pdf, nome_arquivo)
        valor_a_pagar, data_vencimento, num_pages = extrair_informacoes_nota_fiscal_saae(pdf_path)
        informacoes_todos_pdf.append((nome_arquivo, valor_a_pagar, data_vencimento, num_pages))
