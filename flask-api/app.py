from concurrent.futures import ThreadPoolExecutor
from multiprocessing.connection import wait
import threading
from urllib import request
from flask import Flask,render_template,Response,request
import cv2
import os
from sys import maxsize
#from keras.models import load_model
from time import sleep, time
import numpy as np
import tensorflow as tf
import requests 
import json
from tesisLecturaCuerpo import CENTRO, EMOCION, PRENDA, closeSockets, generate_reporting_data, send_and_process_body_captured_data,send_prendas_udp
from ImagenUnity import generate_frames,close_unity_socket
#from flask_cors import CORS

app=Flask(__name__)
#CORS(app)
lock = threading.Lock()
face_classifier = cv2.CascadeClassifier(r'E:\\Escritorio\\Dressy_WebApp\\flask-api\\model\\haarcascade_frontalface_default.xml')
classifier = tf.keras.models.load_model(r'E:\\Escritorio\\Dressy_WebApp\\flask-api\\model\\model_v7.h5') #El que entrenamos nosotros en jupyter
HISTORICO_URL = "https://dressy-reporting-service.herokuapp.com/api/emociones/historico/"
emotion_labels = ['disgust', 'happy', 'neutral','sad','surprise']
CENTRO = "630eba5d10522cae4a888755"
procesarMain = 0


def createRegistro(prenda,emocion,centro):
    payload = json.dumps({
                        "prenda": prenda,
                        "emocion": emocion,
                        "centro": centro
                        })
    headers =  {
                'Content-Type': 'application/json'
                }

    response = requests.request("POST", HISTORICO_URL, headers=headers, data=payload)
    print(response.text)

def modelPrediction(prenda,tipo,marca,procesar):
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

                #threadPool.submit(send_and_process_body_captured_data,frame,faces,prenda)
                for (x, y, w, h) in faces:
                    # Dibuja el rectangulo formando los ejes de la cara.
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)

                    roi_gray = gray[y:y+h, x:x+w]
                    roi_gray = cv2.resize(roi_gray, (48, 48),interpolation=cv2.INTER_AREA)

                    if np.sum([roi_gray]) != 0:
                        
                        roi = tf.keras.preprocessing.image.img_to_array(roi_gray)
                        roi = np.expand_dims(roi, axis=0)
                        
                        prediction = classifier.predict(roi)

                        label = emotion_labels[prediction.argmax()]
                        #print(emotion_labels[np.argmax(prediction[0])])

                        probabilidadPreddicion = str(prediction[0][np.argmax(prediction[0])])

                        label_position = (x, y)
                        cv2.putText(frame, label+probabilidadPreddicion, label_position,
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        if( currentEmotion!="" and label!=currentEmotion and label!="neutral"):
                            print("CAMBIE DE EMOCION")
                            thread =threading.Thread(target=createRegistro,args=(prenda,label,CENTRO))
                            thread.start()
                            #threadPool.submit(generate_reporting_data,PRENDA, EMOCION, CENTRO)
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
        print("Antes:", threading.enumerate())
        #threadPool.shutdown(cancel_futures=True)
        #threadPool.shutdown(wait=True) #Bajo el Pool de Threads incluso si quedó alguno corriendo.
        print("Dps:", threading.enumerate())
    else:
        cap.release() #Esta accediendo a algo que está definido en otro lugar, borrar y ver que pasa.
        cv2.destroyAllWindows() 
        print("DESTRUI TODO")
        print("Antes else:", threading.enumerate())
        #threadPool.shutdown(wait=True,cancel_futures=True)  #Bajo el Pool de Threads incluso si quedó alguno corriendo.
        print("Dps Else:", threading.enumerate())

@app.route('/video_feed',methods = ['GET'])
def video_feed():
    prenda = request.args.get('prenda')
    tipo = request.args.get('tipo')
    marca = request.args.get('marca')
    procesar = request.args.get('procesar')
    global procesarMain
    procesarMain = procesar
    print("PROCESAR"+procesar)
    #send_prendas_udp(prenda)
    return Response(modelPrediction(prenda,tipo,marca,procesar), mimetype= "multipart/x-mixed-replace; boundary=frame")


@app.route('/stop_video',methods = ['POST'])
def stop_video():
    global procesarMain
    procesarMain = 0
    #closeSockets()
    #close_unity_socket()
    return "termino todo bien"

@app.route('/unity_image',methods=['GET'])
def render_unity_image():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=="__main__":
    #threadPool = ThreadPoolExecutor(max_workers=2)
    app.run(debug=False)


cv2.destroyAllWindows() 