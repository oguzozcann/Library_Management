import cv2
import sys
import random
import psycopg2
import datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton ,QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream, QTimer
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from sidebar_ui import Ui_MainWindow
from PyQt5 import QtWidgets, uic


from PyQt5 import QtCore
from PyQt5.uic import loadUi
from detection import TehseenCode
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog


from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QThread, pyqtSlot
from sidebar_ui import Ui_MainWindow 




verit=psycopg2.connect("dbname=Kutuphane_Yonetim_Sistemi user=postgres password=11223344Aa.")
cur=verit.cursor()


 #Video Kaydi Uzerinden Yapilan Kod Blogu 
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)

        weights_path = "yolov4-tiny-custom.weights"
        config_path = "yolov4-tiny-custom.cfg"
        class_names_path = "coco.names"

        #thread
        self.tehseen_thread = TehseenCode()
        self.tehseen_thread.setModelParameters(weights_path, config_path, class_names_path)
        self.tehseen_thread.frameCaptured.connect(self.displayImage)
        self.ui.SHOW.clicked.connect(self.startTehseenThread)
        self.ui.CAPTURE.clicked.connect(self.captureImage)

    @pyqtSlot()
    def startTehseenThread(self):
        video_path, _ = QFileDialog.getOpenFileName(self, 'Video Dosyasını Seç', '', 'Video Files (*.mp4 *.avi *.mkv)')
        if video_path:
            self.ui.TEXT.setText('Lütfen "Resim Çek" düğmesine basarak görüntü çekmeye başlayın.')

            # Yeni video seçildiğinde mevcut thread'i durdurun
            if self.tehseen_thread.isRunning():
                self.tehseen_thread.terminate()
                self.tehseen_thread.wait()

            weights_path = "yolov4-tiny-custom.weights"
            config_path = "yolov4-tiny-custom.cfg"
            class_names_path = "coco.names"

            self.tehseen_thread = TehseenCode()
            self.tehseen_thread.setModelParameters(weights_path, config_path, class_names_path)
            self.tehseen_thread.setVideoPath(video_path)
            self.tehseen_thread.frameCaptured.connect(self.displayImage)
            self.tehseen_thread.start()




    @pyqtSlot(object)
    def displayImage(self, frame):
        self.ui.TEXT.setText('"Resim Çek" düğmesine tekrar basarak görüntünüzü kaydedebilirsiniz.')
        self.ui.imgLabel.setPixmap(QPixmap.fromImage(self.convertFrameToImage(frame)))
        self.ui.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def captureImage(self):
        self.tehseen_thread.logic = 2

    def convertFrameToImage(self, img):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qformat)
        img = img.rgbSwapped()

        return img 




    ## Function for changing page to user page
    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [2, 3]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    ## functions for changing menu page
    def on_kamera_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def on_kamera_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_masalar_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_masalar_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_rezervasyon_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_rezervasyon_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    
    def on_pushButton_clicked(self):
        no=int(self.ui.lineEdit.text())
        yer=str(self.ui.lineEdit_2.text())
        tar=datetime.datetime.strptime(self.ui.lineEdit_3.text(),'%d-%m-%Y').date()
        bas=datetime.datetime.strptime(self.ui.lineEdit_4.text(),'%H:%M').time()
        son=datetime.datetime.strptime(self.ui.lineEdit_5.text(),'%H:%M').time()
        merak="INSERT INTO randevu VALUES(%s,%s,%s,%s,%s)"
        cur.execute(merak,(no,yer,tar,bas,son))
        verit.commit()
        
    def on_pushButton_4_clicked(self):
        no=int(self.ui.lineEdit.text())
        yer=str(self.ui.lineEdit_2.text())
        tar=datetime.datetime.strptime(self.ui.lineEdit_3.text(),'%d-%m-%Y').date()
        bas=datetime.datetime.strptime(self.ui.lineEdit_4.text(),'%H:%M').time()
        son=datetime.datetime.strptime(self.ui.lineEdit_5.text(),'%H:%M').time()
        merak="DELETE FROM randevu WHERE ono=%s AND sandalye_id=%s AND tarih=%s AND baslangic=%s AND bitis=%s"
        cur.execute(merak,(no,yer,tar,bas,son))
        verit.commit()
        
    def on_pushButton_2_clicked(self):
        no=int(self.ui.lineEdit.text())
        yer=str(self.ui.lineEdit_2.text())
        tar=datetime.datetime.strptime(self.ui.lineEdit_3.text(),'%d-%m-%Y').date()
        bas=datetime.datetime.strptime(self.ui.lineEdit_4.text(),'%H:%M').time()
        son=datetime.datetime.strptime(self.ui.lineEdit_5.text(),'%H:%M').time()
        merak="UPDATE randevu SET (baslangic=%s,AND bitis=%s) WHERE ono=%s AND sandalye_id=%s AND tarih=%s"
        cur.execute(merak,(bas,son,no,yer,tar))
        verit.commit()
        
    def on_pushButton_3_clicked(self):
        yer=str(self.ui.lineEdit_2.text())
        guvenlik = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))
        merak="UPDATE randevu SET (toplanma_saati=CURRENT_TIME,AND güvenlik_kodu=%s) WHERE sandalye_id=%s AND tarih=CURRENT_DATE AND baslangıc<CURRENT_TIME AND bitis>CURRENT_TIME"
        cur.execute(merak,(guvenlik,yer))
        verit.commit()
        
    def onButtonClicked(self):
        button = self.sender()
        object_name = button.objectName()
        self.ui.lineEdit_2.setText(object_name)
        soru="SELECT * FROM randevu WHERE sandalye_id=%s AND tarih=CURRENT_DATE AND baslangic<CURRENT_TIME AND bitis > CURRENT_TIME"
        cur.execute(soru,(object_name,))
        sonuc=cur.fetchone()
        if(sonuc):
            self.ui.lineEdit.setText(sonuc[0])
            self.ui.lineEdit_3.setText(str(sonuc[2]))
            self.ui.lineEdit_4.setText(str(sonuc[3]))
            self.ui.lineEdit_5.setText(str(sonuc[4]))
   
    def on_kisiselIptal_clicked(self):
        self.ui.kisiselAd.setText("")
        self.ui.kisielSoyad.setText("")
        self.ui.kisielTel.setText("")
        self.ui.kisielMail.setText("")
        self.ui.kisiselNo.setText("")
        self.ui.mevcutSifre.setText("")
        self.ui.yeniSifre.setText("")
        self.ui.yeniSifreTekrar.setText("")
    
    def on_kisiselGuncelle_clicked(self):
        no=self.ui.kisiselNo.text()
        ad= self.ui.kisiselAd.text()
        soyad=self.ui.kisielSoyad.text()
        tel=self.ui.kisielTel.text()
        mail=self.ui.kisielMail.text()
        mevcut=self.ui.mevcutSifre.text()
        yeni=self.ui.yeniSifre.text()
        tekrar=self.ui.yeniSifreTekrar.text()
        if(no!=None):
            if(ad!=None):
                sor="UPDATE eleman SET isim=%s WHERE eleman_id=%s"
                cur.execute(sor,(ad,no))
                verit.commit()
            if(soyad!=None):
                sor="UPDATE eleman SET soyisim=%s WHERE eleman_id=%s"
                cur.execute(sor,(soyad,no))
                verit.commit()
            if(tel!=None):
                sor="UPDATE eleman SET telefon=%s WHERE eleman_id=%s"
                cur.execute(sor,(tel,no))
                verit.commit()
            if(mail!=None):
                sor="UPDATE eleman SET e_posta=%s WHERE eleman_id=%s"
                cur.execute(sor,(ad,no))
                verit.commit()
            if(mevcut!=None and yeni!=None and tekrar!=None and yeni==tekrar):
                sor="UPDATE eleman SET sifre=%s WHERE eleman_id=%s AND sifre=%s"
                cur.execute(sor,(yeni,no,mevcut))
        
    def on_goster_clicked(self):
        tar=datetime.date(self.ui.dateEdit.date().year(),self.ui.dateEdit.date().month(),self.ui.dateEdit.date().day())
        if(tar==None):
            sorgu="SELECT * FROM randevu"
            cur.execute(sorgu)
            tablo=cur.fetchall()
        else:
            sorgu="SELECT * FROM randevu WHERE tarih=%s"
            cur.execute(sorgu,(tar,))
            tablo=cur.fetchall()
        self.ui.tableWidget.setRowCount(0)  # Tabloyu temizle

        for row_index, row_data in enumerate(tablo):
            self.ui.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))
    def on_sifirla_clicked(self):
        sorgu="SELECT * FROM randevu"
        cur.execute(sorgu)
        tablo=cur.fetchall()
        self.ui.tableWidget.setRowCount(0)  # Tabloyu temizle

        for row_index, row_data in enumerate(tablo):
            self.ui.tableWidget.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))
        

