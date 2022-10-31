from concurrent.futures import ThreadPoolExecutor
from multiprocessing.connection import wait
import threading
from tkinter.tix import Tree
from urllib import request
from webbrowser import get
from flask import Flask,render_template,Response,request
import cv2
import os
from sys import maxsize
from time import sleep, time
import numpy as np
import tensorflow as tf
import requests 
import json
from tesisLecturaCuerpo import closeSockets, generate_reporting_data, send_and_process_body_captured_data,send_prendas_udp
from ImagenUnity import generate_frames,close_unity_socket

app=Flask(__name__)
lock = threading.Lock()
franUrl = 'E:\\Escritorio\\' #URL para clasificadores y modelo.
ivanUrl = 'D:\\DressyFrontend\\' #URL para clasificadores y modelo.
face_classifier = cv2.CascadeClassifier(r'D:\\DressyFrontend\\Dressy_WebApp\\flask-api\\model\\haarcascade_frontalface_default.xml') #Cargamos estructura de pre-classifier.
classifier = tf.keras.models.load_model(r'D:\\DressyFrontend\\Dressy_WebApp\\flask-api\\model\\model_v7.h5') #Cargamos modelo de inteligencia artificial.
HISTORICO_URL = "https://dressy-reporting-service.herokuapp.com/api/emociones/historico/"
emotion_labels = ['disgust', 'happy', 'neutral','sad','surprise']
CENTRO = "630eba5d10522cae4a888755"
procesarMain = 0
global legalState
legalState = False
global genderState
genderState = "genero"


def createRegistro(prenda,emocion,centro,genero):
    '''Genera y envía el request hacia el servicio de reporting'''
    payload = json.dumps({
                        "prenda": prenda,
                        "emocion": emocion,
                        "centro": centro,
                        "genero":genero
                        })
    headers =  {
                'Content-Type': 'application/json'
                }

    response = requests.request("POST", HISTORICO_URL, headers=headers, data=payload)
    print(response.text)

def modelPrediction(prenda,tipo,marca,procesar):
    '''Método que captura la imagen de la camara, carga el modelo de microexpresiones y envia datos hacia Unity y servicio de reporting'''
    global procesarMain
    if(procesarMain):
        global lock
        cap=cv2.VideoCapture(0)
        currentEmotion = ""
        if cap.isOpened():
            rval, frame = cap.read()
        else:
            rval = False
        
        while rval and procesarMain:
            with lock:
                _, frame = cap.read()
                labels = []
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, minNeighbors=10)

                threadPool.submit(send_and_process_body_captured_data,frame,faces,marca)
                for (x, y, w, h) in faces:
                    # Dibuja el rectangulo formando los ejes de la cara.
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)

                    roi_gray = gray[y:y+h, x:x+w]
                    roi_gray = cv2.resize(roi_gray, (48, 48),interpolation=cv2.INTER_AREA) #Resize para que tenga el input correcto la imagen capturada para que el modelo la reconozca

                    if np.sum([roi_gray]) != 0:
                        
                        roi = tf.keras.preprocessing.image.img_to_array(roi_gray)
                        roi = np.expand_dims(roi, axis=0)
                        
                        prediction = classifier.predict(roi)

                        label = emotion_labels[prediction.argmax()]

                        probabilidadPreddicion = str(prediction[0][np.argmax(prediction[0])])

                        label_position = (x, y)
                        cv2.putText(frame, label+probabilidadPreddicion, label_position,
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        if( currentEmotion!="" and label!=currentEmotion and label!="neutral"):
                            global legalState 
                            global genderState
                            if(legalState=="False"):
                                #Se fija si el legalState (si firmo los TyC el usuario, es falso. SI es falso, no guarda la informacion de las expresiones.)
                                print("No acepto TyC, no podemos guardar informacion")
                            else:
                                print("CAMBIE DE EMOCION")
                                thread = threading.Thread(target=createRegistro,args=(prenda,label,CENTRO,genderState))
                                thread.start()
                            currentEmotion = label
                        else:
                            currentEmotion = label
                    
                    (flag, encodedImage) = cv2.imencode(".jpg",frame)

                    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ bytearray(encodedImage) + b'\r\n')
                cv2.imshow('Emotion Detector', frame)
                if not procesarMain:
                    cap.release()
                    cv2.destroyAllWindows() 
                    print("DESTRUI TODO")
                    break
        cap.release()
        cv2.destroyAllWindows() 
        print("DESTRUI TODO")
    else:
        cap.release()
        cv2.destroyAllWindows() 
        print("DESTRUI TODO")

@app.route('/video_feed',methods = ['GET'])
def video_feed():
    prenda = request.args.get('prenda')
    tipo = request.args.get('tipo')
    marca = request.args.get('marca')
    procesar = request.args.get('procesar')
    global procesarMain
    procesarMain = procesar
    print("PROCESAR"+procesar)
    send_prendas_udp(marca) #Enviamos la ropa elegida del usuario hacia Unity.
    return Response(modelPrediction(prenda,tipo,marca,procesar), mimetype= "multipart/x-mixed-replace; boundary=frame")


@app.route('/stop_video',methods = ['POST'])
def stop_video():
    global procesarMain
    procesarMain = 0
    return "termino todo bien"

@app.route('/unity_image',methods=['GET'])
def render_unity_image():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/termsAndConditions',methods=['POST'])
def set_terms_and_conditions():
    #Llamado que recibe el estado legal y el genero del usuario.
    global legalState
    legalState = request.args.get('terms')
    global genderState
    genderState = request.args.get('gender')
    print("Estado legal: {}, genero:{} ".format(legalState,genderState))
    return "ok"


if __name__=="__main__":
    threadPool = ThreadPoolExecutor(max_workers=2)
    app.run(debug=False)


cv2.destroyAllWindows() 