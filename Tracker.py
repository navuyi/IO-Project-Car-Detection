import cv2
import time


def detect(filePath, dirPath, frameOffset):
    CONFIDENCE_THRESHOLD = 0.2
    NMS_THRESHOLD = 0.4
    COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

    class_names = []
    desired_classes = ("car", "bus", "truck", "van", "motorcycle")
    with open("./yolo/yolov3/yolo_classes.txt", "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]

    vc = cv2.VideoCapture("./src/video_input/grupaC1_cut2.mp4")

    net = cv2.dnn.readNet("./yolo/yolov4/yolov4.weights", "./yolo/yolov4/yolov4.cfg")

    # GPU
    # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    # CPU
    # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1 / 255)

    while cv2.waitKey(1) < 1:
        (grabbed, frame) = vc.read()
        if not grabbed:
            exit()

        start = time.time()
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        end = time.time()

        for (classid, score, box) in zip(classes, scores, boxes):
            if class_names[classid[0]] in desired_classes:
                color = COLORS[int(classid) % len(COLORS)]
                label = "%s" % (class_names[classid[0]])
                cv2.rectangle(frame, box, color, 2)
                cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            else:
                pass

        fps_label = "FPS: %.2f" % (1 / (end - start))
        cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("detections", frame)


if __name__ == '__main__':
    detect('', '', 0)
