import os
import platform
import webbrowser
import fpdf
from dataclasses import dataclass

def open_file(filename):
    if platform.system() == 'Darwin':       # macOS
        webbrowser.open_new('file://' + os.path.realpath(filename))
    elif platform.system() == 'Windows':    # Windows
        try:
            os.startfile(filename)
        except:
            webbrowser.open_new('file://' + os.path.realpath(filename))
    else:                                   # linux variants
        webbrowser.open_new('file://' + os.path.realpath(filename))

def prepare_pdf(pdf: fpdf.FPDF):
    pdf.add_page()
    pdf.set_font('Arial', 'B', 11)

def draw_pdf_header(pdf: fpdf.FPDF, data):
    pdf.line(10, 10, 200, 10)
    pdf.line(10, 11, 200, 11)
    pdf.cell(10, 10, f'Listado de {data["title"]}')
    import datetime
    current_date = datetime.datetime.now()
    pdf.set_xy(150, 10)
    pdf.cell(10, 10, f'Fecha: {current_date.day}/{current_date.month}/{current_date.year}')
    pdf.line(10, 18, 200, 18)

