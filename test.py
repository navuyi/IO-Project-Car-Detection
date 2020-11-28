def processFrame(self):
    blob = cv2.dnn.blobFromImage(frame, 1/255, (self.inpWidth, self.inpHeight), [0,0,0], 1, crop=False)
    outs = self.net.forward(outputlayers)
    class_ids = []
    confidences = []
    boxes = [] # Boxes list is new for every frame processed

    # Process frame:
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)

            # Detect only desired objects
            if(self.classNames[class_id] != ("car" or "bus" or "truck" or "motorcycle" or "van")):
                pass
            else:
                if confidence > self.confThreshold:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x -w/2)
                    y = int(center_y - h/2)

                    boxes.append([x,y,w,h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

                    indexes = cv2.dnn.NMSBoxes(boxes, confidence, self.confThreshold, self.nmsThreshold)
                    for i in range(len(boxes)):
                        if i in indexes:
                            x, y, w, h = boxes[i]
                            label = str(self.classNames[class_ids[i]])
                            color = (0,0,255) # Its red becouse cv2 uses BGR instead of RGB xd
                            cv2.rectangle(frame, (x,y), (x+w, y+h), color, 2)
    
    # Show frame with Bound Boxes
    cv2.imshow("WTV", frame)
    cv2.waitKey(1)