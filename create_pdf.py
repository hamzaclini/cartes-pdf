'''
Methods to generate the pdf from submitted questions
'''

import streamlit as st
from fpdf import FPDF
from fpdf import Template
from io import BytesIO

def create_pdf(cards):
    pdf = Template(format="A4", orientation="P", title="ANKICards", author="Clinicog")
    pdf.parse_csv("ANKIClinicogDOS.csv", delimiter=';')
    pdf.add_page()
    pdf["logo"] = "logo.png"
    for index in range(min(8, len(cards))):
        pdf[f"textq{index+1}"] = cards[index][0]
    pdf.add_page()
    pdf["logo"] = "logo.png"
    swap_map = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6}
    for index in range(min(8, len(cards))):
        swapped_index = swap_map[index]
        pdf[f"textq{index+1}"] = cards[swapped_index][1]
    pdf.render("test.pdf")
    pdf_output = BytesIO()
    pdf_output.write(pdf.pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)
    return pdf_output