import socket as skt
def trans_jugada(num):
    if (num=='1'):
        return "Piedra"
    elif (num=='2'):
        return "Papel"
    elif (num=='3'):
        return "Tijera"

serverAddr = 'localhost'
puertoServidor = 50001
socketClient = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

socketClient.connect((serverAddr, puertoServidor))
print("Bienvenidx a Cachipun\nEscoja alguna de las siguientes opciones\n1. Comenzar a jugar\n2. Salir")
toSend = input("Opción: ")

if (toSend=='2'):
    run = False
    socketClient.send(toSend.encode()) #Avisar de cerrar conexion
else:
    run = True

while(run):
    socketClient.send(toSend.encode())
    print("[*] Buscando rival...")
    response = socketClient.recv(2048).decode()[0:2]

    if(response=='OK'):
        print("[*] Rival encontrado")
        jugar = True
        print("El juego ha comenzado. El primer jugador en ganar tres partidas gana.\n¿Piedra, papel o tijera?\n1. Piedra\n2. Papel\n3. Tijera")
        
        while(jugar):
            jugada = input("Opción: ")
            jugada = trans_jugada(jugada)
            socketClient.send(jugada.encode()) #Se envia la jugada al servidor intermediario

            print("[*] Usted jugó ", jugada)

            #Recibir jugada del otro jugador
            print("[*] Esperando jugada del contrincante...")
            resultados_part = socketClient.recv(2048).decode().split('|')
            print("[*] El jugador contrincante jugó ", resultados_part[0])

            if(resultados_part[1]=='GANAR'):
                print("[*] Usted ganó el turno")
            elif(resultados_part[1]=='PERDER'):
                print("[*] Usted perdió el turno")
            else:
                print("[*] Hubo un empate en este turno")

            print("[*] MARCADOR: Usted ", resultados_part[2], "| Contrincante ",resultados_part[3])

            if(resultados_part[4]=='WIN'):
                print(["[*] ¡¡¡Usted ha ganado la partida!!!"])
                jugar = False
            elif(resultados_part[4]=='LOSE'):
                print("[*] Usted ha perdido la partida. Suerte para la próxima.")
                jugar = False
            else:
                print("¿Piedra, papel o tijera?\n1. Piedra\n2. Papel\n3. Tijera")

    else:
        print("Los servidores están ocupados. Vuelva a intentarlo más tarde.")
    
    print("Escoja alguna de las siguientes opciones\n1. Comenzar a jugar\n2. Salir")
    toSend = input("Opción: ")

    if (toSend=='2'):
        run = False
        socketClient.send(toSend.encode()) #Avisar de termino a servidor intermedio
        #Terminar ejecucion de servidores
    else:
        run = True

msg = socketClient.recv(2048).decode() #Recibir OK

if(msg=="OK"):
    print("¡Vuelve pronto!")
    socketClient.close()
else:
    print("Ha ocurrido un error")