if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    # loading style file
    with open("style.qss", "r") as style_file:
        style_str = style_file.read()
    app.setStyleSheet(style_str)

    # loading style file, Example 2
    style_file = QFile("style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())


    window = MainWindow()
    window.show()

    sys.exit(app.exec())














































#Kamera Ile Calisan Kod Blogu 
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()

#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)

#         self.ui.icon_only_widget.hide()
#         self.ui.stackedWidget.setCurrentIndex(0)

#         weights_path = "yolov4-tiny.weights"
#         config_path = "yolov4-tiny-custom.cfg"
#         class_names_path = "coco.names"

#         # Thread
#         self.tehseen_thread = TehseenCode()
#         self.tehseen_thread.setModelParameters(weights_path, config_path, class_names_path)
#         self.tehseen_thread.frameCaptured.connect(self.displayImage)
#         self.ui.SHOW.clicked.connect(self.startTehseenThread)
#         self.ui.CAPTURE.clicked.connect(self.captureImage)

#         self.cap = cv2.VideoCapture(0)  # Kamerayı başlat

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.updateFrame)
#         self.timer.start(30)  # Her 30 milisaniyede bir güncelleme

#     def updateFrame(self):
#         ret, frame = self.cap.read()
#         if ret:
#             self.displayImage(frame)

