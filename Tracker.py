import cv2
import time


def detect_and_save(file_path, dir_path, frame_offset, on_the_fly=False):
    CONFIDENCE_THRESHOLD = 0.2
    NMS_THRESHOLD = 0.4
    COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
    desired_classes = ("car", "bus", "truck", "van", "motorcycle")
    with open("./yolo/yolov3/yolo_classes.txt", "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]

    # loading video
    vc = cv2.VideoCapture(str(file_path))
    # parameters for result video
    fps = int(vc.get(cv2.CAP_PROP_FPS))
    frame_count = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(vc.get(3))
    frame_height = int(vc.get(4))
    size = (frame_width, frame_height)
    file_id = str(hash(int(time.time())))

    # Creating video file to write | Path to file is the first argument
    result_video = cv2.VideoWriter(str(dir_path) + '/video' + file_id + '.avi', cv2.VideoWriter_fourcc(*'MJPG'),
                                   fps / frame_offset, size)

    # Creating .txt file to write
    result_file = open(str(dir_path) + '/video_log' + file_id + '.txt', 'w')

    # Loading neural network
    net = cv2.dnn.readNet("./yolo/yolov4/yolov4.weights", "./yolo/yolov4/yolov4.cfg")

    # GPU computing
    # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    # CPU computing
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(320, 320), scale=1 / 255)

    frame_counter = 0

    while cv2.waitKey(1) < 1:
        (grabbed, frame) = vc.read()
        if not grabbed:
            # Detection is finished, last frame has been proccessed
            vc.release()
            result_video.release()
            cv2.destroyAllWindows()
            result_file.close()
            return

        if frame_counter % frame_offset == 0:
            print("{0:.2f}%".format(frame_counter/frame_count*100))
            # Yield progress and output file
            yield frame_counter/frame_count*100, str(dir_path) + '\/'+'video' + file_id + '.avi'
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
            if frame_counter != 0 and frame_counter % 8 == 0:
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
            result_video.write(frame)
            if on_the_fly:
                fps_label = "FPS: %.2f" % (1 / (end - start) * frame_offset)
                cv2.putText(frame, fps_label, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv2.imshow("Detections", frame)
        else:
            pass
        frame_counter += 1
