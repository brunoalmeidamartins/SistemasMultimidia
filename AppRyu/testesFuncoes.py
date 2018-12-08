S1 = ['10.0.0.1','10.0.0.2','10.0.0.3']
S2 = []
S3 = ['10.0.0.8','10.0.0.9']
S4 = ['10.0.0.4','10.0.0.5']
S5 = ['10.0.0.6','10.0.0.7']
LISTA_SWITCHES = [S1,S2,S3,S4,S5]

def retornaSwitchIP(ip):
    index = -1
    switch = ''
    for i in range(len(LISTA_SWITCHES)):
        if ip in LISTA_SWITCHES[i]:
            index = i+1
    if index == 1:
        switch = 's1'
    elif index == 2:
        switch = 's2'
    elif index == 3:
        switch = 's3'
    elif index == 4:
        switch = 's4'
    elif index == 5:
        switch = 's5'
    else:
        switch = 'Erro'
    return switch

print(retornaSwitchIP('10.0.0.8'))
