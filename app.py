from flask import Flask, render_template, request, send_file
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Criar pastas se não existirem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def criar_marca_dagua(textos_marcas, largura_pagina, altura_pagina):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(largura_pagina, altura_pagina))

    # Usando fontes padrão do ReportLab
    for texto, (offset_x, offset_y) in textos_marcas:
        c.setFont("Helvetica-Bold", 50)
        c.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.3)  # 30% de transparência
        c.saveState()
        c.rotate(45)
        c.drawString((largura_pagina / 2) + offset_x, (altura_pagina / 2) + offset_y, texto)
        c.restoreState()

    c.save()
    packet.seek(0)
    return PdfReader(packet)

def adicionar_marca_dagua(pdf_input_path, pdf_output_path, textos_marcas):
    with open(pdf_input_path, "rb") as arquivo_pdf:
        leitor_pdf = PdfReader(arquivo_pdf)
        escritor_pdf = PdfWriter()

        for pagina in leitor_pdf.pages:
            largura_pagina = float(pagina.mediabox.width)
            altura_pagina = float(pagina.mediabox.height)

            marca_dagua_pdf = criar_marca_dagua(textos_marcas, largura_pagina, altura_pagina)
            marca_dagua_pagina = marca_dagua_pdf.pages[0]

            pagina.merge_page(marca_dagua_pagina)
            escritor_pdf.add_page(pagina)

        with open(pdf_output_path, "wb") as arquivo_saida:
            escritor_pdf.write(arquivo_saida)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        texto1 = request.form['texto1']
        texto2 = request.form['texto2']

        if pdf_file:
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)

            output_pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], f"marca_{pdf_file.filename}")
            textos_marcas = [
                (texto1, (0, 100)),
                (texto2, (0, -100))
            ]

            adicionar_marca_dagua(pdf_path, output_pdf_path, textos_marcas)
            return send_file(output_pdf_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
