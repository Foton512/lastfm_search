# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
import json
from settings import *
from main_window_widget import MainWindowWidget

class MainWindow(QMainWindow):
    def __init__(self, model):
        super(MainWindow, self).__init__()
        self.model = model
        self.initUI()

    def initUI(self):
        self.mainWindowWidget = MainWindowWidget(self, self.model)
        mainLayout = QVBoxLayout()
        self.textEdit = QTextEdit()
        mainLayout.addWidget(self.textEdit)
        self.setLayout(mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.setGeometry(windowLeft, windowTop, windowWidth, windowHeight)
        self.setWindowTitle(u"lastfm search")    
        self.show()