#     @pyqtSlot()
#     def startTehseenThread(self):
#         # Kameradan görüntü alındığında mevcut thread'i durdurun
#         if self.tehseen_thread.isRunning():
#             self.tehseen_thread.terminate()
#             self.tehseen_thread.wait()

#         self.ui.TEXT.setText('Lütfen "Resim Çek" düğmesine basarak görüntü çekmeye başlayın.')

#         weights_path = "yolov4-tiny-custom.weights"
#         config_path = "yolov4-tiny-custom.cfg"
#         class_names_path = "coco.names"

#         self.tehseen_thread = TehseenCode()
#         self.tehseen_thread.setModelParameters(weights_path, config_path, class_names_path)
#         self.tehseen_thread.setCameraCapture(self.cap)
#         self.tehseen_thread.frameCaptured.connect(self.displayImage)
#         self.tehseen_thread.start()

#     @pyqtSlot(object)
#     def displayImage(self, frame):
#         self.ui.TEXT.setText('"Resim Çek" düğmesine tekrar basarak görüntünüzü kaydedebilirsiniz.')
#         self.ui.imgLabel.setPixmap(QPixmap.fromImage(self.convertFrameToImage(frame)))
#         self.ui.imgLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

#     def captureImage(self):
#         self.tehseen_thread.logic = 2

#     def convertFrameToImage(self, img):
#         qformat = QImage.Format_Indexed8

#         if len(img.shape) == 3:
#             if img.shape[2] == 4:
#                 qformat = QImage.Format_RGBA8888
#             else:
#                 qformat = QImage.Format_RGB888

#         img = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qformat)
#         img = img.rgbSwapped()

#         return img

#         ## Function for changing page to user page
#     def on_user_btn_clicked(self):
#         self.ui.stackedWidget.setCurrentIndex(3)

#     ## Change QPushButton Checkable status when stackedWidget index changed
#     def on_stackedWidget_currentChanged(self, index):
#         btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
#                     + self.ui.full_menu_widget.findChildren(QPushButton)
        
#         for btn in btn_list:
#             if index in [2, 3]:
#                 btn.setAutoExclusive(False)
#                 btn.setChecked(False)
#             else:
#                 btn.setAutoExclusive(True)
            
