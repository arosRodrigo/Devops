import requests
from bs4 import BeautifulSoup

class URL:

    def checkURL(self,url):
        if url[0:5] == 'https':
            return True
        else:
            return False

    def scrapingURL(self,url):

        # Capturar a página#
        try:
            page = requests.get(url)
            return BeautifulSoup(page.text, 'html.parser')

        except Exception as erro:
            return False

    def scrapingEstabelecimento(self,soup):
        list = []
        estabelecimento = soup.find(class_='txtCenter')
        estabelecimento = estabelecimento.findAll('div')
        for i in estabelecimento:
            # conteudo da tag: retirando quebra de linha
            i = i.get_text().replace('\r', '')
            i = i.replace('\n', '')
            i = i.replace('\t', '')
            list.append(i)
        return list

    def scrapingItens(self,soup):
        list = []
        itens = soup.find(id='tabResult')
        itens = itens.findAll('tr')
        for i in itens:
            i = i.findAll('span')
            for l in i:
                l = l.get_text().replace('\n', '')
                l = l.replace('\t', '')
                l = l.replace('\r', '')
                list.append(l)
        return list

    def scrapingInfoPagto(self,soup):
        list = []
        info_pgto = soup.find(id='totalNota')
        info_pgto = info_pgto.find_all(['label', 'span'])
        for i in info_pgto:
            i = i.get_text().replace('\r', '')
            i = i.replace('\n', '')
            i = i.replace('\t', '')
            list.append(i)
        return list



