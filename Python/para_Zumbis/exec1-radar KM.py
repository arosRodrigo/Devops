'''
    perguntar a velocidade de um carro. Se o mesmo ultrapassou 110 Km,
    exibir mensagem informando que o usuário foi multado. Aplicar multa de 5 reais por KM acima dos 110
'''

velocidade = int(input('Qual a velocidade do carro?'))

if velocidade > 110:
    velocidadeAcima = (velocidade-110)
    vlrMulta = velocidadeAcima*5
    print('Você excedeu a velodidade em:',velocidadeAcima,'KM. O valor da sua multa será de : R$',vlrMulta)
else:
    print('se livrou.')