import pandas as pd
import xlrd
from datetime import date
import math

#--DECLARAÇÕES-----------------------------------------------
# Metadados
# Matriz
matriz = pd.read_excel('Matriz.xlsx', sheet_names='Tabelas')
# Catalogo
catalago = pd.read_excel('Catalogo.xlsx', sheet_names='registros')
# Relatório de auditoria------------------------
relAudit = ['Arquivo conforme']

#--AUDITORIA-------------------------------------------------
# nomenclatura
for i in catalago.columns:
    colunas = (matriz['NOME LOGICO'].tolist())
    if i not in colunas: # verifica se a coluna do arquivo consta na matriz
        relAudit.append('Coluna ' + i + ' não conforme. Verifique a nomenclatura.')
    else: # verifica o conteúdo da coluna
        tipo = matriz['TYPE'][colunas.index(i)]
        # converte o tipo para um elemento comparável---------------------
        if tipo == 'str': tipo = type(tipo)
        elif tipo == 'int': tipo = type(0)
        elif tipo == 'datetime': tipo = type(date.today())
        # obrigatoriedade---------------------------
        obrg = matriz['Not null'][colunas.index(i)]

        # tamanho definido para o campo---------------------------
        size = matriz['SIZE'][colunas.index(i)]

        conteudo = (catalago[i].tolist())# aloca em uma lista todo o conteudo da coluna
        for r in conteudo:# verifica cada registro
            if obrg == 'Sim': # verifica obrigatoriedade
                if type(r) == str:
                    if not r.strip():
                        relAudit.append('Coluna ' + i + ' não conforme. Verifique o preenhchimento')
                elif type(r) == int:
                    if not r:
                        relAudit.append('Coluna ' + i + ' não conforme. Verifique o preenhchimento')
                elif type(r) != float:
                    if math.isnan(r)==True:
                        relAudit.append('Coluna ' + i + ' não conforme. Verifique o preenhchimento')

            if type(r) != tipo:# verifica o tipo do valor
                    relAudit.append('Coluna ' + i + ' não conforme. Verifique o tipo do registro ' + str(r))
            elif type(r) == str:
                if len(r) > size:  # verificar o tamanho do arquivo em caso de string
                    relAudit.append('Coluna ' + i + ' não conforme. Verifique o tamanho do registro ' + str(r))
#-- FIM AUDITORIA---------------------------------------------------------------------------------
for i in relAudit:
    print(i)

