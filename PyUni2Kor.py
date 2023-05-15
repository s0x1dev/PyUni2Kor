import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
UI_class = uic.loadUiType(BASE_DIR+'\PyUni2Kor.ui')[0]

class MyWindow(QMainWindow, UI_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.plainTextEdit_uni.textChanged.connect(self.update_kor)
        self.plainTextEdit_kor.textChanged.connect(self.update_uni)
        self.checkBox_alwaysOnTop.setChecked(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint) # always on top을 default로 설정
        self.show()
        self.checkBox_alwaysOnTop.stateChanged.connect(self.toggle_always_on_top)

    def update_kor(self):
        text = self.plainTextEdit_uni.toPlainText()
        text = text.replace('\\\\u', '\\u') # AWS에서 표시되는 unicode 양식 변경
        self.plainTextEdit_kor.blockSignals(True)
        self.plainTextEdit_kor.setPlainText(text.encode('utf-8').decode('unicode_escape'))
        self.plainTextEdit_kor.blockSignals(False)
        
    def update_uni(self):
        text = self.plainTextEdit_kor.toPlainText()
        self.plainTextEdit_uni.blockSignals(True)
        self.plainTextEdit_uni.setPlainText(text.encode('unicode_escape').decode('utf-8').replace('\\u','\\\\u'))
        self.plainTextEdit_uni.blockSignals(False)

    def toggle_always_on_top(self, state):
        if state == Qt.CheckState.Checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    Window = MyWindow() 
    Window.show()
    sys.exit(app.exec_())