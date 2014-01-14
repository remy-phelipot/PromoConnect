import sys
from PySide.QtCore import *
from PySide.QtGui import *

class ConnectionWindow(QDialog):
    def __init__(self, controller, parent=None):
        super(ConnectionWindow, self).__init__(parent)
        self.setWindowTitle("Connection")
        self.buildConnectionUI()
        self.resizable = False
        self.controller = controller

    def buildConnectionUI(self):
        mainLayout = QVBoxLayout()

        self.userNameField = QLineEdit()
        self.passwordField = QLineEdit()

        formLayout = QFormLayout()
        formLayout.addRow(self.tr("&Username:"), self.userNameField)
        formLayout.addRow(self.tr("&Password:"), self.passwordField)

        buttonLayout = QHBoxLayout()
        self.connectButton = QPushButton("Connect", self)
        self.quitButton = QPushButton("Quit", self)

        self.connectButton.setEnabled(False)

        buttonLayout.addWidget(self.connectButton)
        buttonLayout.addWidget(self.quitButton)

        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonLayout)
        
        #systray
        self.systray = QSystemTrayIcon(self)
        self.systray.show()
        self.systray.setToolTip("Last connection : date")

        self.setLayout(mainLayout)

        self.quitButton.clicked.connect(self.quitButtonCallback)
        self.connectButton.clicked.connect(self.connectButtonCallback)
        self.userNameField.textChanged.connect(self.fieldsChanged)
        self.passwordField.textChanged.connect(self.fieldsChanged)


    def connectButtonCallback(self):
        username = self.userNameField.text()
        password = self.passwordField.text()
        self.controller.username = username
        self.controller.password = password

        try:
            self.controller.connect()
        except Exception as e:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(str(e))
            msgBox.exec_()

    def quitButtonCallback(self):
        self.close()

    def fieldsChanged(self):
        username = self.userNameField.text()
        password = self.passwordField.text()

        if(len(username) == 0 or len(password) == 0):
            self.connectButton.setEnabled(False)
        else:
            self.connectButton.setEnabled(True)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    form = ConnectionWindow()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec_())
