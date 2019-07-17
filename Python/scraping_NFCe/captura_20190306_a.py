from functions import URL
from pymongo import MongoClient

url = 'https://www.nfce.fazenda.sp.gov.br/NFCeConsultaPublica/Paginas/ConsultaQRCode.aspx?p=35190261075594006630650650000680581385903288|2|1|1|BAAA709387184BC0E2D19BA3816BE4537991F2A4'

b = URL()
cupom = {}

if b.checkURL(url) == True:
    soup = b.scrapingURL(url)
    if soup != False:
        cupom['estabelecimento'] = b.scrapingEstabelecimento(soup)
        cupom['itens'] = b.scrapingItens(soup)
        cupom['infopagto'] = b.scrapingInfoPagto(soup)
else:
    print('url inválida')

client = MongoClient('mongodb://localhost:27017/')
db = client.Notas #base
collection = db.cupomFiscal #coleção
x = collection.insert_one(cupom)
print(x)






