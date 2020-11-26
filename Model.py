import cv2
import time
import numpy as np
class Model:
    def __init__(self, filePath, dirPath):
        self.filePath = "./src/video_input/GrupaC1.avi" # Set to fixed path for now
        self.directoryPath = dirPath
        print(filePath)
        print(dirPath)

        self.frameIndex = 0;
        # Init parameters
        self.confThreshold = 0.5    # Confidence threshold
        self.nmsThreshold = 0.4     # Non-maximum suppresion threshold
        self.inpWidth = 416         # Width of networ's input image
        self.inpHeight = 416        # Height of networ's input image   

        self.classNamesFilePath = "./src/yolov3/yolov3_classes.txt";
        self.classNames = None;
        with open(self.classNamesFilePath, 'rt') as f:
            self.classNames = f.read().strip('\n').split('\n')

        # Load weights and config file
        self.model_cfg = "./src/yolov3/yolov3.cfg"
        self.model_weights = "./src/yolov3/yolov3.weights"

        self.net = cv2.dnn.readNetFromDarknet(self.model_cfg, self.model_weights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # Load input video
        self.video = cv2.VideoCapture(self.filePath)

        # Video writer initialization (to save output video)
        #self.video_writer = cv2.VideoWriter(outputVideo, cv2.VideoWriter_fourcc('M','J','P','G'), 30, (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))



    


    def detect(self):
        layer_names = self.net.getLayerNames()
        outputlayers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        while True:
            ok, frame = self.video.read();
            if self.frameIndex == 0:
                height, width, channels = frame.shape
            # Finish detection if error occured or process is done
            if not ok:
                print('Frame reading error or finished')
                break;
            
            # Create blob from frame
            blob = cv2.dnn.blobFromImage(frame, 1/255, (self.inpWidth, self.inpHeight), [0,0,0], 1, crop=False)
            
            # Set input to the network
            self.net.setInput(blob)

            # Forward informations to outs variable
            outs = self.net.forward(outputlayers)
            class_ids=[]
            confidences=[]
            boxes=[]
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > self.confThreshold:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x -w/2)
                        y = int(center_y - h/2)


                        if(self.classNames[class_id] == "car"):
                            boxes.append([x,y,w,h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)

                            indexes = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
                            for i in range(len(boxes)):
                                if i in indexes:
                                    x,y,w,h = boxes[i]
                                    label = str(self.classNames[class_ids[i]])
                                    color = (0,0,255)
                                    cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
                                


            # Show frame with BBxs         
            cv2.imshow("Result", frame)
            cv2.waitKey(1)

            self.detectionInfo()
            


    

    




    def detectionInfo(self):
        self.frameIndex += 1
        print(self.frameIndex)

    


    '''
    def calculateCvlib(self):
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



    def calculateXML(self):
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
    '''


