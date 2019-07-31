import pandas as pd
import xlrd
from datetime import date
import math
import pymysql
from tqdm import tqdm

#--DECLARAÇÕES-----------------------------------------------
# Metadados
# Matriz
matriz = pd.read_excel('3_matriz.xlsx', sheet_names='Tabelas')
# Catalogo
catalogo = pd.read_excel('2_Catalogo de Dados_Sulamerica.xlsx', sheet_names='Catalogo', skiprows=1) #, skiprows=1(pular uma linha)
# Relatório de auditoria------------------------
relAudit = []

#--AUDITORIA-------------------------------------------------
# COLUNAS
colunas = (matriz['NOME LOGICO'].tolist())
for y in tqdm(range(len(catalogo.columns))):
    for i in catalogo.columns:
        if i.upper() not in colunas: # verifica se a coluna do arquivo consta na matriz
            relAudit.append('. Coluna "' + i + '" não conforme. Verifique a NOMENCLATURA.')
        else: # CONTEUDO
            conteudo = (catalogo[i].tolist())  # aloca em uma lista todo o conteudo da coluna
            count = 0
            for r in conteudo:
                if type(r) == float and math.isnan(r) == True: #  is empty?
                    if matriz['Not null'][colunas.index(i.upper())] == 'Sim': # Not null 'Sim'?
                        relAudit.append('. Coluna "' + i + '" não conforme. Verifique o PREENCHIMENTO')
                    else:
                        catalogo[i][count] = ''
                        #catalogo.at[count, i] = ''
                        #catalogo.set_value(count, i, '',takeable=False)
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
                count = count+1
#-- FIM AUDITORIA---------------------------------------------------------------------------------
if relAudit:
    print('Foram encontradas não conformidades no arquivo. Favor avaliar. Verifiar o Log em log/')
    file = open('log/relatorio_'+str(date.today())+'.txt', 'w')
    for i in relAudit:
        file.write(i + '\n')

