import requests
from bs4 import BeautifulSoup

try:
    page = requests.get('https://www.nfce.fazenda.sp.gov.br/qrcode?p=35190245543915003288650090001361361021854597|2|1|1|D76EE4C5EE544E3C87E8DED2795C62391B3C7DC3')
    soup = BeautifulSoup(page.text, 'html.parser')
    #Dados do Estabelecimento
    empresa = soup.find(class_='txtCenter')
    empresa_dados = empresa.findAll('div')
    #Dados dos Itens
    itens = soup.find(id ='tabResult')
    itens_dados = itens.findAll('span')

except Exception as erro:
    print(erro)
    exit()

#Dados do Estabelecimento
emp_Dados = []
for i in empresa_dados:
    i = i.get_text().replace('\n','')
    i = i.replace('\t', '')
    i = i.replace('\r', '')
    emp_Dados.append(i)

#Dados dos Itens
it_Dados = []
for i in itens_dados:
    i = i.get_text().replace('\n','')
    i = i.replace('\t', '')
    i = i.replace('\r', '')
    it_Dados.append(i)

print(emp_Dados)
print(it_Dados)



#print(soup.prettify())
    #print(soup.find_all('title')[0].get_text())
    #print(soup.find_all(id='u20')[0].get_text())
    #print(soup.find_all(class_='txtTopo'))
    #print(soup.body.contents)