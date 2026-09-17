import requests
from bs4 import BeautifulSoup
import json
import re
import datetime

headers = {"User-Agent": "Mozilla/5.0"}


def variation_in_sentence(sentence):
    if "Subida" in sentence:

        var = "+"
        value = re.search(r"\d+\,*\d*", sentence)
        value = value.group(0)

    elif "Descida" in sentence:
        var = "-"
        value = re.search(r"\d+\,*\d*", sentence)
        value = value.group(0)

    else:
        var= None
        value= None


    return var, value


def avr_prices():

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
        price = float(atritbutes['data-price'])


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


        if resume[cat]["price_change"] == "Preço sem alterações":
            texto_final += f"{cat} : {resume[cat]['current_price']}\n"

        else:
            var, price = variation_in_sentence(resume[cat]['price_change'])
            texto_final += f"{cat} : {resume[cat]['current_price']} ({var}{price} cênt.)\n"

    #print(texto_final)
    return texto_final

def avr_prices_by_brand(limit):

    search_url = "https://www.maisgasolina.com/"

    response = requests.get(search_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    #print(soup.prettify())
    main = soup.body.main

    resume = {}
    for sec in main.contents[4].ul.find_all("li"):
        #print(sec.prettify())
        try:
            values={}
            brand =sec.div.a.text
            #print(brand.text)


            for fuel in sec.contents[1].find_all("span"):
                atributes = fuel.attrs


                values[atributes['title']] = float(atributes['data-price'])


        except AttributeError:
            continue

        resume[brand] = values

    #print(resume)


    date = datetime.datetime.now()
    #_{date.day}_{date.month}_{date.year}
    with open(f"last_precos_medios_marca.json", "w", encoding="utf-8") as f:
        json.dump(resume, f, indent=4, ensure_ascii=False)


    texto_final=f"TOP {limit} PREÇOS MÉDIOS DOS COMBUSTÍVEIS POR MARCA\n(Ordenado por preço de gasolina)"


    for i, cat in enumerate(resume):

        if i > limit - 1:
            break
        else:
            texto_final +=f"\n\n{cat}\n"



            for fuel in resume[cat]:
                texto_final +=f"•{fuel}: {resume[cat][fuel]}\n"




    #print(texto_final)
    return texto_final




if __name__ == '__main__':
    avr_prices()