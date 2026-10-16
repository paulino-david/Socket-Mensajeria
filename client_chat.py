
import socket
import threading
import json
import time

IP_server = "192.168.1.200"
port = 5000

try:

	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:

		server_socket.connect((IP_server,port))

		nombre = input("\nInserte su nombre: ")

#		datos= "nombre":nombre

		server_socket.sendall(nombre.encode())

		respuesta_servidor = server_socket.recv(1024).decode()


		while respuesta_servidor != "Hola "+nombre+"!!":

			print("\nServidor: "+respuesta_servidor+"\n")

			nombre = input("\nInserte su nombre: ")

#			datos= {"nombre":nombre,"ip":socket.gethostbyname(socket.gethostname())}

			server_socket.sendall(nombre.encode())

			respuesta_servidor = server_socket.recv(1024).decode()
	#		print("No registrado")


		else:

			print("\nServidor:",respuesta_servidor,"\n")

			while True:

				mensaje = input("\nMensaje: ")
				destino = input("Destinatario: ")

				datos_mensaje = json.dumps({"Destino":destino,"SMS":mensaje})

				server_socket.sendall(datos_mensaje.encode())

				msg_server = server_socket.recv(1024).decode()

				if msg_server:

					print(msg_server)
				else:

					print("No mensaje!!")
					break

except KeyboardInterrupt:

	print("Desconectando...\n")
	time.sleep(2)
	print("Cliente desconectado.\n")
