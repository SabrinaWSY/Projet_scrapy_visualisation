
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import json
from selenium import webdriver
import glob
from bs4 import BeautifulSoup
from collections import Counter
import re
import string
from nltk.corpus import stopwords


# ---------------------------- traitement fichiers et données -----------------------------
def load_json(js_file):
    with open(js_file, 'r') as fp:
        data = json.load(fp)
        return data

def get_cnt_echant(dict_titles):
    keywords=list()
    cats = list()
    for k in dict_titles.keys():
        if ':' in k:
            cat = k.split(':')[0]
            cats.append(cat)
            keywords = keywords+(k.split(':')[1]).split()
        else:
            cats.append('None')
            keywords = keywords+k.split()

    # supprime les ponctuations
    keywords = [''.join(c for c in s if c not in string.punctuation) for s in keywords]
    keywords = [s.strip('›') for s in keywords]
    # supprime les strings vides
    keywords = [s.lower() for s in keywords if s]
    # supprime stopwords
    keywords = [word for word in keywords if not word in stopwords.words()]
    # supprime les chiffres
    keywords = [s for s in keywords if s.isalpha()]
    # supprime les mots innutiles
    keywords = [s for s in keywords if s not in ['cant','good','cli','closed','make','way']]
    cnt_cats = Counter(cats)
    cnt_keywords = Counter(keywords)
    return cnt_cats,cnt_keywords


# ------------------------------- outil streamlit ------------------------------

def processbar():
    """ Add a process bar """
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
    # Update the progress bar with each iteration.
        latest_iteration.text(f'Progressing {i+1} %')
        bar.progress(i + 1)
        time.sleep(0.01)
        
def draw_donut_chart(dict_x):
    labels = list()
    values = list()
    for a,b in dict_x.items():
        labels.append(a)
        values.append(b)
    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.write(fig)

# ------------------------------- ntealan ------------------------------
def scrap_ntealan(recherche):   
    """
    Scrape les paires de dictionnaire et la traduction correspondent au mot de recherche
    Entrée : recherche, String, mot de recherche
    Sortie : nb_search, le nombre des résultats trouvés
             dict_result, un dictionnaire avec url comme clé, et ses étiquettes correspondantes comme la valeur
    """
    # import le module Keys
    from selenium.webdriver.common.keys import Keys

    print("------------ Scraping on ntealan website ------------")

    # crée l'instance driver
    driver = webdriver.Chrome()

    # définit la taille de fenêtre
    driver.set_window_size(1000,30000)

    # définit l'url de recherche
    url = "https://ntealan.net/dictionaries/content/fr-af/yb_fr_3031"

    # ouvre le site
    driver.get(url)
    time.sleep(1.3)

    # ferme l'annonce de covid-19
    if driver.find_element_by_xpath('//*[@id="dialInfo"]/div/div/div[2]/button'):
        driver.find_element_by_xpath('//*[@id="dialInfo"]/div/div/div[2]/button').click()

    # laisser le temps de réagir
    time.sleep(1.1)
    
    # cliquer dans la zone de text puis envoyer le mot saisi par l'utilisateur comme mot de recherche
    driver.find_element_by_id("myKeypad").click()
    driver.find_element_by_id("myKeypad").send_keys(recherche)
    driver.find_element_by_id("myKeypad").send_keys(Keys.ENTER)

    # laisser le temps de réagir
    time.sleep(1.5)

    # stocker les propositions de traduction dans un dictionnaire avec le mot comme clé et son POS comme valeur
    dict_traduction = dict()
    word_chemin = driver.find_elements_by_xpath("//app-bar-left/div/div[2]/div[1]/div/ul")[0]
    wordlist = word_chemin.find_elements_by_tag_name("li")
    for i in wordlist:
        w = i.find_elements_by_tag_name("a")
        for x in w :
            mot = x.find_elements_by_tag_name("div")[0]
            pos = x.find_elements_by_tag_name('h6')[0]
            dict_traduction[mot.text]=pos.text

    # fermer le navigateur
    driver.close()

    return dict_traduction