#--INICIO CARGA-----------------------------------------------------------------------------------
else:
    #--Abertura de conexão ao banco de dados---------------------------
    conexao = pymysql.connect(db='catalogodados', user='root', passwd='@123')
    cursor = conexao.cursor()

    i = 0
    projeto = []
    tabelaDestino = []
    infoLegal = []
    atrDest = []
    tabelaOrigem = []
    atrOrg = []
    for y in tqdm(range(int(catalogo.shape[0]))):
        while i < catalogo.shape[0]:
            #--Insert de Projeto--------------------------------------------------------------------------------------------------------------------------------------------------
            if cursor.execute("SELECT idProjeto FROM catalogodados.tb_projeto where nome='" + catalogo['Nome do Projeto'][i] + "'"):  # verificar se já existe o registro no banco
                idProjeto = cursor.fetchall()
                for x in idProjeto:
                    projeto.append({"idProjeto": x[0], "Indice": i})
            else:
                cursor.execute("INSERT INTO catalogodados.tb_projeto(nome,descricao)VALUES('" + str(catalogo['Nome do Projeto'][i]) + "','" + str(catalogo['Descrição do Projeto'][i]) + "')")
                lastID = cursor.lastrowid
                conexao.commit()
                projeto.append({"idProjeto": lastID, "Indice": i})
            #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
            #--Tabela Destino-----------------------------------------------------------------------------------------------------------------------------------------------------
            if cursor.execute("SELECT idTbDestino FROM catalogodados.tb_destino where nDatabase='" + catalogo['database da Tabela Destino'][i] + "' and nomeFis='" + catalogo['Nome Físico Tabela Destino'][i] + "' and nomelog='" + catalogo['Nome Lógico Tabela Destino'][i] + "'"):
                idTbDestino = cursor.fetchall()
                for x in idTbDestino:
                    tabelaDestino.append({"idTbDestino": x[0], "Indice":i})
            else:
                # verifica se existe projeto atrelado a tabela destino
                for s in projeto:
                    if str(i) in str(s['Indice']):
                        idProjeto = s['idProjeto']
                cursor.execute("INSERT INTO catalogodados.tb_destino(nDatabase,nomeFis,ambiente,platTec,nomelog,zona,descricao,nOwner,dataSteward,ramoBU,conceito,perIng,tpRepl,cicloVida,ptjGcp,roadMap,tb_projeto_idProjeto) VALUES ("
                               "'" + str(catalogo['database da Tabela Destino'][i]) + "',"
                               "'" + str(catalogo['Nome Físico Tabela Destino'][i]) + "',"
                               "'" + str(catalogo['Ambiente da Tabela Destino'][i])+ "',"
                               "'" + str(catalogo['Plataforma de Tecnologia da Tabela Destino'][i]) + "',"
                               "'" + str(catalogo['Nome Lógico Tabela Destino'][i]) + "',"
                               "'" + str(catalogo['Zona da Tabela Destino'][i]) + "',"
                               "'" + str(catalogo['Descrição da Tabela Destino'][i]) + "',"
                               "'" + str(catalogo['Owner'][i]) + "',"
                               "'" + str(catalogo['Data Steward'][i]) + "',"
                               "'" + str(catalogo['Ramo - BU'][i]) + "',"
                               "'" + str(catalogo['Conceito da Tabela Destino'][i]) + "',"
                               "'" + str(catalogo['Periodicidade de Ingestão'][i]) + "',"
                               "'" + str(catalogo['Tipo de Replicação'][i]) + "',"
                               "'" + str(catalogo['Ciclo de Vida'][i]) + "',"
                               "'" + str(catalogo['Projeto no GCP'][i]) + "',"
                               "'" + str(catalogo['RoadMap'][i]) + "'," + str(idProjeto) + ")")
                lastID = cursor.lastrowid
                conexao.commit()
                tabelaDestino.append({"idTbDestino": lastID, "Indice": i})
            # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
            #--Tabela informação legal---------------------------------------------------------------------------------------------------------------------------------------------
            if cursor.execute("SELECT idTbInfolegal FROM catalogodados.tb_info_legal where baseLegal='" + catalogo['Base Legal'][i] + "' and orgRegulador='" + catalogo['Orgão Regulador'][i] + "'"):
                idTbInfolegal = cursor.fetchall()
                for x in idTbInfolegal:
                    infoLegal.append({"idTbInfolegal": x[0], "Indice":i})
            else:
                cursor.execute("INSERT INTO catalogodados.tb_info_legal(baseLegal,orgRegulador,dadosRegulatorio,confidencialidade,finalidade)VALUES('" + str(catalogo['Base Legal'][i]) + "',"
                                                                                                                                                   "'" + str(catalogo['Orgão Regulador'][i]) + "',"
                                                                                                                                                   "'" + str(catalogo['Dados Regulário'][i]) + "',"
                                                                                                                                                   "'" + str(catalogo['Confidencialidade'][i]) + "',"
                                                                                                                                                   "'" + str(catalogo['Finalidade'][i]) + "')")
                lastID = cursor.lastrowid
                conexao.commit()
                infoLegal.append({"idTbInfolegal": lastID, "Indice": i})
            #  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
            #--Informação Legal / Tabela Destino------------------------------------------------------------------------------------------------------------------------------------
            for s in infoLegal:
                if str(i) in str(s['Indice']):
                    for r in tabelaDestino:
                        if str(i) in str(r['Indice']):
                            cursor.execute("INSERT INTO catalogodados.tb_info_legal_destino(idTbInfolegal,idTbDestino)VALUES('" + str(s['idTbInfolegal']) + "','" + str(r['idTbDestino']) + "')")
            #  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
            #--Atributos Destino-----------------------------------------------------------------------------------------------------------------------------------------------------
            for s in tabelaDestino:
                if str(i) in str(s['Indice']):
                    idTbDestino = s['idTbDestino']
            if cursor.execute("SELECT idAtrDest FROM catalogodados.tb_atributos_destino where nomeLog='" + catalogo['Nome Lógico Atributo Destino'][i] + "' and tb_destino_idTbDestino='" + str(idTbDestino) + "'"):
                idAtrDest = cursor.fetchall()
                for x in idAtrDest:
                    atrDest.append({"idAtrDest": x[0], "Indice":i})
            else:
                cursor.execute("INSERT INTO catalogodados.tb_atributos_destino(nomeFis,nomeLog,descricao,regrasNeg,`type`,primKey,nivProt,tb_destino_idTbDestino)VALUES('" + str(catalogo['Nome Físico Atributo Destino'][i]) + "',"
                                                                                                                                                                       "'" + str(catalogo['Nome Lógico Atributo Destino'][i]) + "',"
                                                                                                                                                                       "'" + str(catalogo['Descrição Atributo Destino'][i]) + "',"
                                                                                                                                                                       "'" + str(catalogo['Regras de Negócio Atributo Destino'][i]) + "',"
                                                                                                                                                                       "'" + str(catalogo['Tipo do Atributo Destino'][i]) + "',"
                                                                                                                                                                       "'" + str(catalogo['Primary Key Atributo Destino'][i]) + "',"
                                                                                                                                                                       "'" + str(catalogo['Nivel de Proteção Atributo Destino'][i]) + "',"
                                                                                                                                                                       "'" + str(idTbDestino) + "')")
                lastID = cursor.lastrowid
                conexao.commit()
                atrDest.append({"idAtrDest": lastID, "Indice": i})
            #  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            #--Tabela Origem------------------------------------------------------------------------------------------------------------------------------------------------------------
            if cursor.execute("SELECT idOrigem FROM catalogodados.tb_origem where nomeFis='" + catalogo['Nome físico da Tabela Origem'][i] + "' and nDatabase='" + catalogo['database da Tabela Origem'][i] + "' and tb_destino_idTbDestino='" + str(idTbDestino) + "'"):
                idOrigem = cursor.fetchall()
                for x in idOrigem:
                    tabelaOrigem.append({"idOrigem": x[0], "Indice":i})
            else:
                cursor.execute("INSERT INTO catalogodados.tb_origem(ambiente,nomeFis,zona,nDatabase,sistema,platTec,proLeg,tb_destino_idTbDestino)VALUES('" + str(catalogo['Ambiente da Tabela Origem'][i]) + "',"
                                                                                                                                                        "'" + str(catalogo['Nome físico da Tabela Origem'][i]) + "',"
                                                                                                                                                        "'" + str(catalogo['Zona Tabela Origem'][i]) + "',"
                                                                                                                                                        "'" + str(catalogo['database da Tabela Origem'][i]) + "',"
                                                                                                                                                        "'" + str(catalogo['Sistema Tabela Origem'][i]) + "',"
                                                                                                                                                        "'" + str(catalogo['Plataforma de Tecnologia da Tabela Origem'][i]) + "',"
                                                                                                                                                        "'" + str(catalogo['Projeto legado'][i]) + "',"
                                                                                                                                                        "'" + str(idTbDestino) + "')")
                lastID = cursor.lastrowid
                conexao.commit()
                tabelaOrigem.append({"idOrigem": lastID, "Indice":i})
            #  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            #--Atributos Origem---------------------------------------------------------------------------------------------------------------------------------------------------------
            for s in tabelaOrigem:
                if str(i) in str(s['Indice']):
                    idOrigem = s['idOrigem']
            if cursor.execute("SELECT idAtrOrg FROM catalogodados.tb_atributos_origem where nomeLog='" + catalogo['Nome Lógico Atributo Origem'][i] + "' and tb_origem_idOrigem='" + str(idOrigem) + "'"):
                idAtrOrg = cursor.fetchall()
                for x in idAtrOrg:
                    atrOrg.append({"idAtrOrg": x[0], "Indice": i})
            else:
                cursor.execute("INSERT INTO catalogodados.tb_atributos_origem(nomeFis,nomeLog,descricao,regrasNeg,`type`,primKey,nivProt,tb_origem_idOrigem)VALUES('" + str(catalogo['Nome Físico Atributo Origem'][i]) + "',"
                                                                                                                                                                    "'" + str(catalogo['Nome Lógico Atributo Origem'][i]) + "',"
                                                                                                                                                                    "'" + str(catalogo['Descrição Atributo Origem'][i]) + "',"
                                                                                                                                                                    "'" + str(catalogo['Regras de Negócio Atributo Origem'][i]) + "',"
                                                                                                                                                                    "'" + str(catalogo['Tipo Atributo Origem'][i]) + "',"
                                                                                                                                                                    "'" + str(catalogo['Primary Key Atributo Origem'][i]) + "',"
                                                                                                                                                                    "'" + str(catalogo['Nivel de Proteção Atributo Origem'][i]) + "',"
                                                                                                                                                                    "'" + str(idOrigem) + "')")
                lastID = cursor.lastrowid
                conexao.commit()
                atrOrg.append({"idAtrDest": lastID, "Indice": i})
            # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            i = i+1
    conexao.close()
    #--FIM CARGA-----------------------------------------------------------------------------------
    print("Processo finalizado.")
    file = open('log/relatorio_'+str(date.today())+'.txt', 'w')
    file.write("Processo finalizado." + '\n')
