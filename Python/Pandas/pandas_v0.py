import pandas as pd
import xlrd

df = pd.read_excel('Pasta1.xlsx', sheet_names='Cadastro')
#df.head()
for i in df.index:
    print(df['Projeto'][i],df['Destino'][i])