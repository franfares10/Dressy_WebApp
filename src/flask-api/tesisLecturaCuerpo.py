from ast import If
import base64
from contextlib import closing
from os import times
import cv2, imutils
from cvzone.PoseModule import PoseDetector
import socket
import json
import datetime

detector = PoseDetector() #Instancio el detector de poses de CV2

# Constantes buffer, ancho, y servicio reporting y prenda enviada.
BUFFER_SIZE = 65536
WIDHT = 400
HISTORICO_URL = "https://dressy-reporting-service.herokuapp.com/api/emociones/historico/"
global prendaEnviada
prendaEnviada = ""

#Instanciamos y configuramos las propiedades de los sockets
senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
senderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)


serverAdressPortCamara = ("127.0.0.1", 8082) #Encargado de enviar la imagen de la camara a Unity.
serverAdressCenterPoint = ("127.0.0.1", 8200) #Encargado de enviar el punto central para orientar a la prenda en Unity.
serverAdressPortReporting = ("127.0.0.1", 8085) #Encargado de fordwardear la request a loader interno.
serverAdressPortLogicaRopa = ("127.0.0.1", 9100) #Encargado de enviar la ropa elegida a Unity.

def send_prendas_udp(prendaObjeto): 
    '''Método que envía la prenda elegida hacia el servicio en Unity, para luego ser procesada por
    la respectiva lógica y poder renderizar la prenda correspondiente.'''
    senderSocket.sendto(str.encode(str(prendaObjeto)),serverAdressPortLogicaRopa)


def from_image_to_matrix(imagen):
    '''Método encargado de resizear la imagen que captura la camara, pasarla a jpg, 
    encodearla a base64 con una calidad del 80% y devolverla para luego mandar a Unity.'''
    formatted_image = imutils.resize(imagen)  # Resize de la imagen para que  el buffer no explote.
    encoded_info, buffer = cv2.imencode('.jpg', formatted_image,
                                        [cv2.IMWRITE_JPEG_QUALITY, 80])  # Encode de la imagen para preservar la calidad
    encoded_message = base64.b64encode(buffer)
    print("Se está mandando este mensaje: {}".format(len(encoded_message)))
    return encoded_message


def send_and_process_body_captured_data(img,faces,prendaElegida): #FaceCoordinates es el x,y,w,h
    '''Método encargado de detectar el punto central del cuerpo del usuario. Tomando
    como referencia los hombros y la cintura. Además, se encarga de enviar el base64 de la imagen
    capturada por CV2 hacia Unity, además de las coordenadas del punto central'''
    senderSocket.sendto(from_image_to_matrix(img), serverAdressPortCamara)
    img = detector.findPose(img,draw=False)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False,draw=False) 
    dataUnity = []
    dataUnityCenteredPoint = []
    if bboxInfo:
        center = bboxInfo["center"]
        for lm in lmList:   
            dataUnity.extend([lm[1], img.shape[0] - lm[2], lm[3]])
        dataUnityCenteredPoint.extend([lmList[12][1]-((lmList[12][1]-lmList[11][1])//2),(lmList[23][2]-((lmList[23][2]-lmList[11][2])//2))])
    senderSocket.sendto(str.encode(str(dataUnityCenteredPoint)), serverAdressCenterPoint)
    send_prendas_udp(prendaElegida)
    
    


def generate_reporting_data(prenda, emocion, centro):
    '''* DEPRECADO *. Método encargado de enviar información al handler propio de eventos
    que luego enviaba la información al servicio de reportería.'''
    payload = json.dumps({
        "prenda": prenda,
        "emocion": emocion,
        "centro": centro,
        "fecha": str(datetime.datetime.now())
    })
    headers = {'Content-Type': 'application/json'}
    senderSocket.sendto(str.encode(str(payload)), serverAdressPortReporting) 




def closeSockets():
    '''Método que cierra los sockets que envían la información a Unity. * DEPRECADO *'''
    print("Cerrando los sockets...")
    senderSocket.close()   
