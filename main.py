import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

class fii:
    def __init__(self, ticker):
        self.ticker = ticker
    def pegar_dividendos_fii(self):
        agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        url = f"https://www.fundamentus.com.br/fii_proventos.php?papel={self.ticker}&tipo=2"
        webpage = requests.get(url, headers=agent)
        soup = BeautifulSoup(webpage.content, "html.parser")
        resultados = soup.find(id = "resultado")
        tabela_body = resultados.find("tbody")
        linhas = tabela_body.find_all("tr")
        data = []
        for linha in linhas:
            colunas = linha.find_all("td")
            colunas = [ele.text.strip() for ele in colunas]
            data.append([ele for ele in colunas if ele])
        data_output = pd.DataFrame(data, columns=["Data_com", "rendimento", "data_rendimento", "valor"])
        data_output['papel'] = self.ticker
        # aqui pegaremos sempre o ultimo dividendo disponivel
        data_output = data_output.iloc[0]

        return data_output

def get_dividend(papel):
    return fii(papel).pegar_dividendos_fii()
 
# usando map para rodar a funcao para os tickers
resultados_map = pd.DataFrame(list(map(get_dividend, ["VISC11", "VRTA11", "RBRF11"])))

# exportando FIIs
#resultados_map.to_excel("dividendos_fiis.xlsx")
print(resultados_map)