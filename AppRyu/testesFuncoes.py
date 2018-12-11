#portas = '1'
#portas = '1,2'
portas = '1,2,3'

#vet = [i.split(',') for i in portas]

for i in portas:
    if i != ',':
        print(i)
