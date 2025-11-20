#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication
from desktop.ui_main import MainWindow

def run_desktop():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
