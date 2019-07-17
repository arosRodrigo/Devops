'''
def soma(nur1,nur2):
    resposta = nur1*nur2
    return resposta


resp = soma(1,2)
print(resp)

recebe um a lista e retornar o valor de maior numero desta coleção
'''

def maior_valor(numeros):
    maior = max(numeros)
    return maior

def menor_valor(numeros):
    menor = min(numeros)
    return menor

numeros = (5,6,12,98,125)
print(maior_valor(numeros))
print(menor_valor(numeros))


