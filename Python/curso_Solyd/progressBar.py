from tqdm import tqdm

lista1 = []
lista2 = []
for i in range(4000):
  lista1.append('teste'+str(i))

for i in tqdm(range(len(lista1))):
  for x in lista1:
    lista2.append(x)



print(lista2)



