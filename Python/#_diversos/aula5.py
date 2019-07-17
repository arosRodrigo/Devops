frutas = ['abacaxi','uva','abacate']
lista_de_numeros = range(3)
palavra = 'Anderson Rodrigo'

#for fruta in frutas:
#    print(fruta)

#for n in range(len(frutas)):
#    print(frutas[n])

#for letra in palavra:
#    print(letra)

#i = 1

#while i < 10:
#    i=i+1
#    print(i)

'''
    leia quantidade de pessoa de uma festa, apos isso o programa vai perguntar os nomes de cada pessoa e colocar numa lista de 
    convidados e imprimir  
'''

qtdPss = int(input('Qtas pessoa'))
convidados=[]

i=0
while i < qtdPss:
    nome = input('Convidado')
    convidados.append(nome)
    i = i+1

print('Estes são seus convidados:')

for convidado in convidados:
    print(convidado)
