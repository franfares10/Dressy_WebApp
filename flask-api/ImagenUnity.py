from ast import Break
import base64
import socket
import numpy as np
import cv2
BUFFER_SIZE = 65536

senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
senderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
socketAdress = ('127.0.0.1',7778)


def generate_frames():
    senderSocket.bind(socketAdress)
    print("Inicio el señor sockete")
    while True:
            msg, clien_addr = senderSocket.recvfrom(BUFFER_SIZE)
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ bytearray(msg) + b'\r\n')

def close_unity_socket():
    senderSocket.close()
