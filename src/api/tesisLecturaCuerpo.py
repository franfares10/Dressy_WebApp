import base64
import socket
import json
import datetime
import cv2, imutils
from cvzone.PoseModule import PoseDetector

detector = PoseDetector() #Instancio el detector de poses de CV2

# Constantes buffer, ancho, y servicio reporting y prenda enviada.
BUFFER_SIZE = 65536
WIDHT = 400
HISTORICO_URL = "https://dressy-reporting-service.herokuapp.com/api/emociones/historico/"
global PRENDA_ENVIADA
PRENDA_ENVIADA = ""

#Instanciamos y configuramos las propiedades de los sockets
senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
senderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)


serverAdressPortCamara = ("127.0.0.1", 8082) #Encargado de enviar la imagen de la camara a Unity.
serverAdressCenterPoint = ("127.0.0.1", 8200) #Encargado de enviar el punto central para orientar a la prenda en Unity.
serverAdressPortReporting = ("127.0.0.1", 8085) #Encargado de fordwardear la request a loader interno.
serverAdressPortLogicaRopa = ("127.0.0.1", 9100) #Encargado de enviar la ropa elegida a Unity.

def send_prendas_udp(prenda_objeto):
    '''
    Método que envía la prenda elegida hacia el servicio en Unity,
    para luego ser procesada por la respectiva lógica y
    poder renderizar la prenda correspondiente.
    '''
    senderSocket.sendto(str.encode(str(prenda_objeto)),serverAdressPortLogicaRopa)


def from_image_to_matrix(imagen):
    '''
    Método encargado de resizear la imagen que captura la camara,
    pasarla a jpg,encodearla a base64 con una calidad del 80% 
    y devolverla para luego mandar a Unity.
    '''
    formatted_image = imutils.resize(imagen)  # Resize de la imagen para que  el buffer no explote.
    # Encode de la imagen para preservar la calidad
    buffer = cv2.imencode('.jpg', formatted_image, [cv2.IMWRITE_JPEG_QUALITY, 80])
    encoded_message = base64.b64encode(buffer)
    return encoded_message

def send_and_process_body_captured_data(img,prenda_elegida): #FaceCoordinates es el x,y,w,h
    '''Método encargado de detectar el punto central del cuerpo del usuario. Tomando
    como referencia los hombros y la cintura. Además, se encarga de enviar el base64 de la imagen
    capturada por CV2 hacia Unity, además de las coordenadas del punto central'''
    senderSocket.sendto(from_image_to_matrix(img), serverAdressPortCamara)
    img = detector.findPose(img,draw=False)
    lm_list, bbox_info = detector.findPosition(img, bboxWithHands=False,draw=False)
    data_unity = []
    data_unity_centered_point = []
    if bbox_info:
        for lm in lm_list:
            data_unity.extend([lm[1], img.shape[0] - lm[2], lm[3]])
        data_unity_centered_point.extend(
            [
                lm_list[12][1]-((lm_list[12][1]-lm_list[11][1])//2),
                (lm_list[23][2]-((lm_list[23][2]-lm_list[11][2])//2))
            ]
        )
    senderSocket.sendto(str.encode(str(data_unity_centered_point)), serverAdressCenterPoint)
    send_prendas_udp(prenda_elegida)
    