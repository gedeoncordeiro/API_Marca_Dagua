import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
import os

def criar_marca_dagua(texto_marca, largura_pagina, altura_pagina):
    # Criar um arquivo em memória para a marca d'água
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(largura_pagina, altura_pagina))

    # Registrar a fonte Arial Black (ou substitua por Helvetica-Bold se necessário)
    try:
        pdfmetrics.registerFont(TTFont('Arial-Black', r'C:\Windows\Fonts\arialbd.ttf'))
    except FileNotFoundError:
        print("A fonte Arial Black não foi encontrada. Verifique o caminho ou use outra fonte.")
        return None

    # Definir o texto e o estilo da marca d'água
    c.setFont("Arial-Black", 50)
    c.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.3)  # Transparência de 30%

    # Centralizar o texto
    texto_largura = c.stringWidth(texto_marca, "Arial-Black", 50)
    x = (largura_pagina - texto_largura) / 600
    y = altura_pagina / 600

    c.rotate(45)
    c.drawString(x, y, texto_marca)
    c.save()
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
        escritor_pdf = PyPDF2.PdfWriter()
        num_paginas = len(leitor_pdf.pages)

        for pagina_num in range(num_paginas):
            pagina = leitor_pdf.pages[pagina_num]
            largura_pagina = float(pagina.mediabox.width)
            altura_pagina = float(pagina.mediabox.height)

            # Criar a marca d'água personalizada
            marca_dagua_pdf = criar_marca_dagua(texto_marca, largura_pagina, altura_pagina)
            if not marca_dagua_pdf:
                continue

            marca_dagua_pagina = marca_dagua_pdf.pages[0]
            pagina.merge_page(marca_dagua_pagina)
            escritor_pdf.add_page(pagina)

        # Salvar novo PDF
        with open(pdf_output, "wb") as arquivo_saida:
            escritor_pdf.write(arquivo_saida)

# Exemplo de uso:
input_pdf = "C:/Users/USER/Desktop/DEV/PDF/1.pdf"  # Entrada
output_pdf = "C:/Users/USER/Desktop/DEV/SAI/1_marca.pdf"  # Destino
texto_da_marca = "           ESPELHO DE MATRÍCULA"
texto_da_marca = "           SEM VALOR DE CERTIDÃO"

adicionar_marca_dagua(input_pdf, output_pdf, texto_da_marca)

