import socket as skt 

def ganarPuntos(jugador, bot):
    if (jugador == 'Piedra') and (bot=='Tijera'):
        return True
    if (jugador == 'Papel') and (bot=='Piedra'):
        return True
    if (jugador == 'Tijera') and (bot=='Papel'):
        return True
    return False

def juegoCachipun(clienteSocket, ip, puerto):
    #Comunicarse con puerto de partida
    serverAddr = ip
    serverPortUDP = int(puerto)

    clientePartida = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
    clientePartida.connect((serverAddr, serverPortUDP))

    #Puntos
    puntos_jugador = 0
    puntos_servidor = 0

    run = True
    while(run):
        #Se recibe la jugada inicial
        jug_inicial = clienteSocket.recv(2048).decode()
        #Se solicita jugada del servidor Cachipun
        clientePartida.send(jug_inicial.encode())
        print("[*] Esperando jugada...")
        bot_jug = clientePartida.recvfrom(2048)[0].decode()
        print("[*] El contrincante juega ", bot_jug)

        if(jug_inicial == bot_jug): #Empate
            resultado = "EMPATE"
        elif ganarPuntos(jug_inicial, bot_jug):
            resultado = "GANAR"
            puntos_jugador+=1
        else:
            resultado = "PERDER"
            puntos_servidor+=1

        if (puntos_jugador==3):
            msg_cliente = bot_jug+'|'+resultado+'|'+str(puntos_jugador)+'|'+str(puntos_servidor)+'|WIN'
            run = False
        elif (puntos_servidor == 3):
            msg_cliente = bot_jug+'|'+resultado+'|'+str(puntos_jugador)+'|'+str(puntos_servidor)+'|LOSE'
            run = False
        else:
            #Enviar jugada y resultados al cliente
            msg_cliente = bot_jug+'|'+resultado+'|'+str(puntos_jugador)+'|'+str(puntos_servidor)+'|SEGUIR'

        clienteSocket.send(msg_cliente.encode())

    #Avisar a Cachipun de que la partida termino
    msg = "FIN"
    clientePartida.send(msg.encode())
    clientePartida.close()
    print("[*] Se cierra conexión con servidor Cachipún en ", puerto)


#Servidor
serverPort = 50003

serverSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #AF_INET: IPV4, SOCK_STREAM: TCP

serverSocket.bind(('', serverPort))

serverSocket.listen(1)

print("[*] Servidor TCP escuchado en: ", serverPort)
clientSocket, clientAddr = serverSocket.accept()

#Cliente
serverAddr = 'localhost'
serverPortUDP = 50002

clientCachipun = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
clientCachipun.connect((serverAddr, serverPortUDP))

print(clientCachipun)
msg = clientSocket.recv(2048).decode()

while(msg != "2"):
    clientCachipun.send(msg.encode()) #Enviar a servidor Cachipun
    print("[*] Consultando disponibilidad de servidor Cachipun")
    disp_Cachipun = clientCachipun.recvfrom(2048)[0]

    respuesta = disp_Cachipun.decode().split('|')
    print(respuesta)

    print("[*] Disponibilidad de servidor Cachipun " + disp_Cachipun.decode())
    clientSocket.send(disp_Cachipun) #Enviar a cliente la disponibilidad

    disp_servidor = respuesta[0]
    ip = respuesta[1]
    puerto = respuesta[2]

    if(disp_servidor == "NO"):
        print("[*] Servidor Cachipun no disponible")
    else:
        print("[*] Comienzo de partida")
        juegoCachipun(clientSocket, ip, puerto)

    msg = clientSocket.recv(2048).decode()

clientCachipun.close()
mensaje = "OK"
clientSocket.send(mensaje.encode())
clientSocket.close()
print("[*] Se cierra conexión con cliente en ", serverPort)



