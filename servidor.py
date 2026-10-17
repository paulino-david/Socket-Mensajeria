
import socket
import threading
import json


IP = socket.gethostbyname(socket.gethostname())
port = 5000

print(IP)

clientes = {}
bloqueo = threading.Lock()

def gestor_clientes(cliente,direccion):

	def registrar(nombre):

		with bloqueo:

			if nombre not in clientes.keys():
#			print(nombre,"in" ,clientes.keys(),"=",nombre in clientes.keys())

				clientes[nombre] = cliente

#				print(clientes)

				return True


	def verificar_registro_completo(nombre,IP_cliente):

#		print(tuple(nombre,IP_cliente))

		with bloqueo:

			return False


	try:

		nombre_cliente = cliente.recv(1024).decode()

#		print(datos_cliente)

		# Aqui se respone al cliente de una manera determinada si encia datos VACIOS, y se queda atento el servidor hasta que el cliente envie un dato

#		Si es que envia DATOS VACIOS

		while not  nombre_cliente:

			cliente.sendall("\nDatos no recibidos..\n".encode())

			nombre_cliente = cliente.recv(1024).decode()

#			print(datos_cliente)

#		Si envia datos

		else:

#			cliente.sendall("\nDatos recibidos..\n".encode())

			respuesta_verificacion = registrar(nombre_cliente)

#			print(verificar_registro_completo(nombre,IP_cliente))

		# Aqui se verifica si el cliente ya existe en los registros.

		# Si es que el cliente ya fue registrado antes, envia a el cliente que se esta registradndo un mensaje, y queda atento por si va a enviar uno nuevo

			while not respuesta_verificacion:

				cliente.sendall("Ya esta registrado un cliente con este nombre..\n".encode())

				nombre_cliente = cliente.recv(1024).decode()

				respuesta_verificacion = registrar(nombre_cliente)


#		Si el cliente no fue registrado, lo registra y le avisa al cliente; luego le permite enviar mensajes

			else:

#				print(list(clientes.items()))

				cliente.sendall("Hola {}!!".format(nombre_cliente).encode())

				print("\nCliente", nombre_cliente, "conectado...\n")

				try:

					with cliente:

						while True:

							msg = json.loads(cliente.recv(1024).decode())

							if msg:

								destino,sms = msg.values()

#								print(sms)

#								print(clientes[destino])

								cliente_destino = clientes[destino]

								mensaje_enviar = json.dumps({"enviador":nombre_cliente,"mensaje":sms})

								cliente_destino.sendall(mensaje_enviar.encode())

								cliente.sendall(json.dumps({"enviador":"Servidor","mensaje":"Mensaje enviado"}).encode())

#								print("Mensaje de",nombre_cliente,":",msg,"\n")

							else:
								print(nombre_cliente+" desconectado..\n")
								break

				except:

					print(nombre_cliente+" desconectado..\n")



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

