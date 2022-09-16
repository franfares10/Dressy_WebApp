import base64
import cv2 , imutils
from cvzone.PoseModule import PoseDetector
import socket
import json
import requests


detector = PoseDetector()

#Constantes buffer, ancho, y servicio reporting.
BUFFER_SIZE=65536
WIDHT=400
HISTORICO_URL = "https://dressy-reporting-service.herokuapp.com/api/emociones/historico/"
PRENDA="630f55248ac2207315ff8b0f"
EMOCION="630ea9efb0c20d906714b1c0"
CENTRO="630eba5d10522cae4a888755"


#Variables sockets
senderSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
senderSocket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)
serverAdressPort = ("127.0.0.1",8079)
serverAdressPortCamara = ("127.0.0.1",8080)
serverAdressPortEmotionRectangle = ("127.0.0.1",8081)
serverAdressPortReporting = ("127.0.0.1",8082)



def from_image_to_matrix(imagen):
    formatted_image = imutils.resize(imagen,width=WIDHT) #Resize de la imagen para que  el buffer no explote.
    encoded_info, buffer = cv2.imencode('.jpg',formatted_image,[cv2.IMWRITE_JPEG_QUALITY,80]) #Encode de la imagen para preservar la calidad
    encoded_message = base64.b64encode(buffer)
    return encoded_message

def send_and_process_body_captured_data(img,facesCoordinates):
    senderSocket.sendto(from_image_to_matrix(img),serverAdressPortCamara)
    img = detector.findPose(img) 
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)
    dataUnity = [] #La necesito refrescar para que se envie
    if bboxInfo:
        #center = bboxInfo["center"]
        for lm in lmList:
            dataUnity.extend([lm[1],img.shape[0]-lm[2],lm[3]]) #Sino cambiarlo a height
    senderSocket.sendto(str.encode(str(dataUnity)),serverAdressPort)#Envio por UDP los datos.
    senderSocket.sendto(str.encode(str(facesCoordinates[0])),serverAdressPortEmotionRectangle)
    print("Mando a Unity")
    

def generate_reporting_data(prenda,emocion,centro):
    #Al estar dando errores de sincronimos
    payload = json.dumps({
        "prenda": prenda,
        "emocion":emocion,
        "centro":centro,
        "fecha": "2022-09-13"
    })
    headers={'Content-Type':'application/json'}
    senderSocket.sendto(str.encode(str(payload)),serverAdressPortReporting)
    #result = requests.request("POST", HISTORICO_URL, headers=headers, data=payload) #Ver de ponerle un timeout para que no quede lockeado el thread!
    
    

def send_emotion_label_information(x,y,w,h):
    #Mando los datos a Unity para dibujar el cuadrado.
    unified_string = x+"-"+y+"-"+w+"-"+h
    senderSocket.sendto(str.encode(str(unified_string)),serverAdressPortEmotionRectangle)

def closeSockets():
    senderSocket.close()


