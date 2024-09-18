import sys
import math
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.speed = 50  
        self.direction = 1
        
        self.label = QtWidgets.QLabel()
        self.setFixedSize(600, 600)
        canvas = QtGui.QPixmap(600, 600)
        canvas.fill(Qt.GlobalColor.white)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.last_x, self.last_y = None, None
        
        self.StartDraw()
        self.animation2()

    def set_speed(self, speed):
        self.speed = speed
        self.animation2()

    def animation2(self):
        self.child = QWidget(self)
        self.child.setStyleSheet("""
            border-radius: 2.5px;
            min-height: 5px;
            max-height: 5px;
            min-width: 5px;
            max-width: 5px;
            background-color: red;
        """)
        
        self.anim_group = QSequentialAnimationGroup()
        
        for i in range(0, 360, 4):  
            angle = math.radians(i * self.direction) 
            pointXY = QPoint(int(297.5 + 200 * math.cos(angle)), int(297.5 + 200 * math.sin(angle)))
            self.anim = QPropertyAnimation(self.child, b"pos")
            self.anim.setEndValue(pointXY)
            self.anim.setDuration(self.speed) 
            self.anim_group.addAnimation(self.anim)
        
        self.anim_group.setLoopCount(-1) 
        self.anim_group.start()

    def StartDraw(self):
        c_rad = 400
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen()
        pen.setWidth(10)
        pen.setColor(QtGui.QColor('blue'))
        
        painter.drawRoundedRect(300 - c_rad // 2,  300 - c_rad // 2, c_rad, c_rad, c_rad // 2, c_rad // 2)
        #painter.drawLine(0, 300, 600, 300)
        #painter.drawLine(300, 0, 300, 600)
        
        painter.end()
        self.label.setPixmap(canvas)

    def mouseMoveEvent(self, e):
        if self.last_x is None: 
            self.last_x = e.position().x()
            self.last_y = e.position().y()
            return 
        
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        painter.drawLine(int(self.last_x), int(self.last_y), int(e.position().x()), int(e.position().y()))
        painter.end()
        self.label.setPixmap(canvas)

        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
