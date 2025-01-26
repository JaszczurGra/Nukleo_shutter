import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QLineEdit, QHBoxLayout, QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QPolygon, QRegion, QPen
from PyQt5.QtGui import QTextCursor, QTextBlockFormat,QPixmap
import math

import socket 

# TODO ip address of the Nucleo board
TCP_IP = '192.168.0.1'
TCP_PORT = 55151
BUFFER_SIZE = 1024


# DO NOT CHANGE ONLY FOR QUALIFIED PERSONEL 
funny = False


class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.connected = False
        self.setGeometry(100, 100, 500, 500)
        self.setFixedSize(850, 500)
        self.setStyleSheet('background-color: grey')

        layout = QHBoxLayout()


        

        left = QVBoxLayout()


        conection_layout = QHBoxLayout()

        r = QWidget()
        r.setFixedWidth(80) 
        conection_layout.addWidget(r)   

        circle_layout = QVBoxLayout()
        circle_layout.addStretch()  
        circle_widget = QWidget(self)
        self.circle = circle_widget
        circle_widget.setFixedSize(40, 40)
        circle_widget.setStyleSheet('background-color: red; border-radius: 20px;')
        circle_layout.addWidget(circle_widget, alignment=Qt.AlignCenter)
        circle_layout.addStretch()  
        conection_layout.addLayout(circle_layout)

        connected = QLineEdit('Disconnected', self)
        connected.setReadOnly(True)
        connected.setAlignment(Qt.AlignLeft)
        connected.setStyleSheet('background-color: transparent ; color: red;border: none;font-size: 40px;')
        connected.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        connected.setFixedHeight(80)
        conection_layout.addWidget(connected)
        left.addLayout(conection_layout)

        self.shutter = ShutterWidget(self)
        left.addWidget(self.shutter)
        
        layout.addLayout(left)

        mid = QWidget() 
        mid.setFixedWidth(40)
        layout.addWidget(mid)

        right = QVBoxLayout()

        upper = QWidget()
        upper.setFixedHeight(30)
        right.addWidget(upper)

        self.infil = QTextEdit('', self)
        self.infil.setReadOnly(True)
        self.infil.setStyleSheet('background-color: grey ; color: black;border: none;font-size: 45px;')
        self.infil.setFixedHeight(130)
        right.addWidget(self.infil)


        self.slider = QSlider(self, orientation=1, maximum=100, minimum=0)
        self.slider.valueChanged.connect(self.change_value)
        self.change_value()
        self.slider.setEnabled(False) 
        self.slider.setFixedHeight(30)
        right.addWidget(self.slider)

        self.slider.setValue(50)


        upper = QWidget()
        upper.setFixedHeight(30)
        right.addWidget(upper)

        button = QPushButton('Connect', self)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setStyleSheet('background-color: lightgrey;font-size: 40px;')
        button.clicked.connect(lambda: self.changeConnection(connected,button))
        right.addWidget(button)

        layout.addLayout(right)


        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: #eee;
                height: 10px;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #66ccff;
                border: 1px solid #777;
                height: 10px;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: #fff;
                border: 1px solid #777;
                height: 10px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #66ccff;
                border: 1px solid #777;
                width: 20px;
                margin-top: -5px;
                margin-bottom: -5px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal:hover {
                background: #55aaff;
                border: 1px solid #555;
            }
            QSlider::sub-page:horizontal:disabled {
                background: #bbb;
                border-color: #999;
            }
            QSlider::add-page:horizontal:disabled {
                background: #eee;
                border-color: #999;
            }
            QSlider::handle:horizontal:disabled {
                background: #ddd;
                border: 1px solid #aaa;
            }
        """)


        # MESSAGE = b"X"

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
        # data = s.recv(BUFFER_SIZE)
    





        self.setLayout(layout)
        # TODO NEVER CHANGE THIS LINE
        self.setWindowTitle('Sexo 69 -> Jacob' if funny else 'Shutter Control') 
        self.show()

    def changeConnection(self,var,button):
        if self.connected:
            self.disconnect(var,button)
        else:
            self.connect(var,button)

    def connect(self,var,button):
        # TODO Implement the connect function
        print('Connecting to the device')


        try:
            self.socket.connect((TCP_IP, TCP_PORT))
            print("Connected successfully")
            value = int(self.socket.recv(BUFFER_SIZE))
            # value = 50
            print(f"Received data: {value}")
            self.slider.setValue(value)
        except socket.error as e:
            print(f"Failed to connect: {e}")
            return




        var.setText('Connected')
        button.setText('Disconnect')
        var.setStyleSheet('background-color: transparent ; color: green;border: none;font-size: 40px;')
        self.circle.setStyleSheet('background-color: green; border-radius: 20px;')
        self.slider.setEnabled(True) 
        self.connected = True




    def disconnect(self,var,button):
        # TODO Implement the disconnect function
        print('Disconnecting from the device')

        self.socket.close() 

        var.setText('Disconnected')
        button.setText('Connect')
        var.setStyleSheet('background-color: transparent ; color: red;border: none;font-size: 40px;')
        self.circle.setStyleSheet('background-color: red; border-radius: 20px;')
        self.slider.setEnabled(False) 
        self.connected = False



    def change_value(self):

        value = self.slider.value()
        self.infil.setHtml(f'<div style="text-align: center;">Current Value:<br>{str(value)}%</div>')
        self.shutter.set_value(value)
        if self.connected:
            print(f"Sending data: {value}")
            self.socket.send(bytes(str(value), 'utf-8'))


class ShutterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.setFixedHeight(400)
        self.setFixedWidth(400)


    def set_value(self, value):
        self.value = value * 1.5
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)


        width = self.width()
        height = self.height()
        center = QPoint(width // 2, height // 2)
        max_radius = min(width, height) // 2
        radius = max_radius * (self.value / 100) / 0.9
       
       
        max_radius = int (max_radius * 0.8)

        steps = 8

        if funny:
            painter.setBrush(QBrush(QColor('transarent')))
        else:
            painter.setBrush(QBrush(QColor('lightblue')))

        painter.setPen(QPen(QColor('gray'), 15))
        painter.drawEllipse(QRect(center.x() - max_radius, center.y() - max_radius, 2 * max_radius, 2 * max_radius))

        # Draw the circular mask
        circle_region = QRegion(center.x() - max_radius, center.y() - max_radius, 2 * max_radius, 2 * max_radius, QRegion.Ellipse)
        painter.setClipRegion(circle_region)
        
        if funny:
            background_image = QPixmap('rico.jpg')
            painter.drawPixmap(self.rect(), background_image)


        painter.setBrush(QBrush(QColor('gray')))


        points = [[0,0],[0.5,0],[1,0],[1,0.5],[1,1],[0.5,1],[0,1],[0,0.5]]

        painter.setPen(QColor('black'))
        angle_step = 360 // steps
        for i in range(steps):
            angle = angle_step * i
            point1 = QPoint(int(points[i][0] * width ), int(points[i][1] * height))
            point2 = QPoint(int(points[(i+1)%steps][0] * width ), int(points[(i+1)%steps][1] * height))
            z  = 0.7
            point3 = QPoint(int(center.x() + radius * math.cos(math.radians(angle - angle_step *z))), int(center.y() + radius * math.sin(math.radians(angle- angle_step * z))))
            polygon = QPolygon([point1, point2, point3])

            # Set the pen to NoPen to remove the outline
            # painter.setPen(Qt.NoPen)
            painter.drawPolygon(polygon)





if __name__ == '__main__':
    print('Starting the PyQt Application')
    app = QApplication(sys.argv)
    window = SimpleWindow()
    sys.exit(app.exec_())




# Message sent should like this b'V' where V is the value of the shutter between 0 and 100

# If you close the stream (i.e., the socket) that is communicating with the Nucleo, the Nucleo will detect that the stream was closed. When a socket is closed, the other end of the connection will receive an end-of-file (EOF) indication. This allows the Nucleo to detect that the connection has been terminated.


# TODO kod w pythonie na nukleo powinien byc asyncrhoniczny i caly czas czekac na polaczenie tcp_ip = 0.0.0.0 znaczy w teori ze na wszystkich ip i na tym jednym ustalonym porcie  
# TCP_IP = '0.0.0.0'
# TCP_PORT = 55151
# BUFFER_SIZE = 1024

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((TCP_IP, TCP_PORT))
# server_socket.listen(1)

# print("Waiting for a connection...")
# while True:
#     conn, addr = server_socket.accept()
#     print(f"Connection from: {addr}")
#     while True:
#         data = conn.recv(BUFFER_SIZE)
#         if not data:
#             break
#         print(f"Received data: {data}")
#         # Process the data
#     conn.close()
#     print("Connection closed, waiting for a new connection...")