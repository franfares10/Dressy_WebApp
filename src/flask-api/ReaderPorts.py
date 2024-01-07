import socket
from contextlib import closing 


lista_puertos = [8080,8200,8085,9100,8082]

BUFFER_SIZE = 65536
HOST = "127.0.0.1"

#Script que itera los puertos que usa Dressy para ver si están abiertos o no. En caso de que alguno este abierto
#por algún proceso de la computadora de la persona que pruebe, favor de cerrarlo.

#Ejemplo de caso exitoso, es decir, como se debería ver el resultado para poder usar la aplicación.

#Puerto con la dirección 8080 NO esta abierto
#Puerto con la dirección 8200 NO esta abierto
#Puerto con la dirección 8085 NO esta abierto
#Puerto con la dirección 9100 NO esta abierto
#Puerto con la dirección 8082 NO esta abierto

testingSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
testingSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)

for puerto in lista_puertos:
    with closing(testingSocket) as sock:
        if testingSocket.connect_ex((HOST, puerto)) == 0:
            print("Puerto con la dirección {} esta abierto".format(puerto))
        else:
            print("Puerto con la dirección {} NO esta abierto".format(puerto))