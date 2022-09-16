from flask import Flask, render_template, Response
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, Response

from Threads import ThreadUdpUnity
from tesisLecturaCuerpo import CENTRO, EMOCION, PRENDA, closeSockets, generate_reporting_data

app = Flask(__name__)

rutaHaarcascade = r'C:\\Users\\IVAN\Desktop\Dressy_WebApp\src\\model\\haarcascade_frontalface_default.xml'
rutaClassifier = r'C:\\Users\\IVAN\Desktop\Dressy_WebApp\src\\model\\model_v2.h5'

face_classifier = cv2.CascadeClassifier(rutaHaarcascade)
classifier = tf.keras.models.load_model(rutaClassifier)  # El que entrenamos nosotros en jupyter

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

cap = cv2.VideoCapture(0)


def modelPrediction():
    currentEmotion = ""
    while True:
        _, frame = cap.read()

        # Cambie de lugar Faces para poder mandar por UDP los x,y,w,h de la cara para dibujarlo en Unity.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        thread_udp_sender = ThreadUdpUnity(frame, faces)

        if not thread_udp_sender.is_alive():
            thread_udp_sender.start()
        else:
            thread_udp_sender.run()
            # thread_udp_sender.join()

        for (x, y, w, h) in faces:
            # Dibuja el rectangulo formando los ejes de la cara. Lo mando a Unity para que lo dibuje también.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:

                roi = tf.keras.preprocessing.image.img_to_array(roi_gray)
                roi = np.expand_dims(roi, axis=0)

                prediction = classifier.predict(roi)

                label = emotion_labels[prediction.argmax()]
                # print(emotion_labels[np.argmax(prediction[0])])

                probabilidadPreddicion = str(prediction[0][np.argmax(prediction[0])])

                label_position = (x, y)
                cv2.putText(frame, label + probabilidadPreddicion, label_position,
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if (label != currentEmotion and label != "neutral"):
                    print("XX. Mandando data a api reporting")
                    generate_reporting_data(PRENDA, EMOCION, CENTRO)
                    currentEmotion = label
                else:
                    currentEmotion = label

            else:
                cv2.putText(frame, 'No Faces', (30, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
        # cv2.imshow('Emotion Detector', frame)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(modelPrediction(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)

cap.release()
closeSockets()
cv2.destroyAllWindows()
