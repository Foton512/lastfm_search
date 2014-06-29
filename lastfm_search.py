# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from main_window import MainWindow
from model import Model

def main():
    app = QtGui.QApplication(sys.argv)
    main = MainWindow(Model())
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
