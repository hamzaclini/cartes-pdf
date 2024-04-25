import streamlit as st
from fpdf import FPDF
from io import BytesIO

def create_pdf(cards):
    pdf = FPDF()
    card_width = 95
    card_height = 54
    margin = 10
    
    # Create a page for questions
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for index in range(min(8, len(cards))):  # Generate up to 8 cards
        question = cards[index][0]
        x = margin + (index % 2) * (card_width + margin)
        y = margin + (index // 2 % 4) * (card_height + margin)
        pdf.set_xy(x, y)
        pdf.cell(card_width, card_height, border=1)
        pdf.set_xy(x + 5, y + 5)
        pdf.cell(card_width - 10, 10, f"Q {index + 1}:", ln=True)
        pdf.set_xy(x + 5, y + 15)
        pdf.multi_cell(card_width - 10, 10, question)  # Auto line break for text that exceeds the line width

    # Create a page for answers, swap positions as specified
    pdf.add_page()
    swap_map = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6}  # Swap mapping
    for index in range(min(8, len(cards))):
        swapped_index = swap_map[index]
        answer = cards[swapped_index][1]
        x = margin + (index % 2) * (card_width + margin)
        y = margin + (index // 2 % 4) * (card_height + margin)
        pdf.set_xy(x, y)
        pdf.cell(card_width, card_height, border=1)
        pdf.set_xy(x + 5, y + 5)
        pdf.cell(card_width - 10, 10, f"R {swapped_index + 1}:", ln=True)
        pdf.set_xy(x + 5, y + 15)
        pdf.multi_cell(card_width - 10, 10, answer)  # Auto line break for text that exceeds the line width

    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)
    return pdf_output


def main():
    st.title("Générateur de cartes flash Anki")
    st.subheader("Entrez 8 questions et 8 réponses pour générer des cartes flash.")

    with st.form(key='cards_form'):
        # Create a list to store questions and answers
        questions = []
        answers = []
        
        # Use columns to place questions and answers side by side
        for i in range(8):
            col1, col2 = st.columns(2)
            with col1:
                question = st.text_input(f"Question {i+1}:", key=f"q{i}")
            with col2:
                answer = st.text_input(f"Réponse {i+1}:", key=f"a{i}")
            questions.append(question)
            answers.append(answer)
        
        submitted = st.form_submit_button("Ajouter les cartes")
        if submitted:
            # Store pairs of questions and answers in session state
            if 'cards' not in st.session_state:
                st.session_state['cards'] = []
            for q, a in zip(questions, answers):
                st.session_state['cards'].append((q, a))
            st.success("Cartes ajoutées! Vous pouvez générer le PDF maintenant.")

    if st.button("Générer le PDF"):
        if 'cards' in st.session_state and len(st.session_state['cards']) >= 8:
            pdf_file = create_pdf(st.session_state['cards'])
            st.success("PDF généré! Vous pouvez maintenant le télécharger.")
            st.download_button(label="Télécharger le PDF",
                               data=pdf_file,
                               file_name="cartes_flash_anki.pdf",
                               mime='application/pdf')
        else:
            st.error("Veuillez ajouter suffisamment de cartes pour générer un PDF (au moins 8).")

if __name__ == "__main__":
    main()