# ------------------------------- main ------------------------------
if __name__ == "__main__":

    # charge les fichiers locaux
    dict_titles = load_json('./json/dict_titles.json')
    dict_lien = load_json('./json/dict_lien.json')
    cat_dict = load_json('./json/cat_dict.json')
    dict_tags = load_json('./json/dict_tags.json')
    tag_cnt = load_json('./json/tag_cnt.json')
    dict_result = load_json('./json/dict_result.json')
    list_htmls = glob.glob('./html_realpython/*.html')

    # ----------------- streamlit ----------------

    # Page d'acceuil du projet
    st.title('Visualisation du Projet Scrape&See')
    st.sidebar.header("Techniques web - Projet ")
    st.sidebar.info('Auteur : Siyu WANG')
    st.sidebar.info('N° étudiant : 21800525')
    st.info('Bienvenu(e) sur notre site de présentation !')

    # Radio selector sur sidebar pour aller aux pages différentes
    st.sidebar.header("Votre sélection :")
    radio = st.sidebar.radio(label="", options=[ "Présentation", "Real python","Stack overflow", "Ntealan"])

    # Si bouton 'Présentation' sélectionné
    if radio == "Présentation":
        st.markdown("## Présentation du projet ")
        st.markdown("Cette application Scrape&See permet à nos chers clients de découvrir les possibilités de conquérir de nouveaux domaines technologiques où ils pourraient investir et diversifier ainsi leurs activités.")
        st.markdown("### À gauche dans le sidebar, vous trouverez 4 boutons à sélectionner pour aller à la page correspondante: ")
        df_presentation = pd.DataFrame({'Thème': ['Présentation du projet','Débogage Python', '','Aide à Traduction'], 'Bouton': ['Présentation','Real Python', 'Over Stackflow', 'Ntealan']})
        st.dataframe(df_presentation)
        st.markdown("**♟ Python ♟**")
        st.markdown("Cette partie s'agit d'une visualisation de la partie d'extraction pour montrer la possibilité d'aider au développement logiciel dont l’objectif sera la recherche automatique de solution de débogage qui pourraient aider le développeur Python à optimiser son rendement professionnel.")
        
        st.markdown("*** - Real Python ***")
        st.markdown("Cette page éffectue la recherche sur python et récupère toutes les catégories, les titres, les liens, et les étiquêttes de chaques block des résultats de recherche sur le site  https://realpython.com.")
        st.markdown("Notre application vosu présentera des graphes pour visualiser facilement les données analysées.")
        st.markdown("Vous pouvez également consulter les articles pertinentes directement sur notre application.")

        st.markdown("*** - Stack Overflow ***")
        st.markdown("Le site de Stack Overflow permet aux developpeurs de poser des questions sur leurs problèmes rencontrés pour déboger.")
        st.markdown("Notre application analysera les contenus trouvés sur le site.")

        st.markdown("**♟ Ntealan ♟**")
        st.markdown("Cette partie consiste à soutienir la communauté des bénévoles travaillant sur les langues peu-dotées, dans l’objectif de créer un marché de la donnée autour de ces langues. ")
        st.markdown("Ici, la présentation concerne une traduction de mot automatique en recherchant le mot dans le dictionnaire en ligne.")

        st.write(" <--- Veuillez sélectionner un bouton pour commencer !")
        

    # Si bouton 'Real python' sélectionné
    elif radio == "Real python":
        st.markdown("## Real Python ")
        st.markdown("### Articles autour du thème 'python'")

        # ----------- table et pie chart par catégorie -------------
        df = pd.DataFrame(list(cat_dict.items()),columns = ["Catégorie","Nombre"]) 
        st.dataframe(df)

        fig = px.pie(df, values='Nombre', names='Catégorie', title="Répartition de tous les articles par catégorie :")
        st.write(fig)

        # ----------------- analyse d'échantillion -------------------------------
        st.markdown("### Sur un échantillion de 50 articles récupérés:")
        st.markdown("#### Répartition d'articles trouvés par étiquêttes : ")
        # ----------- donut chart par étiquette  ------------
        draw_donut_chart(tag_cnt)

        # --------- count par categorie ------------
        st.markdown("#### Répartition d'articles trouvés par catégorie dans le titire : ")
        cnt_cats,cnt_keywords = get_cnt_echant(dict_titles)
        df_e = pd.DataFrame(list(cnt_cats.items()),columns = ["Catégorie","Nombre"]) 
        fig3 = px.bar(df_e, x='Catégorie', y='Nombre')
        st.write(fig3)
        df_mot = pd.DataFrame(list(cnt_keywords.items()),columns = ["Mot","Fréquence"])
        fig4 = px.bar(df_mot, x='Mot', y='Fréquence')
        fig4.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig4.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.markdown("#### Répartition de mots clés : ")
        st.write(fig4)

        # ----------- liens des articles d'échantillons ------------
        st.markdown("### Les articles les plus pertinentes de votre recherche : ")
        for y in range(10):
            st.markdown("** "+list(dict_lien.keys())[y]+"** ")
            st.markdown("- "+list(dict_lien.values())[y])

        print("----------- Real python : streamlit page générée avec succès --------------")


    # Si bouton 'Stack overflow' sélectionné
    elif radio == "Stack overflow":
        st.markdown("## Stack Overflow ")
        st.markdown("### Un échantillion de 15 résultats sur 'debug python'")
        st.markdown("#### Répartition des résultats par TYPE : ")
        st.markdown('- Q : Type question pertinente lié à la recherche')
        st.markdown('- A : Type réponse pertinent lié à la recherche')
        cnt_cats,cnt_keywords = get_cnt_echant(dict_result)

        # bar chart : répartition par type
        df_cat = pd.DataFrame(list(cnt_cats.items()),columns = ["Type","Nombre"]) 
        fig1 = px.bar(df_cat, x='Type', y='Nombre')
        st.write(fig1)

        # donut chart : répartition des mots
        st.markdown("#### Répartition des mots clés : ")
        draw_donut_chart(cnt_keywords)

        st.markdown("### Les 15 questions plus pertinentes : ")

        for k,v in dict_result.items():
            st.markdown("** "+k+"** ")
            st.markdown("- "+str(v))
        print("----------- Stack overflow : streamlit page générée avec succès --------------")

    # Si bouton 'Ntealan' sélectionné
    elif radio == "Ntealan":
        st.markdown("## Ntealan ")
        st.write("Un outil pour faciliter votre travail de traduction ;)")
        
        st.markdown("#### À vous de jouer : cliquer sur 'Traduire' pour éffectuer la recherche ")
        st.warning("Attention : notre application fait tourner votre navigateur automatiquement, veuillez attendre la fermeture automatique du navigateur pour visualiser les résultats.")
        # récupérer le mot à traduire par l'utilisateur
        user_input = st.text_input("Saisissez un mot en français à traduire en yemba : ", "repas")

        # le bouton 'Traduire' cliqué pour faire la recherche
        if st.button('Traduire'):
            try:
                dict_traduction = scrap_ntealan(user_input)
                processbar()
                st.write("Nombre de proposition trouvé : "+str(len(dict_traduction)))
                st.markdown("#### Mot à traduire : "+user_input)
                st.write("- Proposition pour la traduction en Yemba: ")
                df = pd.DataFrame(list(dict_traduction.items()),columns = ["Traduction proposée","POS"]) 
                st.dataframe(df)
                print("----------- Ntealan : streamlit page générée avec succès --------------")
            
            # Éviter le message d'érreur si zéro proposition trouvée
            except IndexError as e:
                st.warning("Désolé ! \n Le mot' "+user_input+ "' n'a aucune entrée dans le dictionnaire.")
