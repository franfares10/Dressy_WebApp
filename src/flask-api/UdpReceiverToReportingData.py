import json
import socket
import threading
from threading import Thread
import requests

BUFFER_SIZE = 65536
# HISTORICO_URL = "https://dressy-reporting-service.herokuapp.com/api/emociones/historico/"

server_reporting_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_reporting_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
reporting_socket_adress = ("127.0.0.1", 8085)
server_reporting_socket.bind(reporting_socket_adress)


class sender_reporting_data_thread(Thread):
    '''Clase que tenía como proposito servir de generadora de Threads,
    con los datos para enviar a reporting. Además, de contar la cantidad
    de request por uso de aplicación.
    La misma se deprecó por encontrar una solución más óptima'''

    def __init__(self, payload):
        Thread.__init__(self)
        self.payload = payload
        self.headers = {'Content-Type':'application/json'}
        self.account = 0
        self.URL = "https://dressy-reporting-service.herokuapp.com/api/emociones/historico/"

    def run(self):
        try:
            requests.request("POST", self.URL, headers=self.headers,
                             data=self.payload)  # Ver de ponerle un timeout para que no quede lockeado el thread!
            self.account += 1
        except RuntimeError:
            print("XX. Error publicando")


lista_request = 0
lista_reprocesos = []
#Proceso que escuchaba el puerto 8085, el mismo corría stand-alone. Y por cada llamado recibido,
#instanciaba una clase que permitía enviar un post al servicio de reporting.
while True:
    mensajeUdp, infoSocket = server_reporting_socket.recvfrom(BUFFER_SIZE)
    if lista_request == 0:
        print("XX. Creacion de un unico thread en el pool")
        thread_instanciado = sender_reporting_data_thread(json.dumps(json.loads(mensajeUdp)))
        lista_request = -1
        if not thread_instanciado.is_alive():
            print("XX. Starteo el thread")
            thread_instanciado.start()
    thread_instanciado.run()
    print("XX. Request ejecutadas: ", thread_instanciado.account)