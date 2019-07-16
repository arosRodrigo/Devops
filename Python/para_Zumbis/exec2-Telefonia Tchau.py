''' Problema
    Abaixo de 200 minutos, a empresa cobra 0,20.
    Entre 200 e 400 minutos, o preço é 0,18
    acima de 400, o preço é 0,15
    Calcule a conta de telefone

    Obs.: se mais que 800, cobrar 0.08
'''

''' #alternativa de solução 1
minutos = int(input('Quantos minutos foram utilizados?'))

if minutos < 200:
    print('Você irá pagar: R$',minutos*0.20)
if minutos >=200 and minutos < 400:
    print('Você irá pagar: R$', minutos * 0.18)
else:
    print('Você irá pagar: R$', minutos * 0.15)
'''
''' alternativa 2
minutos = int(input('Munutos utilizados: '))

if minutos < 200:
    preco = 0.20
else:
    if minutos < 400:
        preco = 0.18
    else:
        if minutos < 800:
            preco = 0.15
        else:
            preco = 0.08

print('O valor a ser pago é: R$',(minutos*preco))
'''

minutos = int(input('Munutos utilizados: '))

if minutos < 200:
    preco = 0.20
elif minutos < 400:
    preco = 0.18
elif minutos < 800:
    preco = 0.15
else:
    preco = 0.08

print('O valor a ser pago é: R$',(minutos*preco))