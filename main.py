import os
from config import whitelist
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from screeninfo import get_monitors


class Widget(QMainWindow):
    def __init__(self):
        super(Widget, self).__init__()

        self.image_index = 0  # Default image index
        self.preset_pos = 3  # Default preset pos
        self.transparency = .5  # Default transparency value

        self.files = os.listdir(os.getcwd())  # All file in current dir
        self.white_files = []  # All whitelist files in current dir
        self.updateFiles()

        # Initializing image label
        self.photo_size = .5

        self.photo = QImage()
        self.photo_label = QLabel(self)  # Creating image label
        self.photo_label.setScaledContents(True)
        self.setImage(0)
        self.updateWindow()

    def setImage(self, _index: int):
        # Getting image data
        with open(self.white_files[_index], mode='rb') as pbytes:
            self.photo.loadFromData(pbytes.read())

        # Adjusting image size
        self.resize(QPixmap().fromImage(self.photo).size())

        # Setting up label photo from image
        self.photo_label.resize(self.size())
        self.photo_label.setPixmap(QPixmap().fromImage(self.photo))
        self.photo_label.setScaledContents(True)

        # Adjusting position
        self.adjustPos(self.preset_pos)

    def changeImage(self):
        self.updateFiles()

        self.image_index += 1

        if self.image_index > len(self.white_files) - 1:
            self.image_index = 0

        self.setImage(self.image_index)

        # Adjusting image position
        self.resizeImage()

    def adjustPos(self, preset_pos: int):
        monitor = get_monitors()[0]

        # Changing position of window according to preset_pos
        if preset_pos == 1:
            self.setGeometry(0, 0, self.width(), self.height())
        elif preset_pos == 2:
            self.setGeometry(monitor.width - self.width(), 0, self.width(), self.height())
        elif preset_pos == 3:
            self.setGeometry(0, monitor.height - self.height(), self.width(), self.height())
        elif preset_pos == 4:
            self.setGeometry(monitor.width - self.width(), monitor.height - self.height(), self.width(), self.height())

        self.photo_label.resize(self.size())

    def resizeImage(self):
        self.resize(int(self.photo.width() * self.photo_size),
                    int(self.photo.height() * self.photo_size))
        self.adjustPos(self.preset_pos)

    def keyPressEvent(self, e):
        # Zoom in
        if e.key() == Qt.Key_Equal:
            self.photo_size += .01

            self.resize(int(self.photo.width() * self.photo_size),
                        int(self.photo.height() * self.photo_size))
            self.adjustPos(self.preset_pos)

        # Zoom out
        elif e.key() == Qt.Key_Minus:
            self.photo_size -= .01

            self.resize(int(self.photo.width() * self.photo_size),
                        int(self.photo.height() * self.photo_size))
            self.adjustPos(self.preset_pos)

        # Changing preset pos
        elif e.key() == Qt.Key_Right:
            self.preset_pos += 1

            if self.preset_pos > 4:
                self.preset_pos = 1

            self.adjustPos(self.preset_pos)

        # Changing displayed image
        elif e.key() == Qt.Key_Left:
            self.changeImage()

        # Lower window transparency
        elif e.key() == Qt.Key_Down:
            self.transparency = self.transparency - .1

            if self.transparency < .05:
                self.transparency = .05

            self.setWindowOpacity(self.transparency)

        # Higher window transparency
        elif e.key() == Qt.Key_Up:
            self.transparency = self.transparency + .1

            if self.transparency > 1:
                self.transparency = 1

            self.setWindowOpacity(self.transparency)

    def updateWindow(self):
        self.setWindowTitle('EzExam')
        self.setWindowIcon(QIcon('exam.png'))

        # Setting up base size
        self.resize(500, 500)

        # Adding some attributes
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        # Adjusting window pos
        self.adjustPos(self.preset_pos)

        # Adjusting window transparency
        self.setWindowOpacity(self.transparency)

        # First image resizing
        self.resize(int(self.photo.width() * self.photo_size),
                    int(self.photo.height() * self.photo_size))
        self.adjustPos(self.preset_pos)

    def updateFiles(self):
        self.files = os.listdir(os.getcwd())  # All file in current dir
        self.white_files = []  # All whitelist files in current dir

        for file in self.files:
            ext = file.split('.')[-1]  # File extension

            # Appending all whitelisted files to white_files
            if ext in whitelist:
                self.white_files.append(os.getcwd() + '\\' + file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Widget()
    window.show()

    app.exec()
