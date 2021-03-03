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

        # Add Security Questions
        self.ui.sqR.addItem("Your favorite actor?")
        self.ui.sqR.addItem("Your celebrity/high school crush?")
        self.ui.sqR.addItem("Your kink?")
        self.ui.sqR.setCurrentIndex(-1)
        self.ui.sqP.addItem("Your favorite actor?")
        self.ui.sqP.addItem("Your celebrity/high school crush?")
        self.ui.sqP.addItem("Your kink?")
        self.ui.sqP.setCurrentIndex(-1)

        # Navigation Button Configurations
        self.ui.LogInBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Login))
        self.ui.RegisterBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Register))
        self.ui.DeleteUserBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Delete))
        self.ui.ResetPasswordBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Reset))

        # Home Button Configuration
        self.ui.Back.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Home))
        self.ui.Back.clicked.connect(
            lambda: self._reset())

        # Reset
        self._reset()

        # LogIn Page Connect
        self.ui.UserL.textChanged.connect(self.checkLogin)
        self.ui.PassL.textChanged.connect(self.checkLogin)
        self.ui.SubmitL.clicked.connect(self.Login)

        # Register Page Connect
        self.ui.UserR.textChanged.connect(self.checkRegister)
        self.ui.PassR.textChanged.connect(self.checkRegister)
        self.ui.sqR.currentIndexChanged.connect(self.checkRegister)
        self.ui.SQR.textChanged.connect(self.checkRegister)
        self.ui.SubmitR.clicked.connect(self.Register)

        # Initialize Window
        self.show()

    def Register(self):
        msg = QMessageBox()
        self.core.add(self.ui.UserR.text(), self.ui.PassR.text(),
                      self.ui.SQR.text(), str(self.ui.sqR.currentIndex()))
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("User Registered")
        msg.setText(f"User {self.ui.UserR.text()} Registered")
        msg.setInformativeText(
            "This application is meant to be integrated into other projects. This is just a demo.")
        msg.exec_()
        self._reset()

    def Login(self):
        msg = QMessageBox()
        if not self.core.check_existance(self.ui.UserL.text()):
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"The user '{self.ui.UserL.text()}' does not exist.")
            msg.setWindowTitle("User Not Found")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        if self.core.authenticate(self.ui.UserL.text(), self.ui.PassL.text()):
            msg.setIcon(QMessageBox.Information)
            msg.setText("You have entered the correct password.")
            msg.setInformativeText("This application is meant to be integrated into other projects. This is just a demo.")
            msg.setWindowTitle("Correct Password!")
        else:
            msg.setIcon(QMessageBox.Critical)
            msg.setText("You have entered the incorrect password.")
            msg.setInformativeText(
                "This application is meant to be integrated into other projects. This is just a demo.")
            msg.setWindowTitle("Incorrect Password!")
        msg.exec_()
        self._reset()

    def checkLogin(self):
        if self.ui.UserL.text() not in [None, ""] and self.ui.PassL.text() not in [None, ""]:
            self.ui.SubmitL.setEnabled(True)
        else:
            self.ui.SubmitL.setEnabled(False)

    def checkRegister(self):
        exist = self.core.check_existance(
            self.ui.UserR.text() if self.ui.UserR.text() is not None else "")
        if exist:
            self.ui.label_9.setText("That username is taken.")
            self.ui.SubmitR.setEnabled(False)
        else:
            self.ui.label_9.setText("Select Security Question:")
        if (self.ui.UserR.text() not in [None, ""] and self.ui.PassR.text() not in [None, ""] and
            self.ui.SQR.text() not in [None, ""] and self.ui.sqR.currentText() != -1 and not exist):
            self.ui.SubmitR.setEnabled(True)
        else:
            self.ui.SubmitR.setEnabled(False)

    def _reset(self):
        # LogIn Page
        self.ui.stackedWidget.setCurrentWidget(self.ui.Home)
        self.ui.SubmitL.setEnabled(False)
        self.ui.UserL.setText('')
        self.ui.PassL.setText('')
        self.ui.sqR.setCurrentIndex(-1)
        self.ui.sqP.setCurrentIndex(-1)
        self.ui.SubmitR.setEnabled(False)
        self.ui.UserR.setText('')
        self.ui.PassR.setText('')
        self.ui.SQR.setText('')

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


# App Driver Code.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
