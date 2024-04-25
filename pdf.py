import streamlit as st
from fpdf import FPDF
from io import BytesIO
import create_pdf


st.title("Anki-style Flashcard Generator")
st.subheader("Enter 8 questions and 8 answers to generate flashcards.")

with st.form(key='cards_form'):
    col1, col2 = st.columns([0.5, 0.5], gap="small")
    with col1:
        questions = [st.text_input(f"Question {i+1}:", value=f'Q{i+1}') for i in range(8)]
    with col2:
        answers = [st.text_input(f"Answer {i+1}:", value=f'A{i+1}') for i in range(8)]
    submitted = st.form_submit_button("Add to Cards")

    if submitted:
        if 'cards' not in st.session_state:
            st.session_state['cards'] = []
        for question, answer in zip(questions, answers):
            st.session_state['cards'].append((question, answer))
        st.success("Cards added! You can add more or generate the PDF.")

if st.button("Generate PDF"):
    if 'cards' in st.session_state and len(st.session_state['cards']) >= 8:
        pdf_file = create_pdf.create_pdf(st.session_state['cards'])
        st.success("PDF Generated! You can now download it.")
        st.download_button(label="Download PDF",
                           data=pdf_file,
                           file_name="anki_cards.pdf",
                           mime='application/pdf')
    else:
        st.error("Please add enough cards to generate a PDF (at least 8).")

st.write(st.session_state)

