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
    return texto_final, resume

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


                values[atributes['title']] = float(atributes['data-price']) if atributes['data-price']!= "0" else "---"


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
                texto_final +=f"•{fuel}: {str(resume[cat][fuel]).replace('.',',')}€\n"




    #print(texto_final)
    return texto_final, resume

def avr_prices_distritos():

    search_url = f"https://www.maisgasolina.com/lista-de-postos/"
    response = requests.get(search_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    #print(soup.prettify())
    lista_distritos = soup.body.main.div.ul
    resume={}

    for sec in lista_distritos.find_all('li'):
        values = {}
        distrito = sec.a.text
        postos = sec.span.text
        values['Postos'] = postos

        for fuel in sec.div.find_all('span'):
            atributes = fuel.attrs
            values[atributes['title']] = float(atributes['data-price']) if atributes['data-price'] != "0" else "---"


        resume[distrito] = values

    #print(resume)
    with open(f"distritos_media.json", "w", encoding="utf-8") as f:
        json.dump(resume, f, indent=4, ensure_ascii=False)


    texto_final=f"PREÇOS MÉDIOS DOS COMBUSTÍVEIS POR DISTRITO\n"


    for cat in resume:

            texto_final +=f"\n\n{cat}\n"

            for val in resume[cat]:
                if val == "Postos":
                    texto_final += f"({resume[cat][val]})\n"
                else:
                    texto_final +=f"•{val}: {str(resume[cat][val]).replace('.',',')}€\n"

    #print(texto_final)
    return texto_final, resume

def avr_price_specific_distrito(distrito):
    _, resume =  avr_prices_distritos()
    texto_final = f"PREÇOS MÉDIOS DOS COMBUSTÍVEIS EM {distrito.upper()}\n"
    for cat in resume:
            if cat.upper() == distrito.upper():
                for val in resume[cat]:
                    if val == "Postos":
                        texto_final += f"({resume[cat][val]})\n"
                    else:
                        texto_final +=f"•{val}: {str(resume[cat][val]).replace('.',',')}€\n"

    #print(texto_final)
    return texto_final, resume
def avr_prices_concelhos(distrito):

    search_url = f"https://www.maisgasolina.com/lista-de-postos/{distrito.replace(' ','-')}/"
    response = requests.get(search_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    #print(soup.prettify())
    lista_concelhos = soup.body.main.div.ul
    resume={}

    for sec in lista_concelhos.find_all('li'):
        values = {}
        concelho = sec.a.text
        postos = sec.span.text
        values['Postos'] = postos

        for fuel in sec.div.find_all('span'):
            atributes = fuel.attrs
            values[atributes['title']] = float(atributes['data-price']) if atributes['data-price'] != "0" else "---"


        resume[concelho] = values

    #print(resume)
    with open(f"distritos_media.json", "w", encoding="utf-8") as f:
        json.dump(resume, f, indent=4, ensure_ascii=False)


    texto_final=f"PREÇOS MÉDIOS DOS COMBUSTÍVEIS POR CONCELHO NO DISTRITO DE {distrito.upper()}\n"


    for cat in resume:

            texto_final +=f"\n\n{cat}\n"

            for val in resume[cat]:
                if val == "Postos":
                    texto_final += f"({resume[cat][val]})\n"
                else:
                    texto_final +=f"•{val}: {str(resume[cat][val]).replace('.',',')}€\n"

    #print(texto_final)
    return texto_final, resume


def avr_price_specific_concelho(distrito, concelho):
    _, resume =  avr_prices_concelhos(distrito)
    texto_final = f"PREÇO MÉDIO DOS COMBUSTÍVEIS EM {concelho.upper()} ({distrito.upper()})\n"
    for cat in resume:
            if cat.upper() == concelho.upper():
                for val in resume[cat]:
                    if val == "Postos":
                        texto_final += f"({resume[cat][val]})\n"
                    else:
                        texto_final +=f"•{val}: {str(resume[cat][val]).replace('.',',')}€\n"

    #print(texto_final)
    return texto_final, resume


def prices_concelho(distrito, concelho):

    search_url = f"https://www.maisgasolina.com/lista-de-postos/{distrito.replace(' ','-')}/{concelho.replace(' ','-')}"

    response = requests.get(search_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup.prettify())
    lista_postos = soup.body.main.div.ul


    resume={}

    for sec in lista_postos.find_all('li'):
        values = {}
        posto = sec.a.text
        #print(posto)
        #print(posto.find("span", class_="updated-date"))

        for atualizacao in sec.find_all("span", class_="updated-date"):
           atualizacao = atualizacao.text
           values["atualizacao"] = atualizacao.replace('Actualização: ','')

        for prices in sec.find_all("span", class_="fuel-prices"):


            for fuel in prices.find_all('span'):
                atributes = fuel.attrs

                values[atributes['title']] = float(atributes['data-price']) if atributes['data-price'] != "0" else "---"

        resume[posto] = values

    #print(resume)
    with open(f"precos_{concelho}.json", "w", encoding="utf-8") as f:
        json.dump(resume, f, indent=4, ensure_ascii=False)

    texto_final = f"PREÇOS DOS POSTOS EM {concelho.upper()} ({distrito.upper()})\n(Ordenado por preço de gasolina)\n"
    for cat in resume:
            texto_final += f"\n{cat}\n"
            for val in resume[cat]:
                if val == "atualizacao":
                    texto_final += f"Atualizado: {resume[cat][val]}\n"
                else:
                    texto_final +=f"•{val}: {str(resume[cat][val]).replace('.',',')}€\n"

    #print(texto_final)
    return texto_final, resume



if __name__ == '__main__':
    prices_concelho("braga","barcelos")