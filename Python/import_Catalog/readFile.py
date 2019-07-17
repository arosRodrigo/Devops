import pandas as pd
import xlrd

#ler o arquivo
df = pd.read_excel('Cadastro.xlsx', sheet_names='cad')
lista = df['NomeProjeto'].tolist()
maior = max(lista, key=lambda x: len(x.strip()))
print(len(maior.strip()))


'''

#--AUDITORIA------------------------------

#Verificar o cabeçalho
cabecalho = ['NomeProjeto','DescricaoProjeto','NomeFisico','Owner']
cabecalhoFile = []
relAudit = []
for r in df.columns:
    cabecalhoFile.append(r.strip())

#Verifica o tipo

#Verificar tamanho de colunas do tipo inteiro
lista = df['NomeProjeto'].tolist()
maior = max(lista, key=lambda x: len(x.strip()))
print(len(maior.strip()))


#verificar campos obrigatórios

#Preenche relatório de auditoria
if cabecalho != cabecalhoFile:
    relAudit = [{'Cabeçhalho':'não conforme'}]
else:
    relAudit = [{'Cabeçhalho':'conforme'}]
'''


'''
#armazenar em um dicionário
registros = []
for i in df.index:
    registros.append(
                      {
                       'NomeProjeto':df['NomeProjeto'][i],
                       'DescricaoProjeto': df['DescricaoProjeto'][i],
                       'NomeFisico': df['NomeFisico'][i],
                       'Owner': df['Owner'][i]
                       }

                     )
print(registros)
'''





#auditar o arquivo

