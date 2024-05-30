import streamlit as st
import pandas as pd
import numpy as np

def bigest_sold(data):
    bigest_sold = data['quantity_sold'].max()    # Recuperation des données de la colonne 'quantity_sold' et calcul du maximum grace a la fonction max()
    bigest_sold_category = data[data['quantity_sold'] == bigest_sold]['category'].values[0]   # Recuperation de la catégorie de la meilleure vente
    st.metric('Meilleure vente global', bigest_sold, bigest_sold_category)   # Affichage de la meilleure vente et de quelle catégorie elle provient

def stats(data):
    col1, col2 = st.columns([1, 1])   # Création de 2 colonnes pour afficher sur la même ligne
    average = data['quantity_sold'].mean()      # Recuperation des données de la colonne 'quantity_sold' et calcul de la moyenne grace a la fonction mean()
    average_book = data[data['category'] == 'Books']['quantity_sold'].mean()   # Recuperation des données de la colonne 'quantity_sold' et calcul de la moyenne pour la catégorie 'Book' grace a la fonction mean()
    mediane = data['quantity_sold'].median()    # Recuperation des données de la colonne 'quantity_sold' et calcul de la mediane grace a la fonction median()
    mediane_book = data[data['category'] == 'Books']['quantity_sold'].median()   # Recuperation des données de la colonne 'quantity_sold' et calcul de la mediane pour la catégorie 'Book' grace a la fonction median()
    with col1:  # Affichage des données dans la première colonne
        st.metric('Moyenne global des ventes', round(average, 2))   # Affichage de la moyenne en l'arrondissant a 2 chiffres après la virgule
    with col2:
        st.metric('Moyenne des ventes de livre', round(average_book, 2))
    with col1:
        st.metric('Mediane global des ventes', round(mediane, 2))   # Affichage de la mediane en l'arrondissant a 2 chiffres après la virgule
    with col2:
        st.metric('Mediane des ventes de livre', round(mediane_book, 2))
    # https://docs.streamlit.io/develop/api-reference/data/st.metric
    bigest_sold(data)

def graph(data):
    st.write('Représentation graphique de la quantité vendue par catégorie')
    st.bar_chart(data.set_index('category')['quantity_sold'], color=(240, 150, 100))   # En triant par catégorie, afficher la quantité vendue
    # https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart

def convert_df(data):
   return data.to_csv(index=False).encode('utf-8')  # Convertir les données en csv

def filter(data):
    # initinialisation des variables de session
    if 'category' not in st.session_state:
        st.session_state.category = None
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    if 'filtered_data' not in st.session_state:
        st.session_state.filtered_data = data
    # https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state

    if st.button('Filtrer'):    # Si le bouton est cliqué
    # https://docs.streamlit.io/develop/api-reference/widgets/st.button
        st.session_state.category = None if st.session_state.category else True # Changer l'etat du bouton a chaque interaction
    if st.session_state.category:   # Si le bouton est activé
        category = st.selectbox('Catégorie', data['category'].unique()) # Selectionner une catégorie et faire en sorte qu'elle soit unique
        if st.button('Go'):
            st.session_state.selected_category = category   # Enregistrer la catégorie selectionnée
            st.session_state.filtered_data = data[data['category'] == category]  # Si la categorie correspond a celle selectionnée, afficher les données correspondantes

    if st.session_state.selected_category and st.session_state.category:    # Si une catégorie est selectionnée et que le bouton filtrer est activé
        st.subheader(f"Données filtrées par catégorie : {st.session_state.selected_category}")
        # https://docs.streamlit.io/develop/api-reference/text/st.subheader
        st.dataframe(st.session_state.filtered_data)
        csv = convert_df(st.session_state.filtered_data)   # Convertir les données filtrées en csv
        st.download_button('Télécharger les données filtrées', csv, 'filtered_data.csv', 'csv')   # Bouton de téléchargement des données filtrées
        # https://docs.streamlit.io/develop/api-reference/widgets/st.download_button

def read_csv(file_path):
    data = pd.read_csv(file_path)    #Lire le csv
    if data is not None:
        st.dataframe(data.head(20))    #Afficher le csv
        # https://docs.streamlit.io/develop/concepts/design/dataframes
    return data


def app():
    st.title('Analyse e-commerce')
    # https://docs.streamlit.io/develop/api-reference/text/st.title
    st.markdown('<h4>Obtenez des statistiques sur votre e-commerce en quelques clics !</h4>', unsafe_allow_html=True)   # Affichage de la description avec une taille de sous titre 4 en html
    # https://docs.streamlit.io/develop/api-reference/text/st.markdown
    data = read_csv('ecommerce_data.csv')
    filter(data)
    graph(data)
    stats(data)


if __name__ == '__main__':
    app()