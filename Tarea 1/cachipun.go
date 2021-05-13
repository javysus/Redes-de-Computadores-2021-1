package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"strings"
	"time"
)

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

func puertoPartida(connection_partida *net.UDPConn) {
	BUFFER := 1024
	buffer := make([]byte, BUFFER)
	defer connection_partida.Close()
	for {
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
		n, addr, err := connection.ReadFromUDP(buffer)

		fmt.Printf("-> Se recibe la opción %s\n", string(buffer[0:n]))

		if strings.TrimSpace(string(buffer[0:n])) == "2" {
			mensaje := []byte("OK")
			_, err = connection.WriteToUDP(mensaje, addr)
			fmt.Println("[*] Se cierra servidor Cachipún")
			return
		} else if strings.TrimSpace(string(buffer[0:n])) == "1" {
			disponibilidad := rand.Intn(100)
			var mensaje []byte

			if disponibilidad <= 9 {
				mensaje = []byte("NO")
				_, err = connection.WriteToUDP(mensaje, addr)

			} else {

				//Abrir puerto de partida
				rand.Seed(time.Now().UnixNano())
				puerto_partida := rand.Intn(41) + 10 //Puertos de 50010 al 50050
				port := ":500" + strconv.Itoa(puerto_partida)
				s, err := net.ResolveUDPAddr("udp4", port)

				if err != nil {
					fmt.Println(err)
					return
				}

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
