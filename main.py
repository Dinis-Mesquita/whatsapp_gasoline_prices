import urllib.parse
import time
import json
import requests
import os
from scrapper import scrapper_main_page
def produce_msg(concelho):


    text_final=""
    text_final += f"\n{scrapper_main_page()}\n"

    return text_final
def send_msg():

    #https://www.callmebot.com/blog/free-api-whatsapp-messages/

    for file in os.listdir("contacts"):
        distritos = json.load(open(f"contacts/{file}"))


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


        for concelho in distritos:
            nome = distritos[concelho]["nome"]
            api_key = distritos[concelho]["apikey"]
            telefone = distritos[concelho]["telefone"]

            text_final = produce_msg(concelho)
            print(text_final)
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