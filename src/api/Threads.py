from threading import Thread
from tesisLecturaCuerpo import send_and_process_body_captured_data

class ThreadUdpUnity(Thread):
    '''
    Clase encargada de crear un hilo para enviar la imagen
    capturada por la camara hacia Unity.
    '''

    def __init__(self, image_unity, face_coordinates):
        Thread.__init__(self)
        self.image_unity = image_unity
        self.face_coordinates = face_coordinates

    def run(self):
        send_and_process_body_captured_data(self.image_unity, self.face_coordinates)
