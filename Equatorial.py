import PyPDF2
import re
import os

def extrair_informacoes_nota_fiscal(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        primeira_pagina = pdf_reader.pages[0]
        texto_pagina = primeira_pagina.extract_text()

        # Extrair o Total a Pagar usando expressão regular
        total_pagar = re.search(r'Total\s*a\s*Pagar\s*R\$[\s\n]*([\d.,]+)', texto_pagina, re.IGNORECASE)
        total_pagar = total_pagar.group(1).replace(".", "").replace(",", ".") if total_pagar else "Não encontrado"

        # Extrair o vencimento usando expressão regular
        vencimento = re.search(r'Vencimento\s*(\d{2}/\d{2}/\d{4})', texto_pagina)
        vencimento = vencimento.group(1) if vencimento else "Não encontrado"

        return vencimento, total_pagar, num_pages

# Caminho da pasta com os arquivos PDF
pasta_pdf = r'C:\Users\Vitoria de Freitas\Desktop\projeto_vitoria\Notas\Equatorial'

# Lista para armazenar as informações de todos os PDFs
informacoes_todos_pdf = []

# Percorrer todos os arquivos da pasta
for nome_arquivo in os.listdir(pasta_pdf):
    if nome_arquivo.endswith(".pdf"):
        pdf_path = os.path.join(pasta_pdf, nome_arquivo)
        vencimento, total_pagar, num_pages = extrair_informacoes_nota_fiscal(pdf_path)
        informacoes_todos_pdf.append((nome_arquivo, vencimento, total_pagar, num_pages))

