
import socket
import threading
import json
import time

IP_server = "192.168.1.200"
port = 5000

def enviar_sms():

	while True:
		mensaje = input("\nMensaje: ")
		destino = input("Destinatario: ")

		datos_mensaje = json.dumps({"Destino":destino,"SMS":mensaje})

		server_socket.sendall(datos_mensaje.encode())

		msg_server = json.loads(server_socket.recv(1024).decode())

		if not msg_server:

<<<<<<< HEAD
			print("No mensaje!!")
=======
			print(msg_server)

>>>>>>> aca65e225446bfa3b3393c003bb89e50fd8ff616
			break

		cliente_B,sms_cliente_B = msg_server.values()

		print("\nMensaje de {}: {}".format(cliente_B,sms_cliente_B))



def recibir_sms():

	while True:

		try:

			mensaje_cliente_B = json.loads(server_socket.recv(1024).decode())

<<<<<<< HEAD
			print("Receptor:",mensaje_cliente_B)
=======
#			print("Receptor: ",server_socket.recv(1024).decode())
>>>>>>> aca65e225446bfa3b3393c003bb89e50fd8ff616

			if mensaje_cliente_B:

				cliente_B,sms_cliente_B = mensaje_cliente_B.values()

#				print("\nMensaje de {}: {}".format(cliente_B,sms_cliente_B))

			else:

				print("\nEl servidor ha cerrado la conexion...")

		except Exception as e:

			print("\nError en el servidor...")
			break

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

			hilo_recepcion = threading.Thread( target = recibir_sms, daemon = True )

			hilo_recepcion.start()

			enviar_sms()

except KeyboardInterrupt:

	print("Desconectando...\n")
	time.sleep(2)
	print("Cliente desconectado.\n")
