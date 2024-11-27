import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os

def criar_marca_dagua(texto_marca):
    # Criar um arquivo em memória para a marca d'água
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Definir o texto e o estilo da marca d'água
    c.setFont("Helvetica", 40)
    c.setFillColorRGB(0.7, 0.7, 0.7)  # Cor da marca d'água (cinza claro)
    c.rotate(45)  # Rotaciona a marca d'água
    c.drawString(200, 500, texto_marca)  # Posição do texto
    c.save()

    # Voltar ao início do arquivo em memória
    packet.seek(0)
    return PyPDF2.PdfReader(packet)

def adicionar_marca_dagua(pdf_input, pdf_output, texto_marca):
    # Verificar se o caminho de saída existe, caso contrário, cria o diretório
    output_dir = os.path.dirname(pdf_output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Abrir o arquivo PDF de entrada
    with open(pdf_input, "rb") as arquivo_pdf:
        leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
        num_paginas = len(leitor_pdf.pages)

        # Criar o PDF da marca d'água
        marca_dagua_pdf = criar_marca_dagua(texto_marca)
        marca_dagua_pagina = marca_dagua_pdf.pages[0]

        # Criar um objeto PDF de saída
        escritor_pdf = PyPDF2.PdfWriter()

        # Adicionar a marca d'água a cada página do PDF original
        for pagina_num in range(num_paginas):
            pagina = leitor_pdf.pages[pagina_num]
            pagina.merge_page(marca_dagua_pagina)  # Mescla a marca d'água com a página

            # Adiciona a página modificada ao PDF de saída
            escritor_pdf.add_page(pagina)

        # Salvar o novo arquivo PDF com a marca d'água
        with open(pdf_output, "wb") as arquivo_saida:
            escritor_pdf.write(arquivo_saida)

# Exemplo de uso:
input_pdf = "C:/Users/USER/Desktop/DEV/PDF/1.pdf"  # Caminho do arquivo PDF original
output_pdf = "C:/Users/USER/Desktop/DEV/SAI/1_marca.pdf"  # Caminho de saída
texto_da_marca = input("Digite o texto da marca d'água: ")  # Texto da marca d'água

adicionar_marca_dagua(input_pdf, output_pdf, texto_da_marca)
