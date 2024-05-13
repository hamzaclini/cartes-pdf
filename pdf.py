import streamlit as st
from fpdf import FPDF
from io import BytesIO
import create_pdf

st.title("Générateur de cartes")
st.subheader("Entrez les questions et les réponses pour générer les cartes")

with st.form(key='cards_form'):
    col1, col2 = st.columns([0.5, 0.5], gap="small")
    with col1:
        questions = [st.text_area(f"Question:", value=f'Q{i+1} : ', height=100) for i in range(8)]
    with col2:
        answers = [st.text_area(f"Réponses:", value=f'R{i+1} : ', height=100) for i in range(8)]
    submitted = st.form_submit_button("Ajouter les cartes")

    if submitted:
        if 'cards' not in st.session_state:
            st.session_state['cards'] = []
        for question, answer in zip(questions, answers):
            st.session_state['cards'].append((question, answer))
        st.success("Cartes ajoutées !")

if st.button("Générer le PDF"):
    if 'cards' in st.session_state and len(st.session_state['cards']) >= 8:
        pdf_file = create_pdf.create_pdf(st.session_state['cards'])
        st.success("PDF généré. Vous pouvez maintenant le télécharger.")
        st.download_button(label="Télécharger PDF",
                           data=pdf_file,
                           file_name="cartes.pdf",
                           mime='application/pdf')
    else:
        st.error("Ajouter suffisamment de cartes pour générer un PDF.")
if st.button("Effacer les cartes"):
    st.session_state.clear()

st.header("Aperçu")
if 'cards' not in st.session_state:
    st.write('Cards cleared.')
else:
    for q, a in st.session_state["cards"]:
        st.write(f'Question : {q}')
        st.write(f'Réponse : {a}')

st.write(st.session_state)