#     ## functions for changing menu page
#     def on_kamera_btn_1_toggled(self):
#         self.ui.stackedWidget.setCurrentIndex(0)
    
#     def on_kamera_btn_2_toggled(self):
#         self.ui.stackedWidget.setCurrentIndex(0)

#     def on_masalar_btn_1_toggled(self):
#         self.ui.stackedWidget.setCurrentIndex(1)

#     def on_masalar_btn_2_toggled(self):
#         self.ui.stackedWidget.setCurrentIndex(1)

#     def on_rezervasyon_1_toggled(self):
#         self.ui.stackedWidget.setCurrentIndex(2)

#     def on_rezervasyon_2_toggled(self):
#         self.ui.stackedWidget.setCurrentIndex(2)
    
#     def on_pushButton_clicked(self):
#         # no=int(self.ui.lineEdit.text())
#         # yer=str(self.ui.lineEdit_2.text())
#         # tar=datetime.datetime.strptime(self.ui.lineEdit_3.text(),'%d-%m-%Y').date()
#         # bas=datetime.datetime.strptime(self.ui.lineEdit_4.text(),'%H:%M').time()
#         # son=datetime.datetime.strptime(self.ui.lineEdit_5.text(),'%H:%M').time()
#         # merak="INSERT INTO randevu VALUES(%s,%s,%s,%s,%s)"
#         # cur.execute(merak,(no,yer,tar,bas,son))
#         # verit.commit()
#         pass
#     def on_pushButton_4_clicked(self):
#         # no=int(self.ui.lineEdit.text())
#         # yer=str(self.ui.lineEdit_2.text())
#         # tar=datetime.datetime.strptime(self.ui.lineEdit_3.text(),'%d-%m-%Y').date()
#         # bas=datetime.datetime.strptime(self.ui.lineEdit_4.text(),'%H:%M').time()
#         # son=datetime.datetime.strptime(self.ui.lineEdit_5.text(),'%H:%M').time()
#         # merak="DELETE FROM randevu WHERE ono=%s AND sandalye_id=%s AND tarih=%s AND baslangic=%s AND bitis=%s"
#         # cur.execute(merak,(no,yer,tar,bas,son))
#         # verit.commit()
#         pass
#     def on_pushButton_2_clicked(self):
#         # no=int(self.ui.lineEdit.text())
#         # yer=str(self.ui.lineEdit_2.text())
#         # tar=datetime.datetime.strptime(self.ui.lineEdit_3.text(),'%d-%m-%Y').date()
#         # bas=datetime.datetime.strptime(self.ui.lineEdit_4.text(),'%H:%M').time()
#         # son=datetime.datetime.strptime(self.ui.lineEdit_5.text(),'%H:%M').time()
#         # merak="UPDATE randevu SET (baslangic=%s,AND bitis=%s) WHERE ono=%s AND sandalye_id=%s AND tarih=%s"
#         # cur.execute(merak,(bas,son,no,yer,tar))
#         # verit.commit()
#         pass
#     def on_pushButton_3_clicked(self):
#         # yer=str(self.ui.lineEdit_2.text())
#         # guvenlik = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))
#         # merak="UPDATE randevu SET (toplanma_saati=CURRENT_TIME,AND güvenlik_kodu=%s) WHERE sandalye_id=%s AND tarih=CURRENT_DATE AND baslangıc<CURRENT_TIME AND bitis>CURRENT_TIME"
#         # cur.execute(merak,(guvenlik,yer))
#         # verit.commit()
#         pass
#     def onButtonClicked(self):
#         # button = self.sender()
#         # object_name = button.objectName()
#         # self.ui.lineEdit_2.setText(object_name)
#         # soru="SELECT * FROM randevu WHERE sandalye_id=%s AND tarih=CURRENT_DATE AND baslangic<CURRENT_TIME AND bitis > CURRENT_TIME"
#         # cur.execute(soru,(object_name,))
#         # sonuc=cur.fetchone()
#         # if(sonuc):
#         #     self.ui.lineEdit.setText(sonuc[0])
#         #     self.ui.lineEdit_3.setText(str(sonuc[2]))
#         #     self.ui.lineEdit_4.setText(str(sonuc[3]))
#         #     self.ui.lineEdit_5.setText(str(sonuc[4]))
#         pass
   
