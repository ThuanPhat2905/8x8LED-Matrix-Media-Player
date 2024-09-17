

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PIL import Image, ImageOps
import numpy as np
import serial
import sys
import serial.tools.list_ports
import cv2 as cv
import time

global ser, flag, close_app, flag2
flag = 1
flag2 = 0
close_app = 1
def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("giaodien.ui", self)
        self.button = self.findChild(QPushButton, "pushButton")
        self.label = self.findChild(QLabel, "label" )
        self.label_image = self.findChild(QLabel, "label_2" )
        self.combobox = self.findChild(QComboBox, "comboBox")
        self.update_COM = self.findChild(QPushButton, "pushButton_2")
        self.checkbox = self.findChild(QCheckBox, "checkBox")
        self.btn_send = self.findChild(QPushButton, "pushButton_3")
        self.opacity = self.findChild(QScrollBar,"horizontalScrollBar")
        self.opacity_value = self.findChild(QLabel, "label_4" )
        self.speed_value = self.findChild(QLabel, "label_6" )
        self.speed = self.findChild(QSlider,"horizontalSlider")
        
        self.speed.valueChanged.connect(self.set_speed)
        self.opacity.valueChanged.connect(self.set_opacity)
        self.btn_send.clicked.connect(self.ser_send)
        self.button.clicked.connect(self.open_file)
        self.update_COM.clicked.connect(self.load_COM)
        self.show()
        self.load_COM()

    def set_speed(self):
        self.speed_value.setText(str(self.speed.value()))    

    def set_opacity(self):
        self.opacity_value.setText(str(self.opacity.value()))

    def load_COM(self):
        i = 0
        ports = list(serial.tools.list_ports.comports())
        self.combobox.clear()
        for p in ports:
            self.combobox.addItem("")
            self.combobox.setItemText(i, str(p))
            i +=1

    def ser_send(self):
        try:
            global flag2
            if(op[0:6]=="Images"):
                self.send_image(fname,1)    #cai 1 de nhan biet la gui serial 
                flag2 = 0
            else:
                if(fname[-3:]=="gif"):
                    while(flag):
                        flag2 = 1
                        self.open_video(fname,1)   
                        flag2 = 0
                else:
                    flag2 = 1
                    self.open_video(fname,1)   
                    flag2 = 0
        except:
            pass
    
    def open_file(self):
        global fname, op, flag, flag2
        
        flag = 0
        fname, op = QFileDialog.getOpenFileName(self, "Open File","","Images (*.png *.xpm *.jpg *.jpeg *.webp *.jpe *.jxr *.bmp *.tif *.tiff);;Videos(*.mp4 *.MOV *.gif *.avi *mkv *.vob)")
        if(op[0:6]=="Images"):
            self.send_image(fname,0)    # 0 de nhan biet la hien thi len giao dien
            flag2 = 0
        else:
            if(fname[-3:]=="gif"):
                flag = 1
                while(flag):
                    flag2 = 1
                    self.open_video(fname,0)
                    flag2 = 0   
            else:
                flag2 = 1
                self.open_video(fname,0)
                flag2 = 0     
    def open_video(self,fname,send):        
        cap = cv.VideoCapture(fname)
        while cap.isOpened():
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            if(cap.get(1)):              
                if(flag2 == 0):
                    break
                if(cap.get(cv.CAP_PROP_POS_FRAMES)%self.speed.value() == 0):
                    cv.imwrite("frame.jpg", frame) 
                    name = "frame.jpg"
                    self.send_image(name,send)
            if cv.waitKey(1) == ord('q'):
                break
        cap.release()
    def send_image(self,name,send):
        global ser
        
        self.label.setStyleSheet("image: url(" + name +");")
        if(send):
            try:
                ser = serial.Serial(self.combobox.currentText()[0:5],9600)
            except:
                pass
            with Image.open(name) as img:
                #print(img)
                c = ImageOps.pad(img, [8,8])
                bitmap = c.convert('L')
                #print(bitmap)
                n = ""
                data = np.array(bitmap,dtype=int).T
                #print(data)
                #bitmap.show()
                """
                      for i in data:
                    for j in i:
                        if(self.checkbox.checkState()):
                            n+=str((int(not(j))))
                        else:
                            n+=str((int((j))))
                """
                for i in data:
                    for j in i: 
                        if(j<self.opacity.value()):
                            if(self.checkbox.checkState()): 
                                n+="1"
                            else:
                                n+="0"
                        else:
                            if(self.checkbox.checkState()): 
                                n+="0"
                            else:
                                n+="1"

                bytes2send = bitstring_to_bytes(n)
                print(bytes2send)
                try:
                    ser.write(bytes2send)   
                    time.sleep(0.005)
                    ser.close()
                except:
                    print("fail")
                    pass

    def closeEvent(self, event):
        global flag, flag2
        reply = QMessageBox.question(self, 'Xác nhận',
            'Bạn có chắc muốn thoát ứng dụng?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            flag = flag2 = 0
            event.accept()
        else:
            event.ignore()
    
app =QApplication(sys.argv)
UIWindow = UI()
app.exec_()


