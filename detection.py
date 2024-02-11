import cv2
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np



# #Video Kaydi Uzerinden Yapilan Kod Blogu 
class TehseenCode(QThread):
    frameCaptured = pyqtSignal(object)

    def __init__(self):
        super(TehseenCode, self).__init__()

        self.logic = 0
        self.value = 1
        self.video_path = ""
        self.weights_path = ""
        self.config_path = ""
        self.class_names_path = ""

    def setModelParameters(self, weights_path, config_path, class_names_path):
        self.weights_path = weights_path
        self.config_path = config_path
        self.class_names_path = class_names_path

    def setVideoPath(self, video_path):
        self.video_path = video_path

    def run(self):
        if not self.video_path or not self.weights_path or not self.config_path or not self.class_names_path:
            print("Gerekli dosya yolları belirtilmedi.")
            return

        # YOLOv4-tiny modelini yükle
        net = cv2.dnn.readNet(self.weights_path, self.config_path)
        with open(self.class_names_path, 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        cap = cv2.VideoCapture(self.video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # YOLOv4-tiny nesne tespiti işlemini gerçekleştir
                blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
                net.setInput(blob)
                layer_names = net.getUnconnectedOutLayersNames()
                detections = net.forward(layer_names)

                # Tespit edilen nesneleri işle ve çerçevele
                for detection in detections:
                    for obj in detection:
                        scores = obj[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]

                        if confidence > 0.7:  # Güvenilirlik eşiği gerektiğine göre ayarlanabilir
                            center_x = int(obj[0] * frame.shape[1])
                            center_y = int(obj[1] * frame.shape[0])
                            width = int(obj[2] * frame.shape[1])
                            height = int(obj[3] * frame.shape[0])


                            x, y = center_x - width // 2, center_y - height // 2

                            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                            cv2.putText(frame, classes[class_id], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                self.frameCaptured.emit(frame)
                cv2.waitKey(48)  # 1 ms bekleyin

                if self.logic == 2:
                    self.value += 1
                    cv2.imwrite(f'C:/Users/oguzo/Desktop/admin_app/image_{self.value}.png', frame)

                    self.logic = 1
            else:
                print("Video frame alınamadı")
                break

        cap.release()
        cv2.destroyAllWindows()






























#Kamera Ile Calisan Kod Blogu 
# class TehseenCode(QThread):
#     frameCaptured = pyqtSignal(object)

#     def __init__(self):
#         super(TehseenCode, self).__init__()

#         self.logic = 0
#         self.value = 1
#         self.cap = None
#         self.weights_path = ""
#         self.config_path = ""
#         self.class_names_path = ""

#     def setModelParameters(self, weights_path, config_path, class_names_path):
#         self.weights_path = weights_path
#         self.config_path = config_path
#         self.class_names_path = class_names_path

#     def setCameraCapture(self, cap):
#         self.cap = cap

#     def run(self):
#         if not self.cap or not self.weights_path or not self.config_path or not self.class_names_path:
#             print("Gerekli dosya yolları veya kamera bilgileri belirtilmedi.")
#             return

#         net = cv2.dnn.readNet(self.weights_path, self.config_path)
#         with open(self.class_names_path, 'r') as f:
#             classes = [line.strip() for line in f.readlines()]

#         while self.cap.isOpened():
#             ret, frame = self.cap.read()
#             if ret:
#                 blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
#                 net.setInput(blob)
#                 layer_names = net.getUnconnectedOutLayersNames()
#                 detections = net.forward(layer_names)

#                 for detection in detections:
#                     for obj in detection:
#                         scores = obj[5:]
#                         class_id = np.argmax(scores)
#                         confidence = scores[class_id]

#                         if confidence > 0.1:
#                             center_x = int(obj[0] * frame.shape[1])
#                             center_y = int(obj[1] * frame.shape[0])
#                             width = int(obj[2] * frame.shape[1])
#                             height = int(obj[3] * frame.shape[0])

#                             x, y = center_x - width // 2, center_y - height // 2

#                             cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
#                             cv2.putText(frame, classes[class_id], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#                 self.frameCaptured.emit(frame)
#                 self.msleep(30)  # PyQt5 QThread'deki bir fonksiyon olan msleep ile bekleyin

#                 if self.logic == 2:
#                     self.value += 1
#                     cv2.imwrite(f'image_{self.value}.png', frame)
#                     self.logic = 1
#             else:
#                 print("Kamera görüntüsü alınamadı")
#                 break

#         self.cap.release()
#         cv2.destroyAllWindows()

