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
# COLUNAS
colunas = (matriz['NOME LOGICO'].tolist())
for i in catalogo.columns:
    if i.upper() not in colunas: # verifica se a coluna do arquivo consta na matriz
        relAudit.append('. Coluna "' + i + '" não conforme. Verifique a NOMENCLATURA.')
    else: # CONTEUDO
        conteudo = (catalogo[i].tolist())  # aloca em uma lista todo o conteudo da coluna
        for r in conteudo:
            if type(r) == float and math.isnan(r) == True: #  is empty?
                if matriz['Not null'][colunas.index(i.upper())] == 'Sim': # Not null 'Sim'?
                    relAudit.append('. Coluna "' + i + '" não conforme. Verifique o PREENCHIMENTO')
            else: # type correto?
                tipo = matriz['TYPE'][colunas.index(i.upper())]
                if tipo == 'str': tipo = type(tipo)
                elif tipo == 'int': tipo = type(0)
                elif tipo == 'datetime': tipo = type(date.today())

                if type(r) != tipo: # Type
                    relAudit.append('. Coluna "' + i + '" não conforme. Verifique o TIPO do registro ' + str(r))
                else: # size in case type = string
                    if type(r) == str:
                        if len(r) > matriz['SIZE'][colunas.index(i.upper())]:  # verificar o tamanho do arquivo em caso de string
                            relAudit.append('. Coluna "' + i + '" não conforme. Verifique o TAMANHO do registro ' + str(r))
#-- FIM AUDITORIA---------------------------------------------------------------------------------
if relAudit:
    print('Foram encontradas não conformidades no arquivo. Favor avaliar. Verifiar o Log em log/')
    file = open('log/relatorio_'+str(date.today())+'.txt', 'w')
    for i in relAudit:
        file.write(i + '\n')
#--INICIO CARGA-----------------------------------------------------------------------------------
else:
    print('Segue para carga')

