import os
path_home = os.getenv("HOME") #Captura o caminho da pasta HOME
#Switches e seus Hosts
S1 = ['10.0.0.1','10.0.0.2','10.0.0.3']
S2 = []
S3 = ['10.0.0.8','10.0.0.9']
S4 = ['10.0.0.4','10.0.0.5']
S5 = ['10.0.0.6','10.0.0.7']
LISTA_SWITCHES = [S1,S2,S3,S4,S5]
#Mapeamento estatico de IPs_Porta
SWITCH_S1 = {'10.0.0.1':'1','10.0.0.2':'2','10.0.0.3':'3'} #Qualquer outro sai na porta 5
SWITCH_S2 = {'10.0.0.1':'1','10.0.0.2':'1','10.0.0.3':'1','10.0.0.4':'3','10.0.0.5':'3','10.0.0.6':'4','10.0.0.7':'4','10.0.0.8':'2','10.0.0.9':'2'}
SWITCH_S3 = {'10.0.0.8':'1','10.0.0.9':'2'} #Qualquer outro sai na porta 5
SWITCH_S4 = {'10.0.0.4':'1','10.0.0.5':'2'} #Qualquer outro sai na porta 5
SWITCH_S5 = {'10.0.0.6':'1','10.0.0.7':'2'} #Qualquer outro sai na porta 5
#Lista de Grupos que ja possui o fluxo no Switch
GRUPOS_S1 = [{'239.0.0.1':[],'239.0.0.2':[2],'239.0.0.3':[2,5]}]
GRUPOS_S2 = []
GRUPOS_S3 = []
GRUPOS_S4 = []
GRUPOS_S5 = []
#Grafo da Rede
GRAFO = nx.MultiGraph()
GRAFO.add_edge('10.0.0.1','s1',cost=1,index=0)
GRAFO.add_edge('10.0.0.2','s1',cost=1,index=1)
GRAFO.add_edge('10.0.0.3','s1',cost=1,index=2)
GRAFO.add_edge('10.0.0.4','s4',cost=1,index=3)
GRAFO.add_edge('10.0.0.5','s4',cost=1,index=4)
GRAFO.add_edge('10.0.0.6','s5',cost=1,index=5)
GRAFO.add_edge('10.0.0.7','s5',cost=1,index=6)
GRAFO.add_edge('10.0.0.8','s3',cost=1,index=7)
GRAFO.add_edge('10.0.0.9','s3',cost=1,index=8)
GRAFO.add_edge('s1','s2',cost=1,index=9)
GRAFO.add_edge('s3','s2',cost=1,index=10)
GRAFO.add_edge('s4','s2',cost=1,index=11)
GRAFO.add_edge('s5','s2',cost=1,index=12)
#MAC do Controlador
MAC_CONTROLADOR = 'ff:ff:ff:00:00:00'
#IP do controlador
IP_CONTROLADOR = '10.0.0.99'
#Porta de envio Servicos Multicast
PORTA_MULTICAST = 27000
#Porta para dizer a oferta de Servicos
PORTA_OFERTA_SERVICO = 23000
#Lista de grupos Multicast
LISTA_GRUPO_MULTICAST = []
#Lista de Grupos Multicast com participantes
LISTA_PARTICIPANTES_GRUPO_MULTICAST = []
#Fim Variaveis Globais

'''
Adiciona Regra de fluxo entre servidor e o cliente
'''
def addRegraFluxoServerClient(self,ip_server,ip_client,ip_grupo):
    path_server_client = nx.dijkstra_path(GRAFO,ip_server,ip_client,weight='cost') #Grafo do caminho
    print("Caminho entre cliente e servidor!!")
    print(path_server_client)
    switch_caminho = []
    for j in range(1,len(path_server_client)-1):
            switch_caminho.append(path_server_client[j]) # Guarda os Switches ate o cliente
    #Para cada switch verifico se ja possui o fluxo
    if len(switch_caminho) == 1: # Host Cliente esta no mesmo switch do Servidor
        #BuscarVetorDePortas
        #print("Parei Aqui!!")
        #print("Vetor de Portas!!")
        portas = self.retornaVetPortasFluxo(ip_grupo,switch_caminho[0]) #Recebe a portas que deveram ter o fluxo
        os.system('ovs-ofctl add-flow ' + switch_caminho[0] + ' priority=40000,dl_type=0x0800,nw_proto=17,nw_src='+ip_server+',nw_dst='+ip_grupo+',tp_dst='+str(PORTA_MULTICAST)+',actions=output:'+portas)
        print('Regra Aplicada!!! \n')
    else: #Host Cliente esta em outro Switch
        for j in switch_caminho:
            portas = self.retornaVetPortasFluxo(ip_grupo,j) #Recebe a portas que deveram ter o fluxo
            print('ovs-ofctl add-flow ' + j + ' priority=40000,dl_type=0x0800,nw_proto=17,nw_src='+ip_server+',nw_dst='+ip_grupo+',tp_dst='+str(PORTA_MULTICAST)+',actions=output:'+portas)
            '''
            if self.switchPossuiFluxoMulticast(ip_grupo,j):
                print('Swithc: '+ j +' ja possui o Fluxo')
            else:
                print('Swithc: '+ j +' nao possui o Fluxo')
            '''
'''
FIM Adiciona Regra de fluxo entre servidor e o cliente
'''


'''
Retorna vetor de portas para acao da regra de fluxos
'''
def retornaVetPortasFluxo(self,ip_grupo,switch):
    retorno = ''
    if switch == 's1':
        global GRUPOS_S1

    '''
    for i in LISTA_PARTICIPANTES_GRUPO_MULTICAST:
        if i[0] == ip_grupo:
            lista = i #Recebe a lista de participantes do grupo
            if len(lista) == 2: #So possui o servidor, regra DROP
                retorno = 'drop'
            else: #Busca as portas que deveram ter o fluxo
                for j in range(len(lista)): #Para cada elemento da lista, tirando o primeiro e o segundo, busca as portas
                    if j > 1 and j < (len(lista)-2): #A partir do segundo elemento da lista
                        retorno = retorno + ',' + self.buscaPortaHostSiwtch(switch,lista[j]) #Passa o switch e o ip
                    elif j > 1 and j == (len(lista)-1):
                        retorno = retorno + self.buscaPortaHostSiwtch(switch,lista[j]) #Passa o switch e o ip
                    else:
                        pass
    '''
    return retorno


'''
FIM Retorna vetor de portas para acao da regra de fluxos
'''

'''
Busca porta do Host em um determinado Switch
'''
def buscaPortaHostSiwtch(self, switch, ip_host):
    #Buscar no Mapeamento estatico
    porta = ''
    if switch == 's1':
        if ip_host in SWITCH_S1:
            porta = SWITCH_S1[ip_host]
        else:
            porta = '5'
    elif switch == 's2':
        if ip_host in SWITCH_S2:
            porta = SWITCH_S2[ip_host]
        else:
            porta = '5'
    elif switch == 's3':
        if ip_host in SWITCH_S3:
            porta = SWITCH_S3[ip_host]
        else:
            porta = '5'
    elif switch == 's4':
        if ip_host in SWITCH_S4:
            porta = SWITCH_S4[ip_host]
        else:
            porta = '5'
    elif switch == 's5':
        if ip_host in SWITCH_S5:
            porta = SWITCH_S5[ip_host]
        else:
            porta = '5'
    else:
        porta = '0'
    return porta
'''
FIM Busca porta do Host em um determinado Switch
'''



























'''
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
'''
