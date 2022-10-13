from ast import If
import base64
from contextlib import closing
from os import times
import cv2, imutils
from cvzone.PoseModule import PoseDetector
import socket
import json
import datetime

detector = PoseDetector()

# Constantes buffer, ancho, y servicio reporting.
BUFFER_SIZE = 65536
WIDHT = 400
HISTORICO_URL = "https://dressy-reporting-service.herokuapp.com/api/emociones/historico/"
PRENDA = "630f55248ac2207315ff8b0f"
EMOCION = "630ea9efb0c20d906714b1c0"
CENTRO = "630eba5d10522cae4a888755"
global prendaEnviada
prendaEnviada = ""

# Variables sockets
senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
senderSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))
#Creo Socket de prueba para testear si el puerto esta abierto. (el de la prenda en Unity.)


serverAdressPort = ("127.0.0.1", 8079)
serverAdressPortCamara = ("127.0.0.1", 8082) #Renderiza la imagen de la camara aca en C Sharp
serverAdressCenterPoint = ("127.0.0.1", 8200)  # Renderiza el punto central del usuario en C Sharp.
serverAdressPortReporting = ("127.0.0.1", 8085) 
serverAdressPortLogicaRopa = ("127.0.0.1", 9100) #Render ropa 

def send_prendas_udp(prendaObjeto): 
    #Me aseguro que esté escuchando el puerto cuando arranca
    senderSocket.sendto(str.encode(str(prendaObjeto)),serverAdressPortLogicaRopa)


def from_image_to_matrix(imagen):
    formatted_image = imutils.resize(imagen)#, width=WIDHT)  # Resize de la imagen para que  el buffer no explote.
    encoded_info, buffer = cv2.imencode('.jpg', formatted_image,
                                        [cv2.IMWRITE_JPEG_QUALITY, 80])  # Encode de la imagen para preservar la calidad
    encoded_message = base64.b64encode(buffer)
    return encoded_message


def send_and_process_body_captured_data(img,faces,prendaElegida): #FaceCoordinates es el x,y,w,h
    senderSocket.sendto(from_image_to_matrix(img), serverAdressPortCamara)
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False) 
    dataUnity = []  # La necesito refrescar para que se envie
    dataUnityCenteredPoint = []
    if bboxInfo:
        center = bboxInfo["center"] #Es el punto del centro!!!!   
        for lm in lmList:   
            dataUnity.extend([lm[1], img.shape[0] - lm[2], lm[3]])  # Sino cambiarlo a height  
        #480 - componente en Y.
        dataUnityCenteredPoint.extend([lmList[12][1]-((lmList[12][1]-lmList[11][1])//2),(lmList[23][2]-((lmList[23][2]-lmList[11][2])//2))])
    senderSocket.sendto(str.encode(str(dataUnity)), serverAdressPort)  # Envio por UDP los datos, no lo necesitaríamos más.
    senderSocket.sendto(str.encode(str(dataUnityCenteredPoint)), serverAdressCenterPoint)
    send_prendas_udp(prendaElegida)
    
    


def generate_reporting_data(prenda, emocion, centro):
    # Al estar dando errores de sincronimos
    payload = json.dumps({
        "prenda": prenda,
        "emocion": emocion,
        "centro": centro,
        "fecha": str(datetime.datetime.now())
    })
    headers = {'Content-Type': 'application/json'}
    senderSocket.sendto(str.encode(str(payload)), serverAdressPortReporting) 
    # result = requests.request("POST", HISTORICO_URL, headers=headers, data=payload) #Ver de ponerle un timeout para que no quede lockeado el thread!


def send_emotion_label_information(x, y, w, h):
    # Mando los datos a Unity para dibujar el cuadrado.
    unified_string = x + "-" + y + "-" + w + "-" + h
    senderSocket.sendto(str.encode(str(unified_string)), serverAdressCenterPoint)


def closeSockets():
    print("Cerrando los sockets")
    senderSocket.close()

def draw_alert_message(img,faces_coordinates,lmList): 
    print(lmList[15]+"-"+lmList[16])
    for (x,y,w,h) in faces_coordinates:
        cv2.putText(img,"FLACO PONETE BIEN",(x,y),thickness=10)
        cv2.rectangle(img,(x, y), (x + w, y + h),(255,0,0),-1)    