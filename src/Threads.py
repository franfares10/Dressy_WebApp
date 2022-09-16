from threading import Thread
from time import sleep

from tesisLecturaCuerpo import generate_reporting_data, send_and_process_body_captured_data


class ThreadUdpUnity(Thread):

    def __init__(self, imageUnity, facesCoordinates):
        Thread.__init__(self)
        self.imageUnity = imageUnity
        self.facesCoordinates = facesCoordinates

    # El start de esta clase, llama internamente al run.
    def run(self):
        send_and_process_body_captured_data(self.imageUnity, self.facesCoordinates)

class ThreadReportingData(Thread): ##Quedo deprecado, revisar si quedó por algun lado pero no deberia
    def __init__(self, prenda, centro, emocion):
        Thread.__init__(self)
        self.prenda = prenda
        self.centro = centro
        self.emocion = emocion

    def run(self):
        try:
            generate_reporting_data(self.prenda, self.emocion, self.centro)
        except Exception as e:
            print("Error: ", e)
