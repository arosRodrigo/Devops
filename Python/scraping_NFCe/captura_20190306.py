import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient



#Capturar a página#
try:
    page = requests.get('https://www.nfce.fazenda.sp.gov.br/qrcode?p=35190245543915003288650090001361361021854597|2|1|1|D76EE4C5EE544E3C87E8DED2795C62391B3C7DC3')
    #page = requests.get('https://www.nfce.fazenda.sp.gov.br/NFCeConsultaPublica/Paginas/ConsultaQRCode.aspx?p=35190261075594006630650650000680581385903288|2|1|1|BAAA709387184BC0E2D19BA3816BE4537991F2A4')
    #page = requests.get('https://www.nfce.fazenda.sp.gov.br/qrcode?p=35190245543915003288650110001517731021847065|2|1|1|8C322F3031670AC10D25F113FBDF770422B25169')
    #page = requests.get('https://www.nfce.fazenda.sp.gov.br/NFCeConsultaPublica/Paginas/ConsultaQRCode.aspx?p=35190261075594006630650650000680581385903288|2|1|1|BAAA709387184BC0E2D19BA3816BE4537991F2A4')
    soup = BeautifulSoup(page.text, 'html.parser')
    # dados da empresa
    estabelecimento = soup.find(class_='txtCenter')
    estabelecimento = estabelecimento.findAll('div')
    # itens do cupom********************************#
    itens = soup.find(id='tabResult')
    itens = itens.findAll('tr')
    # informações de pagto
    info_pgto = soup.find(id='totalNota')
    info_pgto = info_pgto.find_all(['label','span'])
    # informações gerais
    #info_gerais = soup.find(id='infos')

except Exception as erro:
    print(erro)
    #exit()

# Dicionario para alocar os dados da pagina capturada...
cupom = {}
list_est = []
list_itens = []
list_info_pgto = []
list_info_gerais = []


#alocar dados do estabelecimento
for i in estabelecimento:
    #conteudo da tag: retirando quebra de linha
    i = i.get_text().replace('\r', '')
    i = i.replace('\n', '')
    i = i.replace('\t', '')
    list_est.append(i)
    cupom['estabelecimento'] = list_est

#alocar itens do cupom
for i in itens:
    i = i.findAll('span')
    for l in i:
        l = l.get_text().replace('\n', '')
        l = l.replace('\t', '')
        l = l.replace('\r', '')
        list_itens.append(l)
        cupom['itens'] = list_itens

#alocar informações de pgto
for i in info_pgto:
    i = i.get_text().replace('\r', '')
    i = i.replace('\n', '')
    i = i.replace('\t', '')
    list_info_pgto.append(i)
    cupom['info_pagto'] = list_info_pgto
'''
#alocar informações gerais
for i in info_gerais:
    print(i)
'''


