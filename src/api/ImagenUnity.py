import socket
import numpy as np
import cv2

BUFFER_SIZE = 65536
global SOCKET_COUNT
SOCKET_COUNT = 0
senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
senderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)


def create_singleton_instance():
    '''
    Metodo que actua como singleton, entre comillas,
    para no crear más de 1 vez el socket que escuche la respuesta de Unity.
    '''

    global SOCKET_COUNT
    if SOCKET_COUNT == 0:
        socket_adress = ('127.0.0.1',7778)
        senderSocket.bind(socket_adress)
        SOCKET_COUNT = 1

def generate_frames():
    '''
    Método que escucha el puerto al cual Unity le envia la captura de la camara,
    para poder renderizarlo en el frontend.
    '''
    create_singleton_instance()
    while True:
        msg = senderSocket.recvfrom(BUFFER_SIZE)
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ bytearray(msg) + b'\r\n'

def close_unity_socket():
    '''
    Método que cierra el socket de escucha de Unity.
    '''
    senderSocket.close()
