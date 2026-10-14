
import socket
import threading
import json


IP = socket.gethostbyname(socket.gethostname())
port = 5000

clientes = {}
bloqueo = threading.Lock()

def gestor_clientes(cliente,direccion):

	def registrar(nombre,IP_cliente):

		with bloqueo:

			if nombre not in clientes.keys():
#			print(nombre,"in" ,clientes.keys(),"=",nombre in clientes.keys())

				clientes[nombre] = IP_cliente

				print(clientes)

				return True


	def verificar_registro_completo(nombre,IP_cliente):

		with bloqueo:

			print(tuple(nombre,IP_cliente))

			return False


	try:

		datos_cliente = json.loads(cliente.recv(1024).decode())

#		print(datos_cliente)

		# Aqui se respone al cliente de una manera determinada si encia datos VACIOS, y se queda atento el servidor hasta que el cliente envie un dato

#		Si es que envia DATOS VACIOS

		while not  datos_cliente["nombre"]:

			cliente.sendall("\nDatos no recibidos..\n".encode())

			datos_cliente = json.loads(cliente.recv(1024).decode())

#			print(datos_cliente)

#		Si envia datos

		else:

#			cliente.sendall("\nDatos recibidos..\n".encode())

			nombre = datos_cliente["nombre"]
			IP_cliente = datos_cliente["ip"]

#			print(verificar_registro_completo(nombre,IP_cliente))

			respuesta_verificacion = registrar(nombre,IP_cliente)

		# Aqui se verifica si el cliente ya existe en los registros.

		# Si es que el cliente ya fue registrado antes, envia a el cliente que se esta registradndo un mensaje, y queda atento por si va a enviar uno nuevo

			while not respuesta_verificacion:

				cliente.sendall("Ya esta registrado un cliente con este nombre..\n".encode())

				datos_cliente = json.loads(cliente.recv(1024).decode())

				nombre = datos_cliente["nombre"]

				IP_cliente = datos_cliente["ip"]

				respuesta_verificacion = registrar(nombre,IP_cliente)


#		Si el cliente no fue registrado, lo registra y le avisa al cliente; luego le permite enviar mensajes

			else:

				print(list(clientes.items()))

				cliente.sendall("Cliente {} registrado".format(nombre).encode())

				print("\nCliente", nombre, "registrado...\n")

				try:

					with cliente:

						while True:

							msg = cliente.recv(1024).decode()

							if msg:

								cliente.sendall("Mensaje recibido".encode())

								print("Mensaje de",nombre,":",msg,"\n")

							else:
								print(nombre+" desconectado..\n")
								break

				except ConnectionResetError:

					print(nombre+" desconectado..\n")



	except:

		print("Error en el cliente..")


try:

	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_sock:

		server_sock.bind((IP,port))

		print("Servidor escuchando en el puerto 5000...")

		server_sock.listen(10)


		while True:

			client_sock, client_address = server_sock.accept()


			hilo = threading.Thread(target = gestor_clientes, args = (client_sock, client_address))

			hilo.start()


except KeyboardInterrupt:

	print("\nServidor cerrado por Ctrl + C\n")

