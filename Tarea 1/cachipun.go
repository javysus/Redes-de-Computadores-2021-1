package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"strings"
	"time"
)

//Jugada random del bot
func jugadaBot() (jugada string) {
	rand.Seed(time.Now().UnixNano())
	opcion := rand.Intn(3)

	if opcion == 0 {
		jugada = "Piedra"
	} else if opcion == 1 {
		jugada = "Papel"
	} else {
		jugada = "Tijera"
	}
	return
}

//Se realiza y envían las jugadas en el puerto de partida
func puertoPartida(connection_partida *net.UDPConn) {
	BUFFER := 1024
	buffer := make([]byte, BUFFER)
	defer connection_partida.Close()
	for {
		//Se recibe los mensajes "JUGAR" para generar una jugada aleatoria o "FIN" para terminar la partida y cerrar el puerto
		n, addr, err := connection_partida.ReadFromUDP(buffer)
		fmt.Printf("-> Se recibe la opción %s\n", string(buffer[0:n]))

		if strings.TrimSpace(string(buffer[0:n])) == "JUGAR" {
			bot := jugadaBot()
			mensaje := []byte(bot)
			fmt.Printf("[*] Se envia %s\n", bot)
			_, err = connection_partida.WriteToUDP(mensaje, addr)

			if err != nil {
				fmt.Println(err)
				return
			}
		} else if strings.TrimSpace(string(buffer[0:n])) == "FIN" {
			fmt.Print("[*] Cerrando puerto de partida...\n")
			return
		}

		if err != nil {
			fmt.Println(err)
			return
		}
	}
}

func main() {
	//Servidor en puerto 50002
	puerto := ":50002"
	BUFFER := 1024
	s, err := net.ResolveUDPAddr("udp4", puerto)

	if err != nil {
		fmt.Println(err)
		return
	}

	connection, err := net.ListenUDP("udp4", s)
	if err != nil {
		fmt.Println(err)
		return
	}

	defer connection.Close()
	buffer := make([]byte, BUFFER)

	fmt.Printf("[*] Servidor Cachipun abierto en puerto %s\n", puerto)

	for {
		//Se lee lo recibido por servidor Intermedio, opciones de jugar o finalizar programa
		n, addr, err := connection.ReadFromUDP(buffer)

		fmt.Printf("-> Se recibe la opción %s\n", string(buffer[0:n]))

		if strings.TrimSpace(string(buffer[0:n])) == "2" {
			mensaje := []byte("OK")
			_, err = connection.WriteToUDP(mensaje, addr)
			fmt.Println("[*] Se cierra servidor Cachipún")
			return
		} else if strings.TrimSpace(string(buffer[0:n])) == "1" {
			//Disponibilidad aleatoria
			rand.Seed(time.Now().UnixNano())
			disponibilidad := rand.Intn(100)
			fmt.Print(disponibilidad)

			var mensaje []byte

			//Probabilidad de 10% de no estar disponible
			if disponibilidad <= 9 {
				mensaje = []byte("NO")
				fmt.Println("[*] Servidor no disponible")
				_, err = connection.WriteToUDP(mensaje, addr)

			} else {
				//Abrir puerto de partida aleatorio
				rand.Seed(time.Now().UnixNano())
				puerto_partida := rand.Intn(41) + 10 //Puertos de 50010 al 50050
				port := ":500" + strconv.Itoa(puerto_partida)
				s, err := net.ResolveUDPAddr("udp4", port)

				if err != nil {
					fmt.Println(err)
					return
				}

				//Crear conexión en el puerto de partida aleatorio
				connection_partida, err := net.ListenUDP("udp4", s)
				if err != nil {
					fmt.Println(err)
					return
				}

				fmt.Printf("[*] Partida iniciada en el puerto %s\n", port)

				//Enviar disponibilidad y puerto
				disp_port := "OK|localhost|" + "500" + strconv.Itoa(puerto_partida)
				mensaje = []byte(disp_port)
				_, err = connection.WriteToUDP(mensaje, addr)

				puertoPartida(connection_partida)
				fmt.Printf("[*] Partida en puerto 500%s cerrada\n", strconv.Itoa(puerto_partida))
			}

		}

		if err != nil {
			fmt.Println(err)
			return
		}

	}
}
