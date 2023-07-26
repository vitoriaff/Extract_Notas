import pdfminer
import re
import os
from pdfminer.high_level import extract_text

def extrair_informacoes_nota_fiscal_cesan(pdf_path):
    texto_pagina = extract_text(pdf_path)

    # Procurar por "Vencimento" e extrair a data no formato dd/mm/aaaa
    vencimento_match = re.search(r'Vencimento\s+(\d{2}/\d{2}/\d{4})', texto_pagina, re.IGNORECASE)
    vencimento = vencimento_match.group(1) if vencimento_match else "Não encontrado"

    # Extrair o "Valor Total a Pagar" usando a função personalizada
    valor_total = extrair_valor_total_a_pagar(texto_pagina)

    return vencimento, valor_total

def extrair_valor_total_a_pagar(texto_pagina):
    # Procurar por linhas que contenham "Valor Total a Pagar"
    linhas = texto_pagina.split('\n')
    for linha in linhas:
        valor_total_match = re.search(r'R\$[\s]*(\d{1,3}(?:\.\d{3})*(?:,\d{2}))', linha)
        if valor_total_match:
            return valor_total_match.group(1).replace(".", "").replace(",", ".")

    return "Não encontrado"

# Resto do código permanece o mesmo

# Exemplo de uso:
# Rest of the code remains the same
pasta_pdf = r'C:\Users\Vitoria de Freitas\Desktop\projeto_vitoria\Notas\CESAN'
informacoes_todos_pdf = []

for nome_arquivo in os.listdir(pasta_pdf):
    if nome_arquivo.endswith(".pdf"):
        pdf_path = os.path.join(pasta_pdf, nome_arquivo)
        informacoes = extrair_informacoes_nota_fiscal_cesan(pdf_path)
        if informacoes is not None:  # Check if both "Vencimento" and "Valor Total a Pagar" are found
            vencimento, total_pagar = informacoes
            informacoes_todos_pdf.append((vencimento, total_pagar))
        else:
            print(f"Warning: Skipping {pdf_path} due to insufficient information.")

