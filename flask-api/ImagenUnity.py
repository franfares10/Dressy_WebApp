import base64
import socket
import numpy as np
import cv2

BUFFER_SIZE = 65536
global socketCounter
socketCounter = 0
senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
senderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)


def createSingletonInstance():
    global socketCounter
    if (socketCounter == 0):
        #Creo que el socket porque no se creo
        print("Levanta el socket")
        socket_adress = ('127.0.0.1',7778)
        senderSocket.bind(socket_adress)
        socketCounter = 1
    else:
        print("No creamos la conexion porque ya esta creada")

def generate_frames():
    createSingletonInstance()
    while True:
            msg, clien_addr = senderSocket.recvfrom(BUFFER_SIZE)
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ bytearray(msg) + b'\r\n')

def close_unity_socket():
    senderSocket.close()
