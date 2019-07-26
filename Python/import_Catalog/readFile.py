import pandas as pd
import xlrd
from datetime import date
import math

#--DECLARAÇÕES-----------------------------------------------
# Metadados
# Matriz
matriz = pd.read_excel('3_matriz.xlsx', sheet_names='Tabelas')
# Catalogo
catalogo = pd.read_excel('2_Catalogo de Dados_Sulamerica.xlsx', sheet_names='Catalogo') #, skiprows=1(pular uma linha)
# Relatório de auditoria------------------------
relAudit = []

#--AUDITORIA-------------------------------------------------
# nomenclatura
colunas = (matriz['NOME LOGICO'].tolist())
for i in catalogo.columns:
    if i.upper() not in colunas: # verifica se a coluna do arquivo consta na matriz
        relAudit.append('. Coluna "' + i + '" não conforme. Verifique a NOMENCLATURA.')
    else: # verifica o conteúdo da coluna
        tipo = matriz['TYPE'][colunas.index(i.upper())]
        # converte o tipo para um elemento comparável---------------------
        if tipo == 'str': tipo = type(tipo)
        elif tipo == 'int': tipo = type(0)
        elif tipo == 'datetime': tipo = type(date.today())

        conteudo = (catalogo[i].tolist())# aloca em uma lista todo o conteudo da coluna
        for r in conteudo:# verifica cada registro
            if not r:
                print(r)

            # obrigatoriedade---------------------------
            obrg = matriz['Not null'][colunas.index(i.upper())]
            if obrg == 'Sim': # verifica obrigatoriedade
                if type(r) == str:
                    if not r.strip():
                        relAudit.append('. Coluna "' + i + '" não conforme. Verifique o PREENCHIMENTO')
                elif type(r) == int:
                    if not r:
                        relAudit.append('. Coluna "' + i + '" não conforme. Verifique o PREENCHIMENTO')
                elif type(r) != float:
                    if math.isnan(r)==True:
                        relAudit.append('. Coluna "' + i + '" não conforme. Verifique o PREENCHIMENTO')

            if type(r) != tipo:# verifica o tipo do valor
                    relAudit.append('. Coluna "' + i + '" não conforme. Verifique o TIPO do registro ' + str(r))
            elif type(r) == str:
                # tamanho definido para o campo---------------------------
                size = matriz['SIZE'][colunas.index(i.upper())]
                if len(r) > size:  # verificar o tamanho do arquivo em caso de string
                    relAudit.append('Coluna "' + i + '" não conforme. Verifique o TAMANHO do registro ' + str(r))
#-- FIM AUDITORIA---------------------------------------------------------------------------------
if relAudit:
    print('Foram encontradas não conformidades no arquivo. Favor avaliar.')
    for i in relAudit:
        print(i)
#--INICIO CARGA-----------------------------------------------------------------------------------
else:
    print('Segue para carga')

