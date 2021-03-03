# Importing Required Modules
import sys
import platform
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import os

# GUI
from main_ui import Ui_MainWindow

# Importing Backend
from core import AuthWall


class MainWindow(QMainWindow):

    def __init__(self):
        # Initialize GUI
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize Backend
        self.core = AuthWall()

        # Move Window
        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # Custom Title Bar
        self.ui.frame_2.mouseMoveEvent = moveWindow

        # Exit Button
        self.ui.Exit.clicked.connect(lambda: sys.exit())

        # Remove Window Frame & Make background translucent
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Navigation Button Configurations
        self.ui.LogInBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Login))
        self.ui.RegisterBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Register))
        self.ui.DeleteUserBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Delete))
        self.ui.ResetPasswordBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Reset))

        # Reset
        self.reset()

        # LogIn Page Connect
        self.ui.UserL.textChanged.connect(self.checkLogin)
        self.ui.PassL.textChanged.connect(self.checkLogin)
        self.ui.SubmitL.clicked.connect(self.Login)

        self.show()

    def Login(self):
        msg = QMessageBox()
        if not self.core.check_existance(self.ui.UserL.text()):
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"The user '{self.ui.UserL.text()}' does not exist.")
            msg.setWindowTitle("Wrong Username")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        if self.core.authenticate(self.ui.UserL.text(), self.ui.PassL.text()):
            msg.setIcon(QMessageBox.Information)
            msg.setText("""You have entered the correct password.\n
                        This application is meant to be integrated into other projects.\n
                        This is just a demo.""")
            msg.setWindowTitle("Correct Password!")
        else:
            msg.setIcon(QMessageBox.Critical)
            msg.setText("""You have entered the wrong password.\n
                        This application is meant to be integrated into other projects.\n
                        This is just a demo.""")
            msg.setWindowTitle("Incorrect Password!")

    def checkLogin(self):
        if self.ui.UserL.text() not in [None, ""] and self.ui.PassL.text() not in [None, ""]:
            self.ui.SubmitL.setEnabled(True)
        else:
            self.ui.SubmitL.setEnabled(False)

    def reset(self):
        # LogIn Page
        self.ui.SubmitL.setEnabled(False)
        self.ui.UserL.setText('')
        self.ui.PassL.setText('')

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


# App Driver Code.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
