import cv2
import cvlib
from cvlib.object_detection import draw_bbox
import time
class Model:
    def __init__(self, filePath, dirPath):
        self.filePath = filePath
        self.directoryPath = dirPath
        print(filePath)
        print(dirPath)

        self.licznik = 0;




    def calculate(self):
        video = cv2.VideoCapture('src/GrupaC1.avi')
        start = time.time()
        while True:
            (successful_read, frame) = video.read()
            if successful_read:
                grayscaled_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.licznik += 1
            else:
                break

            (bbox, label, conf) = cvlib.detect_common_objects(frame)
            print(self.licznik)
            output_frame = draw_bbox(frame, bbox, label, conf)
            cv2.imshow("Result", output_frame)

            cv2.waitKey(1)

        end = time.time()
        print(end - start)



    def calculate2(self):
        car_tracker = cv2.CascadeClassifier('src/cars.xml')
        video = cv2.VideoCapture('src/GrupaC1.avi')

        while True:
            read_successful, frame = video.read()

            if read_successful:
                grayscaled_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                break

            # Detect cars
            cars = car_tracker.detectMultiScale(grayscaled_frame, 1.2, 1)

            for (x,y,w,h) in cars:
                cv2.rectangle(grayscaled_frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            cv2.imshow("Bla bla", grayscaled_frame)
            cv2.waitKey(1)



