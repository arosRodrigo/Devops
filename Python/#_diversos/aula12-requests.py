import requests

try:
    requisicao = requests.get('https://www.nfce.fazenda.sp.gov.br/qrcode?p=35190245543915003288650090001361361021854597|2|1|1|D76EE4C5EE544E3C87E8DED2795C62391B3C7DC3')
    print(requisicao.content)
except Exception as erro:
    print(erro)
    exit()
