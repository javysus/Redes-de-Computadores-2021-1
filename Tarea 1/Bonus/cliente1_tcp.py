import socket as skt
#Función que transforma el numero entregado a la opción piedra, papel o tijera
def trans_jugada(num):
    if (num=='1'):
        return "Piedra"
    elif (num=='2'):
        return "Papel"
    elif (num=='3'):
        return "Tijera"

#Se define localhost y el puerto 50001 donde se realizará la conexión TCP
serverAddr = 'localhost'
puertoServidor = 50001
socketClient = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

socketClient.connect((serverAddr, puertoServidor))
print("¡Bienvenidx a Cachipun!\nEscoja alguna de las siguientes opciones\n1. Comenzar a jugar\n2. Salir")
toSend = input("Opción: ")

#Opción: Cerrar el programa
if (toSend=='2'):
    run = False
    socketClient.send(toSend.encode()) #Avisar de cerrar conexion
else:
    run = True

#Opción: Comenzar partida
while(run):
    #Se avisa del comienza de la partida al servidor Intermedio 1
    socketClient.send(toSend.encode())
    print("[*] Buscando rival...")
    response = socketClient.recv(2048).decode()[0:2]

    #Si servidor Cachipún esta disponible
    if(response=='OK'):
        print("[*] Rival encontrado")
        jugar = True
        print("El juego ha comenzado. El primer jugador en ganar tres partidas gana.\n¿Piedra, papel o tijera?\n1. Piedra\n2. Papel\n3. Tijera")
        
        while(jugar):
            jugada = input("Opción: ")
            jugada = trans_jugada(jugada)
            socketClient.send(jugada.encode()) #Se envia la jugada al servidor intermediario

            print("[*] Usted jugó ", jugada)

            #Recibir jugada del otro jugador en formato Jugada|Resultado(GANAR, PERDER, EMPATE)|Puntos jugador|Puntos bot|Estado final(WIN, LOSE, SEGUIR)
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

    #Si servidor Cachipun no esta disponible
    else:
        print("Los servidores están ocupados. Vuelva a intentarlo más tarde.")
    
    print("Escoja alguna de las siguientes opciones\n1. Comenzar a jugar\n2. Salir")
    toSend = input("Opción: ")

    #Salir del juego
    if (toSend=='2'):
        run = False
        #Se avisa a servidor Intermedio del fin del programa
        socketClient.send(toSend.encode()) 
    else:
        run = True
        
#Se espera confirmación de cierre
msg = socketClient.recv(2048).decode() 

if(msg=="OK"):
    print("¡Vuelve pronto!")
    socketClient.close()
else:
    print("Ha ocurrido un error")