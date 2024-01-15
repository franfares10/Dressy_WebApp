import json
from concurrent.futures import ThreadPoolExecutor
from urllib import request
import threading
import numpy as np
import tensorflow as tf
import requests 
from tkinter.tix import Tree
import cv2
from flask import Flask,Response,request
from tesisLecturaCuerpo import send_and_process_body_captured_data,send_prendas_udp
from ImagenUnity import generate_frames

app=Flask(__name__)
lock = threading.Lock()
FRAN_URL = 'E:\\Escritorio\\' #URL para clasificadores y modelo.
IVAN_URL = 'D:\\DressyFrontend\\' #URL para clasificadores y modelo.
FACE_CLASSIFIER = cv2.CascadeClassifier(r'D:\\DressyFrontend\\Dressy_WebApp\\flask-api\\model\\haarcascade_frontalface_default.xml')
CLASSIFIER = tf.keras.models.load_model(r'D:\\DressyFrontend\\Dressy_WebApp\\flask-api\\model\\model_v7.h5')
HISTORICO_URL = "https://dressy-reporting-service.herokuapp.com/api/emociones/historico/"
EMOTION_LABELS = ['disgust', 'happy', 'neutral','sad','surprise']
CENTRO = "630eba5d10522cae4a888755"
PROCESAR_MAIN = 0
LEGAL_STATE = False
GENDER_STATE = "genero"

def create(prenda,emocion,centro,genero):
    """
    Creates a new entry in the historical records.

    :param prenda: The type of clothing for the entry.
    :type prenda: str

    :param emocion: The emotion associated with the entry.
    :type emocion: str

    :param centro: The location or context of the entry.
    :type centro: str

    :param genero: The gender associated with the entry.
    :type genero: str

    :return: None
    """
    payload = json.dumps({
                        "prenda": prenda,
                        "emocion": emocion,
                        "centro": centro,
                        "genero":genero
                        })
    headers =  {
                'Content-Type': 'application/json'
                }

    requests.request("POST", HISTORICO_URL, headers=headers, data=payload)

def model_prediction(prenda,marca):
    '''
        Método que captura la imagen de la camara,
        carga el modelo de microexpresionesenvia datos hacia Unity 
        y servicio de reporting
    '''
    if PROCESAR_MAIN:
        cap=cv2.VideoCapture(0)
        current_emotion = ""
        if cap.isOpened():
            rval, frame = cap.read()
        else:
            rval = False
        while rval and PROCESAR_MAIN:
            with lock:
                _, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = FACE_CLASSIFIER.detectMultiScale(gray, minNeighbors=10)
                threadPool.submit(send_and_process_body_captured_data,frame,faces,marca)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
                    roi_gray = gray[y:y+h, x:x+w]
                    #Resize de imagen capturada para que el modelo la reconozca
                    roi_gray = cv2.resize(roi_gray, (48, 48),interpolation=cv2.INTER_AREA)
                    if np.sum([roi_gray]) != 0:
                        roi = tf.keras.preprocessing.image.img_to_array(roi_gray)
                        roi = np.expand_dims(roi, axis=0)
                        prediction = CLASSIFIER.predict(roi)

                        label = EMOTION_LABELS[prediction.argmax()]

                        prediction_probability = str(prediction[0][np.argmax(prediction[0])])

                        label_position = (x, y)
                        cv2.putText(frame, label+prediction_probability, label_position,
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        if( current_emotion!="" and label!=current_emotion and label!="neutral"):
                            if LEGAL_STATE=="True":
                                thread = threading.Thread(target=create,args=(prenda,label,CENTRO,GENDER_STATE))
                                thread.start()
                            current_emotion = label
                        else:
                            current_emotion = label
                    (encoded_image) = cv2.imencode(".jpg",frame)
                    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ bytearray(encoded_image) + b'\r\n')
                cv2.imshow('Emotion Detector', frame)
                if not PROCESAR_MAIN:
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
    """
    Endpoint for streaming video feed with optional processing parameters.

    This function retrieves clothing and brand information from the request parameters,
    sets a global processing flag, sends clothing information to Unity, and returns a
    streaming response based on model predictions.

    :return: Response containing the video stream with model predictions.
    :rtype: flask.Response
    """
    prenda = request.args.get('prenda')
    marca = request.args.get('marca')
    procesar = request.args.get('procesar')
    global PROCESAR_MAIN
    PROCESAR_MAIN = procesar
    send_prendas_udp(marca) #Enviamos la ropa elegida del usuario hacia Unity.
    return Response(model_prediction(prenda,marca), mimetype= "multipart/x-mixed-replace; boundary=frame")


@app.route('/stop_video',methods = ['POST'])
def stop_video():
    """
    Stops the video processing.

    This function sets a global flag (`PROCESAR_MAIN`) to 0, indicating that
    video processing should be stopped.

    :return: A message indicating successful termination.
    :rtype: void
    """
    global PROCESAR_MAIN
    PROCESAR_MAIN = 0

@app.route('/unity_image',methods=['GET'])
def render_unity_image():
    """
    Renders Unity images as a streaming response.

    This function returns a streaming response containing Unity images
    generated by the `generate_frames` function.

    :return: Streaming response for Unity images.
    :rtype: flask.Response
    """
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/termsAndConditions',methods=['POST'])
def set_terms_and_conditions():
    """
    Sets the terms and conditions for the user.

    This function receives the legal state and gender information from the user
    through the request parameters. It updates global variables `LEGAL_STATE` and
    `GENDER_STATE` accordingly and prints the updated values.

    :return: A message indicating successful update.
    :rtype: void
    """
    global LEGAL_STATE
    LEGAL_STATE = request.args.get('terms')
    global GENDER_STATE
    GENDER_STATE = request.args.get('gender')

if __name__=="__main__":
    threadPool = ThreadPoolExecutor(max_workers=2)
    app.run(debug=False)

cv2.destroyAllWindows()
