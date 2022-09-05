from flask import Flask,render_template,Response
import cv2
import os
from sys import maxsize
#from keras.models import load_model
from time import sleep, time
import numpy as np
import tensorflow as tf
import requests
import json

app=Flask(__name__)

face_classifier = cv2.CascadeClassifier(r'E:\\Escritorio\\Dressy_WebApp\\src\\model\\haarcascade_frontalface_default.xml')
classifier = tf.keras.models.load_model(r'E:\\Escritorio\\Dressy_WebApp\\src\\model\\model_v2.h5') #El que entrenamos nosotros en jupyter
HISTORICO_URL = "https://dressy-reporting-service.herokuapp.com/api/emociones/historico/"
emotion_labels = ['Angry', 'Disgust', 'Fear','Happy', 'Neutral', 'Sad', 'Surprise']

cap=cv2.VideoCapture(0)

def modelPrediction():
    currentEmotion = ""
    while True:
        _, frame = cap.read()
        labels = []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

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
                    #aca escribo en el archivo
                    print("CAMBIE DE EMOCION")
                    payload = json.dumps({
                        "prenda": "630f55248ac2207315ff8b0f",
                        "emocion": "630ea9efb0c20d906714b1c0",
                        "centro": "630eba5d10522cae4a888755",
                        "fecha": "05/09/2022"
                        })
                    headers = {
                        'Content-Type': 'application/json'
                        }

                    response = requests.request("POST", HISTORICO_URL, headers=headers, data=payload)

                    print(response.text)
                    currentEmotion = label
                else:
                    currentEmotion = label

            else:
                cv2.putText(frame, 'No Faces', (30, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            (flag, encodedImage) = cv2.imencode(".jpg",frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ bytearray(encodedImage) + b'\r\n')
        cv2.imshow('Emotion Detector', frame)
        


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(modelPrediction(), mimetype= "multipart/x-mixed-replace; boundary=frame")


if __name__=="__main__":
    app.run(debug=True)

cap.release()
cv2.destroyAllWindows()