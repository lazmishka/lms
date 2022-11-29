from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import sqlite3


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Лазарев проект PyQt5")

        self.setGeometry(100, 100, 1240, 800)
        self.fixedX = 1240
        self.fixedY = 800
        self.newX = 1240
        self.newY = 800
        self.setFixedSize(self.fixedX, self.fixedY)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        #self.image.size()

        self.image.fill(Qt.white)
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black

        self.lastPoint = QPoint()

        con = sqlite3.connect("log.sqlite")
        self.con = con
        self.curs = con.cursor()

        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu("File")

        b_size = mainMenu.addMenu("Brush Size")

        b_color = mainMenu.addMenu("Brush Color")

        filter_Menu = mainMenu.addMenu("Filter") 

        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl + S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction("Clear", self)
        clearAction.setShortcut("Ctrl + C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        button_action_open = QAction("Open", self)
        button_action_open.setStatusTip("Open")
        button_action_open.triggered.connect(self.open)
        fileMenu.addAction(button_action_open)

        pix_4 = QAction("4px", self)
        b_size.addAction(pix_4)
        pix_4.triggered.connect(self.Pixel_4)

        pix_7 = QAction("7px", self)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(self.Pixel_7)

        pix_9 = QAction("9px", self)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(self.Pixel_9)

        pix_12 = QAction("12px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(self.Pixel_12)

        black = QAction("Black", self)
        b_color.addAction(black)
        black.triggered.connect(self.blackColor)

        white = QAction("White", self)
        b_color.addAction(white)
        white.triggered.connect(self.whiteColor)

        green = QAction("Green", self)
        b_color.addAction(green)
        green.triggered.connect(self.greenColor)

        yellow = QAction("Yellow", self)
        b_color.addAction(yellow)
        yellow.triggered.connect(self.yellowColor)

        red = QAction("Red", self)
        b_color.addAction(red)
        red.triggered.connect(self.redColor)

        random_period_brush = QAction("Random period brush", self)
        filter_Menu.addAction(random_period_brush)
        random_period_brush.triggered.connect(self.mixed_function)

        file_menu_action = QAction("file")
        file_menu_action.triggered.connect(self.file_window)

        # file_toolbar = self.addToolBar('File')
        # file_toolbar.addAction(button_action_open)
        # file_toolbar.addAction(clearAction)
        # file_toolbar.addAction(saveAction)
        # file_toolbar.setStyleSheet('Background-color: white')
        # file_toolbar.addSeparator()
        # file_toolbar.addSeparator()


    def action_log(self, msg_text):
        unix_time = int(datetime.now().timestamp())
        query_str = f"""INSERT INTO log (datatime, action_msg) VALUES ({unix_time}, "{msg_text}")"""
        if self.con:
            result = self.curs.execute(query_str)
            self.con.commit()
        else:
            pass

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.drawing = True
            p = event.localPos()
            xm = (self.newX/self.fixedX)*p.x()
            ym = (self.newY/self.fixedY)*p.y()
            p.setX(xm)
            p.setY(ym)
            self.lastPoint = p

            pass

    def mouseMoveEvent(self, event):

        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)

            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            p = event.localPos()
            xm = (self.newX/self.fixedX)*p.x()
            ym = (self.newY/self.fixedY)*p.y()
            p.setX(xm)
            p.setY(ym)
            painter.drawLine(self.lastPoint, p)

            self.lastPoint = p
            self.update()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)

        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)
        self.action_log(f"Сохранил файл: {filePath}")

    def open(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return

        self.image.load(filePath)
        #self.image.size().scale(self.fixedX, self.fixedY, Qt.KeepAspectRatioByExpanding)
        self.newX = self.image.size().width()
        self.newY = self.image.size().height()
        self.update()

        self.action_log(f"открыл файл: {filePath}")

    def clear(self):
        self.image.fill(Qt.white)
        self.update()
        self.action_log("Очистил поле")

    def Pixel_4(self):
        self.brushSize = 4
        self.action_log(f"Установил толщину пера на 4 пикселей")

    def Pixel_7(self):
        self.brushSize = 7
        self.action_log(f"Установил толщину пера на 7 пикселей")

    def Pixel_9(self):
        self.brushSize = 9
        self.action_log(f"Установил толщину пера на 9 пикселей")

    def Pixel_12(self):
        self.brushSize = 12
        self.action_log(f"Установил толщину пера на 12 пикселей")

    def blackColor(self):
        self.brushColor = Qt.black
        self.action_log(f"Выбрал черный цвет")

    def whiteColor(self):
        self.brushColor = Qt.white
        self.action_log(f"Выбрал белый цвет")

    def greenColor(self):
        self.brushColor = Qt.green
        self.action_log(f"Выбрал зеленый цвет")

    def yellowColor(self):
        self.brushColor = Qt.yellow
        self.action_log(f"Выбрал желтый цвет")

    def redColor(self):
        self.brushColor = Qt.red
        self.action_log(f"Выбрал красный цвет")

    def mixed_function(self):
        from PIL import Image
        import random

        def image_filter(src_color, i, width):
            """Модифицирует цвет пиксела синхронно по все цветовым каналам на случайную величину
            масштаб отклонений зависит от координаты по ширине
            менее подвержены темные участки"""

            percent_mod = random.randint(int(width/5), int(width/4) + i % 20)
            rand_koef = random.randint(0, percent_mod)
            r0,g0,b0 = src_color.red(), src_color.green(), src_color.blue()
            r = r0 + int(r0 * rand_koef / 100)
            g = g0 + int(g0 * rand_koef / 100)
            b = b0 + int(b0 * rand_koef / 100)
            return QColor.fromRgb(r % 256, g % 256, b % 256)

        x, y = self.image.width(), self.image.height()
        for i in range(x):
            for j in range(y):
                self.image.setPixelColor(i, j, image_filter(self.image.pixelColor(i,j),i,x))
        self.update()
        self.action_log(f"Применил фильтр")

    def file_window(self):
        pass






App = QApplication(sys.argv)

window = Window()

window.show()

sys.exit(App.exec())
