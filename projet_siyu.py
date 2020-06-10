#!/usr/bin/env python3
# coding: utf-8
# Projet personel : Siyu Wang 

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd
import sys
import time
import sys
import requests
from bs4 import BeautifulSoup
import json
import nltk
nltk.download('stopwords')


# ------------------------------- realpython --------------------------------
def scrap_python(recherche):
    """
    Scrape les informations correspondent au mot de recherche
    Entrée : recherche, String, mot de recherche
    Sortie : dict_titles, un dictionnaire avec le titre comme clé, et ses étiquettes correspondantes comme valeur
             cat_dict, un dictionnaire avec le catégorie comme clé, et le nombre d'articles de cette catégorie comme valeur
             dict_liens, un dictionnaire avec le titre comme clé et son lien comme valeur
             tags, une liste de étiquêttes
             nb_total, le nombre total des articles trouvés
    """
    print("---------------- Scraping on realpython website ----------------")

    # crée l'instance driver
    driver = webdriver.Chrome()

    # définit la taille de fenêtre
    driver.set_window_size(1000,30000)

    # définit l'url de recherche
    url = "https://realpython.com/search?q={}".format(recherche)

    # ouvre le site
    driver.get(url)

    time.sleep(2.5)
    print("------------- Searching 'python' on realpython website -------------")

    def get_nb_art():
        """ récupérer le nb d'articles en strong """
        nb_art_trouves = driver.find_elements_by_xpath('/html/body/div/div/div/div/div[1]/div/span/strong')[0]
        nb_int = int(nb_art_trouves.text)
        return nb_int

    # le nb total des articles trouvés
    nb_total = get_nb_art()

    # scroll le site automatiquement pour afficher plus de résultats
    for x in range(1,8):
        js="var q=document.documentElement.scrollTop=130000"  
        driver.execute_script(js) 
        time.sleep(1.8) # en fonction de la vitesse d'internet, à augmenter si l'internet est lent
        print("---scrolling : "+str(x)+"/7---")

    # récupérer les titres et tags
    tags = list()
    dict_titles = dict()
    dict_liens = dict()

    # récupère un échantillon de 35 articles
    for x in range(1,51):
        chemin_titre = '/html/body/div/div/div/div/div[2]/div['+str(x)+']/div/div/div[2]/a'
        chemin_tag = '/html/body/div/div/div/div/div[2]/div['+str(x)+']/div/div/div[2]/p'
        lien_titre = driver.find_elements_by_xpath(chemin_titre)[0]
        lien_tag = driver.find_elements_by_xpath(chemin_tag)[0]
        titre = lien_titre.text
        lien = lien_titre.get_attribute(("href"))
        dict_liens[titre]=lien
        tag = lien_tag.find_elements_by_tag_name('a')
        tag_list = []
        for a in tag:
            t = a.text
            tag_list.append(t)
        dict_titles[titre]=tag_list
        for tg in tag_list:
            if tg not in tags:
                tags.append(tg)

    # initialize la dict des catégories
    cat_dict = dict()

    #clique sur le checkbox niveau 3-7 et récupére le nb d'articles de chaque catégorie
    for i in range(3,8):
        chemin_cat = '/html/body/div/div/div/aside/div/div['+str(i)+']/label'
        catbox = driver.find_elements_by_xpath(chemin_cat)[0]
        action = catbox.click()

        time.sleep(2) # en fonction de la vitesse d'internet, à augmenter si l'internet est lent
        
        cat = catbox.text
        nb_cat = get_nb_art()
        cat_dict[cat] = nb_cat
        action = catbox.click()

        time.sleep(2) 

    # ferme le navigateur
    driver.close()

    dict_tags = dict()
    for t in tags:
        for k,v in dict_titles.items():
            if t in v:
                if t not in dict_tags.keys():
                    dict_tags[t]= [k]
                else:
                    dict_tags[t].append(k)

    return dict_titles, dict_liens, cat_dict, tags, nb_total, dict_tags


def get_tag_cnt(dict_titles, tags):
    """ Compter le nombre de chaque étiquête 
        Return : tag_cnt, un dictionnaire avec l'étiquêtte comme clé, et son nombre de compte comme valeur
    """
    dict_tags = dict()
    for k,v in dict_titles.items():
        for t in tags:
            if t in v:
                if t in dict_tags.keys():
                    dict_tags[t].append(k)
                else:
                    dict_tags[t]=[k]

    tag_cnt = dict()
    for a,b in dict_tags.items():
        tag_cnt[a]=len(dict_tags[a])

    return tag_cnt


# ------------------------------- stackoverflow --------------------------------
def scrap_stack(recherche):
    """
    Scrape les informations correspondent au mot de recherche
    et les rend accessible avec le parseur beautifulsoup
    Entrée : recherche, String, mot de recherche
    Sortie : nb_search, le nombre des résultats trouvés
             dict_result, un dictionnaire avec url comme clé, et ses étiquettes correspondantes comme la valeur
    """
    print("------------ Scraping on stackoverflow website ------------")

    # crée l'instance driver
    driver = webdriver.Chrome()

    # définit la taille de fenêtre
    driver.set_window_size(1000,30000)

    # définit l'url de recherche
    url = "https://stackoverflow.com/search?q={}".format(recherche)

    # ouvre le site
    driver.get(url)
    time.sleep(1)

    # récupère le nombre de résultats trouvés
    nb_results = driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[1]/div[3]/div[1]')[0]
    nb_search = nb_results.text

    # récupère les 15 premieres questions les plus pertinentes
    dict_result = dict()
    for i in range(1,16):
        chemin = '/html/body/div[4]/div[2]/div[1]/div[4]/div/div['+str(i)+']/div[2]/div[1]/h3'
        link_chemin = '/html/body/div[4]/div[2]/div[1]/div[4]/div/div['+str(i)+']/div[2]/div[1]/h3/a'
        result = driver.find_elements_by_xpath(chemin)[0]
        link = driver.find_elements_by_xpath(link_chemin)[0]
        dict_result[result.text] = link.get_attribute(("href"))

    # fermer le navigateur
    driver.close()

    return nb_search, dict_result


# ---------------------------- Traitement commun ----------------------------
def save_to_html(page,path):
    with open(path, "w") as f:
        f.write(str(page.text))

def save_to_json(chemin, dict_x):
    with open(chemin, 'w') as fp:
        json.dump(dict_x, fp)

def get_pages(dict_lien,chemin):
    for t,l in dict_lien.items():
        print(l)
        page = requests.get(l)
        f_name = l.split('/')[4]
        path = chemin+f_name+".html"
        save_to_html(page,path)
        
# ------------------------------- main ------------------------------

if __name__ == "__main__":
    dict_titles, dict_lien, cat_dict, tags, nb_total, dict_tags = scrap_python('python')
    tag_cnt = get_tag_cnt(dict_titles, tags)

    save_to_json('./json/dict_titles.json',dict_titles)
    save_to_json('./json/dict_lien.json',dict_lien)
    save_to_json('./json/cat_dict.json',cat_dict)
    save_to_json('./json/dict_tags.json',dict_tags)
    save_to_json('./json/tag_cnt.json',tag_cnt)

    # récupérer 35 pages de real python
    print('------ downloading from realpython: ---------')
    get_pages(dict_lien, "./html_realpython/")

    # récupérer 15 pages de stack overflow
    nb_results, dict_result = scrap_stack("debug python")
    print('------ downloading from stackoverflow: ---------')
    # sauvegarde les fichiers
    save_to_json('./json/dict_result.json',dict_result)
    get_pages(dict_result, "./html_stackoverflow/")

    print('------  Scraping finished ------')
