'''
Methods to generate the pdf from submitted questions
'''

import streamlit as st
from fpdf import FPDF
from fpdf import Template
from io import BytesIO

def create_pdf(cards):
    pdf = Template(format="A4", orientation="P", title="Flashcards", author="Clinicog")
    pdf.parse_csv("TemplateClinicog.csv", delimiter=';')
    pdf.add_page()
    pdf["logo"] = "logo.png"
    for index in range(min(8, len(cards))):
        pdf.set_font("Arial", size=14)
        pdf.set_xy(pdf.get_x() + (pdf.epw - pdf.get_string_width(cards[index][0])) / 2, pdf.get_y() + 30)
        pdf.cell(0, 10, txt=cards[index][0], border=0, ln=True, align='C')
    pdf.add_page()
    pdf["logo"] = "logo.png"
    swap_map = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6}
    for index in range(min(8, len(cards))):
        swapped_index = swap_map[index]
        pdf.set_font("Arial", size=14)
        pdf.set_xy(pdf.get_x() + (pdf.epw - pdf.get_string_width(cards[swapped_index][1])) / 2, pdf.get_y() + 30)
        pdf.cell(0, 10, txt=cards[swapped_index][1], border=0, ln=True, align='C')
    pdf.render("test.pdf")
    pdf_output = BytesIO()
    pdf_output.write(pdf.pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)
    return pdf_output



