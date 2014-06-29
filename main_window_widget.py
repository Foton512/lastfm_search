# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, pyqtSlot
from settings import *

class MainWindowWidget(QWidget):
    def __init__(self, parent, model):
        super(MainWindowWidget, self).__init__(parent)
        self.model = model
        self.model.searchCompleted.connect(self.searchCompleted)
        self.initUI()

    def initUI(self):
        artistsLayout = QHBoxLayout()
        artistsLayout.setContentsMargins(0, 0, 0, 0)
        artistsLayout.setAlignment(Qt.AlignLeft)
        artistsLayout.addWidget(QLabel(u"Number or artists [0, 1000]:"));
        self.artistsEdit = QLineEdit("100")
        self.artistsEdit.setMinimumWidth(100)
        self.artistsEdit.setMaximumWidth(100)
        artistsLayout.addWidget(self.artistsEdit);
        artistsLayout.addItem(QSpacerItem(0, 0, hPolicy = QSizePolicy.Expanding))
        artistsWidget = QWidget()
        artistsWidget.setLayout(artistsLayout)

        weightLayout = QHBoxLayout()
        weightLayout.setContentsMargins(0, 0, 0, 0)
        weightLayout.setAlignment(Qt.AlignLeft)
        weightLayout.addWidget(QLabel(u"Tag weight threshold [0, 100]:"));
        self.weightEdit = QLineEdit("60")
        self.weightEdit.setMinimumWidth(100)
        self.weightEdit.setMaximumWidth(100)
        weightLayout.addWidget(self.weightEdit);
        weightLayout.addItem(QSpacerItem(0, 0, hPolicy = QSizePolicy.Expanding))
        weightWidget = QWidget()
        weightWidget.setLayout(weightLayout)

        tagLayout = QHBoxLayout()
        tagLayout.setContentsMargins(0, 0, 0, 0)
        tagLayout.addWidget(QLabel(u"Tag:"));
        self.tagEdit = QLineEdit()
        self.tagEdit.setMinimumWidth(300)
        self.tagEdit.setMaximumWidth(300)
        tagLayout.addWidget(self.tagEdit);
        searchButton = QPushButton("Search")
        searchButton.clicked.connect(self.search)
        tagLayout.addWidget(searchButton);
        tagLayout.addItem(QSpacerItem(0, 0, hPolicy = QSizePolicy.Expanding))
        tagWidget = QWidget()
        tagWidget.setLayout(tagLayout)

        textLayout = QHBoxLayout()
        textLayout.setContentsMargins(0, 0, 0, 0)
        self.resultEdit = QTextEdit()
        self.resultEdit.setReadOnly(True)
        textLayout.addWidget(self.resultEdit);
        textWidget = QWidget()
        textWidget.setLayout(textLayout)

        layout = QVBoxLayout()
        layout.addWidget(artistsWidget)
        layout.addWidget(weightWidget)
        layout.addWidget(tagWidget)
        layout.addWidget(textWidget)
        self.setLayout(layout)

    def search(self):
        self.model.search(str(self.tagEdit.text()), self.artistsEdit.text().toInt()[0], self.weightEdit.text().toInt()[0])

    @pyqtSlot(object)
    def searchCompleted(self, result):
        self.resultEdit.setText(result)
