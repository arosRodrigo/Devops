import requests

#url ='https://code.launchpad.net/~inkscape.dev/+archive/ubuntu/stable'
url = 'https://satsp.fazenda.sp.gov.br/COMSAT/Public/ConsultaPublica/ConsultaPublicaCfe.aspx'
page = requests.get(url)
print(page)