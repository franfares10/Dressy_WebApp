#Script que lee si todos los puertos que usa Dressy están abiertos o cerrados.
import socket
from contextlib import closing 


lista_puertos = [8079,8080,8200,8085,9100,8082]

BUFFER_SIZE = 65536
HOST = "127.0.0.1"

testingSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
testingSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)

for puerto in lista_puertos:
    with closing(testingSocket) as sock:
        if testingSocket.connect_ex((HOST, puerto)) == 0:
            print("Puerto con la dirección {} esta abierto".format(puerto))
        else:
            print("Puerto con la dirección {} NO esta abierto".format(puerto))