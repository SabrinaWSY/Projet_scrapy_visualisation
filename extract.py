import requests
import fake_useragent
from bs4 import BeautifulSoup

#print(requests.utils.default_user_agent())

franceinfo = requests.get("https://www.francetvinfo.fr/")
lemonde = requests.get("https://www.lemonde.fr/recherche/?search_keywords=coronavirus&start_at=19%2F12%2F1944&end_at=12%2F03%2F2020&search_sort=relevance_desc")


#print(franceinfo.text)
#print(lemonde.text)
def scrap_wikipedia(recherche):
    url = "http://wikipedia.fr/Resultats.php?q={}&projet=article".format(recherche)
    wikipedia = requests.get(url)
    html_wiki = BeautifulSoup(wikipedia.text, 'html.parser')
    contenu_left = html_wiki.findChild("div", attrs={"id": "contenu_left"})
    content = contenu_left.findChild("p", attrs={"class":"style1", "style":"text-align: left"})
    for child in content.children:
        print(child)
        a_list =  []
        br_list = []
        if child.name == "br":
            br_list.append(child)
        if child.name == "a":
            a_list.append(child)
    
    for a, b in zip(a_list[:5], br_list[:5]):
        print("{:>5} {:>5}".format(a, b))
        

def scrap_lemonde(recherche):
    url = "https://www.lemonde.fr/recherche/?search_keywords={}".format(recherche)
    lemonde = requests.get(url)
    html_lemonde = BeautifulSoup(lemonde.text,'html.parser')
    contenu_recherche = html_lemonde.findChild("section",attrs={"class":"js-river-search"})
    #print(dir(contenu_recherche))
    list_titles = list()
    list_des = list()
    for section in contenu_recherche.children:

        if section.name == "section":
            if section.a:
                print("----------------------")
                title = section.a.h3.get_text()
                description = section.a.p.get_text()
                list_titles.append(title)
                list_des.append(description)
                # print(title)
                # print("***")
                # print(description)

    streamlit.sidebar.header("Scrapy le monde")
    streamlit.sidebar.info("Exos pour extraction d'information concernant le coronavirus")
    streamlit.error("errorrrrr")
    streamlit.title("Exo scrapy le monde coronavirus title et description")

    # for a, b in zip(list_titles[:5], list_des[:5]):
    #     print("{:>5} {:>5}".format(a, b))
    #return list_titles,list_des


def test_get():
    data = requests.get("https://ntealan.net/dictionaries-platform")
    print(data.text)


def scrap_spa(recerche):
    from selenium.webdriver import Firefox, Chrome
    from selenium.webdriver.firefox.options import Options as fireOptions
    from selenium.webdriver.chrome.options import Options as chromeOptions
    opts = chromeOptions()
    opts.set_headless()
    opts.add_argument("--remote-debugging-port=9222")
    browser = Chrome(options=opts)
    url = "https://ntealan.net/dictionaries-platform"
    browser.get(url)
    #print(browser.save_screenshot('ntealan.png'))
    # recherche l'élément body dans la page
    #body = browser.find_element_by_tag_name('body')
    #open("body_ntealan.html", 'w').write(body.get_attribute("outerHTML"))

    browser.get('https://duckduckgo.com')
    search_form = browser.find_element_by_id('search_form_input_homepage')
    search_form.send_keys('voiture')
    search_form.submit()
    print(search_form.get_attribute("outerHTML"))
    #print(dir(body))


if __name__ == "__main__":
    # recherche = {
    #     'modele': 0, 'prixMax': 0, 'depart': 0,
    #     'prixMin': 0, 'city': 0, 'distance': 0,
    #     'kmMax': 0, 'modele': 0, 'page': 0
    # }
    #titles,descriptions = scrap_lemonde("coronavirus")
    scrap_lemonde("coronavirus")
    #test_get()
    #scrap_wikipedia("voiture")
    #scrap_spa(recherche)