#     def on_kisiselIptal_clicked(self):
#         # self.ui.kisiselAd.setText("")
#         # self.ui.kisielSoyad.setText("")
#         # self.ui.kisielTel.setText("")
#         # self.ui.kisielMail.setText("")
#         # self.ui.kisiselNo.setText("")
#         # self.ui.mevcutSifre.setText("")
#         # self.ui.yeniSifre.setText("")
#         # self.ui.yeniSifreTekrar.setText("")
#         pass
    
#     def on_kisiselGuncelle_clicked(self):
#         # no=self.ui.kisiselNo.text()
#         # ad= self.ui.kisiselAd.text()
#         # soyad=self.ui.kisielSoyad.text()
#         # tel=self.ui.kisielTel.text()
#         # mail=self.ui.kisielMail.text()
#         # mevcut=self.ui.mevcutSifre.text()
#         # yeni=self.ui.yeniSifre.text()
#         # tekrar=self.ui.yeniSifreTekrar.text()
#         # if(no!=None):
#         #     if(ad!=None):
#         #         sor="UPDATE eleman SET isim=%s WHERE eleman_id=%s"
#         #         cur.execute(sor,(ad,no))
#         #         verit.commit()
#         #     if(soyad!=None):
#         #         sor="UPDATE eleman SET soyisim=%s WHERE eleman_id=%s"
#         #         cur.execute(sor,(soyad,no))
#         #         verit.commit()
#         #     if(tel!=None):
#         #         sor="UPDATE eleman SET telefon=%s WHERE eleman_id=%s"
#         #         cur.execute(sor,(tel,no))
#         #         verit.commit()
#         #     if(mail!=None):
#         #         sor="UPDATE eleman SET e_posta=%s WHERE eleman_id=%s"
#         #         cur.execute(sor,(ad,no))
#         #         verit.commit()
#         #     if(mevcut!=None and yeni!=None and tekrar!=None and yeni==tekrar):
#         #         sor="UPDATE eleman SET sifre=%s WHERE eleman_id=%s AND sifre=%s"
#         #         cur.execute(sor,(yeni,no,mevcut))
#         pass
#     def on_goster_clicked(self):
#     #     tar=datetime.date(self.ui.dateEdit.date().year(),self.ui.dateEdit.date().month(),self.ui.dateEdit.date().day())
#     #     if(tar==None):
#     #         sorgu="SELECT * FROM randevu"
#     #         cur.execute(sorgu)
#     #         tablo=cur.fetchall()
#     #     else:
#     #         sorgu="SELECT * FROM randevu WHERE tarih=%s"
#     #         cur.execute(sorgu,(tar,))
#     #         tablo=cur.fetchall()
#     #     self.ui.tableWidget.setRowCount(0)  # Tabloyu temizle

#     #     for row_index, row_data in enumerate(tablo):
#     #         self.ui.tableWidget.insertRow(row_index)
#     #         for col_index, cell_data in enumerate(row_data):
#     #             self.ui.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))
#     # def on_sifirla_clicked(self):
#     #     sorgu="SELECT * FROM randevu"
#     #     cur.execute(sorgu)
#     #     tablo=cur.fetchall()
#     #     self.ui.tableWidget.setRowCount(0)  # Tabloyu temizle

#     #     for row_index, row_data in enumerate(tablo):
#     #         self.ui.tableWidget.insertRow(row_index)
#     #         for col_index, cell_data in enumerate(row_data):
#     #             self.ui.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))
#         pass

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     ## loading style file
#     # with open("style.qss", "r") as style_file:
#     #     style_str = style_file.read()
#     # app.setStyleSheet(style_str)

#     ## loading style file, Example 2
#     style_file = QFile("style.qss")
#     style_file.open(QFile.ReadOnly | QFile.Text)
#     style_stream = QTextStream(style_file)
#     app.setStyleSheet(style_stream.readAll())


#     window = MainWindow()
#     window.show()

#     sys.exit(app.exec())









































