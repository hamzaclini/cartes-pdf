# coding: utf8
'''
Methods to generate the pdf from submitted questions
'''

import streamlit as st
from fpdf import FPDF, Template
from io import BytesIO

def create_pdf(cards):
    tmpl = Template(format="A4", orientation="P", title="Flashcards", author="Clinicog")
    tmpl.parse_csv("TemplateClinicog2.csv", delimiter=';', encoding='utf-8')
    tmpl.add_page()
    tmpl.pdf.add_font(family='DejaVuSans', style='', fname='font/DejaVuSans.ttf')
    tmpl.pdf.add_font(family='Eunjin', style='', fname='font/Eunjin.ttf')
    tmpl.pdf.add_font(family='Fireflysung', style='', fname='font/fireflysung.ttf')
    tmpl.pdf.set_fallback_fonts(["Eunjin", "Fireflysung"])
    tmpl["logo"] = "logo.png"
    for index in range(min(8, len(cards))):
        tmpl[f"textq{index+1}"] = cards[index][0]
    tmpl.add_page()
    tmpl["logo"] = "logo.png"
    swap_map = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6}
    for index in range(min(8, len(cards))):
        swapped_index = swap_map[index]
        tmpl[f"textq{index+1}"] = cards[swapped_index][1]
    tmpl.render(outfile="test.pdf")
    pdf_output = BytesIO()
    pdf_output.write(tmpl.pdf.output())
    pdf_output.seek(0)
    return pdf_output

if __name__ == "__main__":
    cartes = [('Question1 : 안녕하세요 ', 'Réponse1 : 你好世界'),
              ('Question2 : こんにちは世界', 'Réponse2'),
              ('Question3', 'Réponse3'),
              ('Question4', 'Réponse4'),
              ('Question5', 'Réponse5'),
              ('Question6', 'Réponse6'),
              ('Question7', 'Réponse7'),
              ('Question8', 'Réponse8')]
    create_pdf(cartes)
    print(cartes[0][0])