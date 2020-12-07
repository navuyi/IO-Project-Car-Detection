import cv2
import time


def detect(file_path, dir_path, frame_offset):
    CONFIDENCE_THRESHOLD = 0.2
    NMS_THRESHOLD = 0.4
    COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
    dirPath = './results'
    class_names = []
    desired_classes = ("car", "bus", "truck", "van", "motorcycle")
    with open("./yolo/yolov3/yolo_classes.txt", "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]

    # loading video
    vc = cv2.VideoCapture("./src/video_input/grupaC1_cut2.mp4")
    # parameters for result video
    fps = int(vc.get(cv2.CAP_PROP_FPS))
    frame_width = int(vc.get(3))
    frame_height = int(vc.get(4))
    size = (frame_width, frame_height)

    result_video = cv2.VideoWriter(str(dirPath) + '/result.avi', cv2.VideoWriter_fourcc(*'MJPG'),
                                   fps / frame_offset, size)

    # creating file to write
    result_file = open(str(dirPath) + '/result.txt', 'w')

    # loading neural network
    net = cv2.dnn.readNet("./yolo/yolov4/yolov4.weights", "./yolo/yolov4/yolov4.cfg")

    # GPU computing
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    # CPU computing
    # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(320, 320), scale=1 / 255)

    frame_counter = 0

    while cv2.waitKey(1) < 1:
        (grabbed, frame) = vc.read()
        if not grabbed:
            exit()

        frame_counter += 1
        start = time.time()
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        end = time.time()
        label_count = []

        for (classid, score, box) in zip(classes, scores, boxes):
            if class_names[classid[0]] in desired_classes:
                color = COLORS[int(classid) % len(COLORS)]
                label = "%s" % (class_names[classid[0]])
                label_count.append(label)
                cv2.rectangle(frame, box, color, 2)
                cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        if frame_counter % 8 == 0:
            result_lines = []
            duration = frame_counter / fps
            minutes = int(duration / 60)
            seconds = duration % 60
            result_lines.append(str(minutes) + ':' + str("{:.0f}".format(seconds)) + '; ')
            for label in desired_classes:
                detected_objects = label_count.count(label)
                if detected_objects != 0:
                    result_lines.append(str(label) + ': ' + str(detected_objects) + '\t')
            result_lines.append("\n")
            result_file.writelines(result_lines)
        else:
            pass

        fps_label = "FPS: %.2f" % (1 / (end - start))
        cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("detections", frame)
        result_video.write(frame)


if __name__ == '__main__':
    detect('', '', 1)
