import socket as skt 

#Función que define cuando el jugador gana 
def ganarPuntos(jugador, bot):
    if (jugador == 'Piedra') and (bot=='Tijera'):
        return True
    if (jugador == 'Papel') and (bot=='Piedra'):
        return True
    if (jugador == 'Tijera') and (bot=='Papel'):
        return True
    return False

#Función que ejecuta la partida
def juegoCachipun(clienteSocket, ip, puerto):
    #Comunicarse con puerto de partida
    serverAddr = ip
    serverPortUDP = int(puerto)

    #Conexión con puerto de partida 
    clientePartida = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
    clientePartida.connect((serverAddr, serverPortUDP))

    #Puntos
    puntos_jugador = 0
    puntos_servidor = 0

    run = True
    while(run):
        #Se recibe la jugada inicial
        jug_inicial = clienteSocket.recv(2048).decode()

        #Se solicita jugada del servidor Cachipun, es decir, del otro jugador
        clientePartida.send(jug_inicial.encode())
        print("[*] Esperando jugada...")
        bot_jug = clientePartida.recvfrom(2048)[0].decode()
        print("[*] El contrincante juega ", bot_jug)


        #Casos de empate, ganar o perder ronda
        if(jug_inicial == bot_jug): 
            resultado = "EMPATE"
        elif ganarPuntos(jug_inicial, bot_jug):
            resultado = "GANAR"
            puntos_jugador+=1
        else:
            resultado = "PERDER"
            puntos_servidor+=1

        #Casos de ganar, perder la partida o seguir con otra ronda
        if (puntos_jugador==3):
            msg_cliente = bot_jug+'|'+resultado+'|'+str(puntos_jugador)+'|'+str(puntos_servidor)+'|WIN'
            run = False
        elif (puntos_servidor == 3):
            msg_cliente = bot_jug+'|'+resultado+'|'+str(puntos_jugador)+'|'+str(puntos_servidor)+'|LOSE'
            run = False
        else:
            msg_cliente = bot_jug+'|'+resultado+'|'+str(puntos_jugador)+'|'+str(puntos_servidor)+'|SEGUIR'

        #Se envia los resultados al Cliente de forma Jugada|Resultado(GANAR, PERDER, EMPATE)|Puntos jugador|Puntos bot|Estado final(WIN, LOSE, SEGUIR)
        clienteSocket.send(msg_cliente.encode())

    #Avisar a Cachipun de que la partida termino
    msg = "FIN"
    print("[*] Partida terminada")
    clientePartida.send(msg.encode())
    clientePartida.close()
    print("[*] Se cierra conexión con servidor Cachipún en ", puerto)


#Servidor que se comunica con Cliente
serverPort = 50003

serverSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM) #AF_INET: IPV4, SOCK_STREAM: TCP

serverSocket.bind(('', serverPort))

serverSocket.listen(1)

print("[*] Servidor TCP escuchado en: ", serverPort)
clientSocket, clientAddr = serverSocket.accept()

#Cliente que se comunica con Cachipun
serverAddr = 'localhost'
serverPortUDP = 50002

clientCachipun = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
clientCachipun.connect((serverAddr, serverPortUDP))

#Recibir la opción de Cliente (1 para jugar, 2 para terminar)
msg = clientSocket.recv(2048).decode()

while(msg != "2"):
    #Enviar a servidor Cachipun la opción para consultar disponibilidad
    clientCachipun.send(msg.encode()) 
    print("[*] Consultando disponibilidad de servidor Cachipun")

    #Recibir respuesta
    disp_Cachipun = clientCachipun.recvfrom(2048)[0] 
    respuesta = disp_Cachipun.decode()

    print("[*] Disponibilidad de servidor Cachipun " + disp_Cachipun.decode())
    clientSocket.send(disp_Cachipun) #Enviar a cliente la disponibilidad

    if(respuesta == "NO"):
        print("[*] Servidor Cachipun no disponible")
    else:
        respuesta = respuesta.split('|')
        ip = respuesta[1]
        puerto = respuesta[2]
        print("[*] Comienzo de partida")
        juegoCachipun(clientSocket, ip, puerto)

    msg = clientSocket.recv(2048).decode()

clientCachipun.close()
mensaje = "OK"
clientSocket.send(mensaje.encode())
clientSocket.close()
print("[*] Se cierra conexión con cliente en ", serverPort)



