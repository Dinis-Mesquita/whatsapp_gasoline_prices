import random
import urllib.parse
import datetime
import time
import json
import requests
import os
import random
from scrapper import avr_prices, avr_prices_by_brand, avr_prices_distritos, avr_price_specific_distrito, avr_prices_concelhos, avr_price_specific_concelho,prices_concelho
def produce_msg(distrito, concelho):
    average_prices, _= avr_prices()
    average_prices_by_brand, _= avr_prices_by_brand(5)
    average_prices_distritos, _ = avr_prices_distritos()
    average_price_specific_distrito, _ = avr_price_specific_distrito(distrito)
    average_prices_concelhos, _ = avr_prices_concelhos(distrito)
    average_price_specific_concelho, _ = avr_price_specific_concelho(distrito, concelho)
    precos_concelho, _ = prices_concelho(distrito, concelho)

    text_final=""
    #text_final += f"\n{average_prices}\n\n"
    #text_final += f"\n{average_prices_by_brand}\n"
    print("Finished main page")
    time.sleep(random.randrange(5,10))
    #text_final += f"\n{average_prices_distritos}\n"
    #text_final += f"\n{average_price_specific_distrito}\n"
    print("Finished distritos page")
    time.sleep(random.randrange(5, 10))
    #text_final += f"\n{average_prices_concelhos}\n"
    #text_final += f"\n{average_price_specific_concelho}\n"
    print("Finished concelhos page")
    #time.sleep(random.randrange(5, 10))
    text_final += f"\n{precos_concelho}\n"

    return text_final
def send_msg():

    #https://www.callmebot.com/blog/free-api-whatsapp-messages/

    for distrito in os.listdir("contacts"):
        concelhos = json.load(open(f"contacts/{distrito}"))




        '''
        {
          "braga" :
            {
                "nome": "example",
                "telefone": "+351",
                "apikey": ""
            }
        
        }
        '''


        for concelho in concelhos:
            nome = concelhos[concelho]["nome"]
            api_key = concelhos[concelho]["apikey"]
            telefone = concelhos[concelho]["telefone"]

            i=0
            
            text_final = produce_msg(distrito.strip(".json"),concelho)
            print(text_final)
            print(f"sent at:{datetime.datetime.now()}")
            text_norm = urllib.parse.quote_plus(text_final)

            url = f"https://api.callmebot.com/whatsapp.php?phone={telefone}&text={text_norm}&apikey={api_key}"


            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"Sucesso: Mensagem enviada para {nome} ({telefone})")
                else:
                    print(f"Erro ao enviar")
            except Exception as e:
                print(f"Falha na conexão ao tentar enviar {nome} ({telefone})")


            time.sleep(5)








if __name__ == '__main__':
    send_msg()