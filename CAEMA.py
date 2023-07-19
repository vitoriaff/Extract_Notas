import pdfplumber
import re
import os

def extrair_informacoes_nota_fiscal(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        primeira_pagina = pdf.pages[0]
        texto_pagina = primeira_pagina.extract_text()

        # Procurar por "VENCIMENTO" e extrair a data de vencimento próxima
        data_vencimento = "Não encontrado"
        match_data_vencimento = re.search(r'VENCIMENTO[\s:]+(\d{2}/\d{2}/\d{4})', texto_pagina, re.IGNORECASE)
        if match_data_vencimento:
            data_vencimento = match_data_vencimento.group(1)

        # Procurar por "VALOR R$" usando expressão regular
        total_pagar = re.search(r'VALOR\s*R?\$\s*([\d.,]+)', texto_pagina, re.IGNORECASE)
        total_pagar = total_pagar.group(1).replace(".", "").replace(",", ".") if total_pagar else "Não encontrado"

        return data_vencimento, total_pagar, len(pdf.pages)

# Restante do código permanece o mesmo...

# Caminho da pasta com os arquivos PDF
pasta_pdf = r'C:\Users\Vitoria de Freitas\Desktop\projeto_vitoria\Notas\CAEMA'

# Lista para armazenar as informações de todos os PDFs
informacoes_todos_pdf = []

# Percorrer todos os arquivos da pasta
for nome_arquivo in os.listdir(pasta_pdf):
    if nome_arquivo.endswith(".pdf"):
        pdf_path = os.path.join(pasta_pdf, nome_arquivo)
        informacoes = extrair_informacoes_nota_fiscal(pdf_path)
        informacoes_todos_pdf.append((nome_arquivo, informacoes[0], informacoes[1], informacoes[2]))
