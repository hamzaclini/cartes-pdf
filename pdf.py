import pandas as pd
import streamlit as st
import create_pdf
import openpyxl

st.title("Générateur de cartes")
if 'cards' not in st.session_state:
    st.session_state['cards'] = []

if st.toggle('Utiliser un fichier Excel comme source'):
    uploaded_file = st.file_uploader("Upload fichier Excel avec Q/R", type=['xlsx'],
                                     help="Header du fichier excel : deck, numeroInitialQuestion, question, reponse")
    if uploaded_file is not None:
        st.session_state['uploaded_file_name'] = uploaded_file.name
        data = pd.read_excel(uploaded_file).values.tolist()
        if st.button("Ajouter les questions"):
            for deck, i, question, answer in data:
                st.session_state['cards'].append((f'Q{i} : {question}', f'R{i} : {answer}'))
else:
    st.subheader("Entrez les questions et les réponses pour générer les cartes")

    with st.form(key='cards_form'):
        col1, col2 = st.columns([0.5, 0.5], gap="small")
        with col1:
            questions = [st.text_area(f"Question:", value=f'Q{i+1} : ', height=100) for i in range(8)]
        with col2:
            answers = [st.text_area(f"Réponses:", value=f'R{i+1} : ', height=100) for i in range(8)]
    submitted = st.form_submit_button("Ajouter les cartes")

    if submitted:
        for question, answer in zip(questions, answers):
            st.session_state['cards'].append((question, answer))
        st.success("Cartes ajoutées !")

if st.button("Générer le PDF"):
    if 'cards' in st.session_state and len(st.session_state['cards']) >= 1:
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