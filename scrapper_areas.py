import requests
from bs4 import BeautifulSoup
import json
import time

headers = {"User-Agent": "Mozilla/5.0"}

def obter_area_medica(termo_en):
    termo_query = termo_en.replace(" ", "+")
    search_url = f"https://meshb.nlm.nih.gov/search?searchMethod=FullWord&searchInField=termDescriptor&sort=&size=20&searchType=allWords&from=0&q={termo_query}"

    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Verificar se há resultados
    no_results = soup.find("div", string="No results for")
    if no_results:
        return "Outras áreas"

    # Aceder ao primeiro link do resultado
    first_result = soup.select_one("div#searchResults div[id^='result_'] a")
    if not first_result:
        return "Outras áreas"

    link_termo = "https://meshb.nlm.nih.gov" + first_result.get("href")
    res_termo = requests.get(link_termo, headers=headers)
    soup_termo = BeautifulSoup(res_termo.text, "html.parser")

    # Verificar existência de Tree Number
    tree_number_link = soup_termo.select_one("a[id^='treeNumber_']")
    if not tree_number_link:
        return "Outras áreas"

    # Extrair a primeira área da árvore hierárquica
    first_tree = soup_termo.select_one("div#treesTabContent ul > li")
    if first_tree:
        first_span = first_tree.find("span")
        if first_span:
            area = first_span.get_text(strip=True)
        else:
            area = first_tree.get_text(strip=True).split("[")[0].strip()
        return area
    else:
        return "Outras áreas"

# Carregar JSON
with open("json_completo_atualizado.json", encoding="utf-8") as f:
    conceitos = json.load(f)

# Atualizar conceitos
for conceito in conceitos:
    if "área médica" not in conceito and "en" in conceito:
        termo_en = conceito["en"][0]
        area = obter_area_medica(termo_en)
        conceito["área médica"] = area
        time.sleep(1)

# Guardar novo JSON
with open("gloss_atualizado.json", "w", encoding="utf-8") as f:
    json.dump(conceitos, f, ensure_ascii=False, indent=2)

print("📁 Ficheiro atualizado com sucesso!")
