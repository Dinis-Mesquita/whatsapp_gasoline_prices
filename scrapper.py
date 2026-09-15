import requests
from bs4 import BeautifulSoup
import json
import re
import datetime

headers = {"User-Agent": "Mozilla/5.0"}


def variation_in_sentence(sentence):
    if "Subida" in sentence:

        var = "+"
        value = re.search(r"\d*\,\d*", sentence)
        value = value.group(0)

    elif "Descida" in sentence:
        var = "-"
        value = re.search(r"\d*\,\d*", sentence)
        value = value.group(0)

    else:
        var= None
        value= None

    return var, value


def scrapper_main_page():

    search_url = "https://www.maisgasolina.com/"

    response = requests.get(search_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    #print(soup.prettify())
    main = soup.body.main

    resume = {}
    for sec in main.contents[2].div.ul.find_all("li"):

        atritbutes = sec.span.attrs
        #print(atritbutes)

        fuel = atritbutes['title']
        price = atritbutes['data-price'].replace(".",",")

        price_change = sec.contents[2].get_text()

        changes={}
        changes['current_price'] =price
        changes['price_change'] = price_change


        resume[fuel] = changes


    #print(resume)
    date = datetime.datetime.now()
    #_{date.day}_{date.month}_{date.year}
    with open(f"last_precos_medios.json", "w", encoding="utf-8") as f:
        json.dump(resume, f, indent=4, ensure_ascii=False)


    texto_final="PREÇOS MÉDIOS DOS COMBUSTÍVEIS\n"
    for cat in resume:
        variation_in_sentence(resume[cat]['price_change'])


        if resume[cat]["price_change"] == "Preço sem alterações":
            texto_final += f"{cat} : {resume[cat]['current_price']}\n"

        else:
            var, price = variation_in_sentence(resume[cat]['price_change'])
            texto_final += f"{cat} : {resume[cat]['current_price']} ({var}{price} cênt.)\n"


    return texto_final

