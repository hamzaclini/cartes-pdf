import streamlit as st
from fpdf import FPDF
from io import BytesIO
import create_pdf

# Load the CSS file
with open("file.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Set the page title and subheader
st.title("Générateur de cartes")
st.subheader("Entrez les questions et les réponses pour générer les cartes")

try:
    # Create a form to add cards
    with st.form(key='cards_form'):
        # Create two columns for questions and answers
        col1, col2 = st.columns([0.5, 0.5], gap="small")
        with col1:
            # Create 8 text areas for questions
            questions = [st.text_area(f"Question:", value=f'Q{i+1} : ', height=100) for i in range(8)]
        with col2:
            # Create 8 text areas for answers
            answers = [st.text_area(f"Réponse:", value=f'R{i+1} : ', height=100) for i in range(8)]

        # Add a submit button to add the cards
        submitted = st.form_submit_button("Ajouter les cartes")

        if submitted:
            # If the session state doesn't exist, create it
            if 'cards' not in st.session_state:
                st.session_state['cards'] = []

            # Add the cards to the session state
            for question, answer in zip(questions, answers):
                st.session_state['cards'].append((question, answer))

            st.success("Cartes ajoutées !")

    # Add a button to generate the PDF
    if st.button("Générer le PDF"):
        # If there are at least 8 cards in the session state, generate the PDF
        if 'cards' in st.session_state and len(st.session_state['cards']) >= 8:
            pdf_file = create_pdf.create_pdf(st.session_state['cards'])
            st.success("PDF généré. Vous pouvez maintenant le télécharger.")
            st.download_button(label="Télécharger le PDF",
                               data=pdf_file,
                               file_name="cartes.pdf",
                               mime='application/pdf')
        else:
            st.error("Ajoutez suffisamment de cartes pour générer un PDF")

    # Add a button to clear the cards
    if st.button("Effacer les cartes"):
        st.session_state.clear()

    # Display a preview of the cards
    st.header("Aperçu")
    if 'cards' not in st.session_state:
        st.write('Cartes réinitialisées.')
    else:
        for q, a in st.session_state["cards"]:
            st.write(f'Question : {q}')
            st.write(f'Réponse : {a}')

    # Load your logo image
    logo = "logo.png"
    st.image(logo, width=400)

except Exception as e:
    st.error(f"Une erreur s'est produite : {str(e)}. Veuillez contacter les développeurs pour assistance.")
