'''
    imprimir os numeros pares de 0 a té o número digitado pelo usuário

'''

''' alternativa 1
numero = int(input("Digite um numero"))
i = 2

while i<= numero:
    print(i)
    i = i + 2
'''

numero = int(input("Digite um numero"))
i = 0

while i<= numero:
    if i % 2 == 0:
        print(i)
    i = i + 1
