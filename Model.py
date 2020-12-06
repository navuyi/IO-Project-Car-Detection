# Opencv 4.1.2 works with yolov3 and yolov3-tiny
import cv2
import numpy as np
import time

from Settings import *


class Model:
    def __init__(self, filePath, dirPath):
        # self.filePath = filePath  # Set to fixed path for now
        # self.directoryPath = dirPath
        self.filePath = './src/video_input/grupaC1_cut2.mp4'
        self.directoryPath = './results'
        print(filePath)
        print(dirPath)

        self.frameIndex = 0
        # Init parameters
        self.confThreshold = 0.5  # Confidence threshold
        self.nmsThreshold = 0.6  # Non-maximum suppresion threshold
        self.inpWidth = 416  # Width of network's input image
        self.inpHeight = 416  # Height of network's input image

        self.classNamesFilePath = "./yolo/yolov3/yolo_classes.txt"
        self.classNames = None
        with open(self.classNamesFilePath, 'rt') as f:
            self.classNames = f.read().strip('\n').split('\n')

        # Load weights and config file
        #self.model_cfg = "./yolo/yolov4/yolov4.cfg"
        #self.model_weights = "./yolo/yolov4/yolov4.weights"
        self.model_cfg = "./yolo/yolov3/yolov3_v416.cfg"
        self.model_weights = "./yolo/yolov3/yolov3_v416.weights"

        self.net = cv2.dnn.readNetFromDarknet(self.model_cfg, self.model_weights)

        # CPU
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # GPU

        #self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        #self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.classes = ("car", "bus", "truck", "van", "motorcycle")
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # Load input video
        self.video = cv2.VideoCapture(self.filePath)
        self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
        frame_width = int(self.video.get(3))
        frame_height = int(self.video.get(4))
        self.size = (frame_width, frame_height)
        self.result = cv2.VideoWriter(str(self.directoryPath) + '/result.avi', cv2.VideoWriter_fourcc(*'MJPG'),
                                      self.fps / FRAME_OFFSET, self.size)
        self.boxes = []
        self.confidences = []

        # creating file to write
        self.result_file = open(str(self.directoryPath) + '/result.txt', 'w')
        self.result_lines = []
        self.frame_counter = 0

    def detect(self):
        while True:
            ok, frame = self.video.read()
            if self.frameIndex == 0:
                height, width, channels = frame.shape
            self.frameIndex += 1
            self.frame_counter += 1
            # Finish detection if error occured or process is done
            if not ok:
                print('Frame reading error or finished')
                self.video.release()
                self.result.release()
                cv2.destroyAllWindows()
                self.result_file.writelines(self.result_lines)
                self.result_file.close()
                break
            if self.frameIndex % FRAME_OFFSET == 0:
                if self.frame_counter % self.fps == 0:
                    print(self.frame_counter)
                    self.processFrame(frame, width, height, True)
                    self.detectionInfo()
                    self.result.write(frame)
                else:
                    self.processFrame(frame, width, height)
                    self.detectionInfo()
                    self.result.write(frame)
            else:
                # self.showFrame(frame)
                self.detectionInfo()

    def processFrame(self, frame, width, height, log=False):
        t1 = time.time()
        fps_count = 0.0
        # Create blob from frame
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (self.inpWidth, self.inpHeight), [0, 0, 0], swapRB=True,
                                     crop=False)
        # Set input to neural network
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        self.class_ids = []
        self.confidences = []
        self.boxes = []  # Boxes list is new for every frame processed
        label_count = []

        # Process frame:
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # Detect only desired objects
                if self.classNames[int(class_id)] in self.classes:
                    if confidence > self.confThreshold:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        self.boxes.append([x, y, w, h])
                        self.confidences.append(float(confidence))
                        self.class_ids.append(class_id)

                        indexes = cv2.dnn.NMSBoxes(self.boxes, self.confidences, self.confThreshold, self.nmsThreshold,
                                                   5)

                        for i in range(len(self.boxes)):
                            if i in indexes:
                                x, y, w, h = self.boxes[i]
                                label = str(self.classNames[int(self.class_ids[i])])
                                color = (0, 0, 255)  # Its red because cv2 uses BGR instead of RGB xd
                                label_count.append(label)
                                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                else:
                    pass
        if log:
            duration = self.frame_counter / self.fps
            minutes = int(duration / 60)
            seconds = duration % 60
            self.result_lines.append(str(minutes) + ':' + str("{:.0f}".format(seconds)) + '; ')
            for label in self.classes:
                detected_objects = label_count.count(label)
                if detected_objects != 0:
                    self.result_lines.append(str(label) + ': ' + str(detected_objects) + '\t')
            self.result_lines.append("\n")
        fps_count = (fps_count + (1. / (time.time() - t1))) / 2 * FRAME_OFFSET
        cv2.putText(frame, "FPS: {:.2f}".format(fps_count), (0, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        cv2.imshow("WTV", frame)
        cv2.waitKey(1)

    def showFrame(self, frame):
        indexes = cv2.dnn.NMSBoxes(self.boxes, self.confidences, self.confThreshold, self.nmsThreshold)
        for i in range(len(self.boxes)):
            if i in indexes:
                x, y, w, h = self.boxes[i]
                label = str(self.classNames[int(self.class_ids[i])])
                color = (0, 0, 255)  # Its red because cv2 uses BGR instead of RGB xd
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        cv2.imshow("WTV", frame)
        cv2.waitKey(1)

    def detectionInfo(self):

        print(self.frameIndex)


if __name__ == '__main__':
    time1 = time.time()
    model = Model('', '')
    model.detect()
    time2 = time.time()
    print("Seconds since epoch =", time2 - time1)
