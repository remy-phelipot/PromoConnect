import sys
from PySide.QtCore import *
from PySide.QtGui import *

import qrc_images

class InformationWidget(QWidget):
    def __init__(self,controller,parent=None):
        super(InformationWidget,self).__init__(parent)
        self.controller = controller
        # Create UI components
        self.mainLayout = QFormLayout(self)
        self.setLayout(self.mainLayout)
        self.tokenIdLabel = QLabel(self)
        self.lastUpdate = QLabel(self)

        self.timeSpinBox = QSpinBox(self)
        self.timeSpinBox.setValue(self.controller.refreshDuration)
        self.timeSpinBox.setMinimum(1)

        self.mainLayout.addRow(self.tr("Last connection : "), self.lastUpdate)
        self.mainLayout.addRow(self.tr("Disconnection token id : "), self.tokenIdLabel)
        self.mainLayout.addRow(self.tr("&Update interval (minutes):"), self.timeSpinBox)

        controller.networkUpdate.connect(self.updateLastUpdateDate)
        self.timeSpinBox.valueChanged.connect(self.updateRefreshInterval)

    def updateLastUpdateDate(self, date):
        lastUpdateText = date
        tokenText = self.controller.disconnectionTokken
        self.lastUpdate.setText(lastUpdateText)
        self.tokenIdLabel.setText(tokenText)

    def updateRefreshInterval(self,value):
        self.controller.refreshDuration = value

class ConnectionFormWidget(QWidget):
    informationsChanged = Signal(str,str)
    def __init__(self,parent=None):
        super(ConnectionFormWidget,self).__init__(parent)

        # Create UI components
        self.usernameField = QLineEdit()
        self.passwordField = QLineEdit()
        self.passwordField.setEchoMode(QLineEdit.Password)

        formLayout = QFormLayout(self)
        self.setLayout(formLayout)

        formLayout.addRow(self.tr("&Username:"), self.usernameField)
        formLayout.addRow(self.tr("&Password:"), self.passwordField)

        self.usernameField.textChanged.connect(self.onInformationsChanged)
        self.passwordField.textChanged.connect(self.onInformationsChanged)

    def onInformationsChanged(self):
        username = self.usernameField.text()
        password = self.passwordField.text()
        self.informationsChanged.emit(username,password)

    def checkInformations(self):
        username = self.usernameField.text()
        password = self.passwordField.text()
        return len(username) > 0 and len(password)

    def clear(self):
        self.usernameField.setText("")
        self.passwordField.setText("")

class ConnectionWindow(QDialog):
    def __init__(self, controller, parent=None):
        super(ConnectionWindow, self).__init__(parent)
        self.controller = controller

        self.setWindowTitle("PromoHack")
        self.setWindowIcon(QIcon(":/ressources/icon.ico"))

        self.resizable = False
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        self.informationWidget = InformationWidget(controller,self)
        self.connectionForm = ConnectionFormWidget(self)

        self.quitButton = QPushButton(self.tr("&Quit"),self)
        self.connectButton = QPushButton(self.tr("&Connect"),self)
        self.disconnectButton = QPushButton(self.tr("&Disconnect"),self)
        self.forceButton = QPushButton(self.tr("&Force!"),self)

        self.buttonLayout = QHBoxLayout(self)
        self.buttonLayout.addWidget(self.quitButton)

        self.mainLayout.addLayout(self.buttonLayout)

        self.systray = QSystemTrayIcon(QIcon(":/ressources/icon.png"),self)
        self.systray.activated.connect(self.onSystrayActivated)
        self.systray.show()

        self.readyToQuit = False

        self.doLayout()
        self.onFormInformationsChanged("","")

        self.connectionForm.informationsChanged.connect(self.onFormInformationsChanged)
        self.quitButton.clicked.connect(self.onQuitAction)
        self.connectButton.clicked.connect(self.onConnectAction)
        self.disconnectButton.clicked.connect(self.onDisconnectAction)
        self.forceButton.clicked.connect(self.forceConnection)

        controller.networkUpdate.connect(self.onNetworkStateUpdate)
        controller.connectionError.connect(self.onConnectionError)

    def doLayout(self):
        if self.controller.isConnected():
            self.connectButton.setEnabled(False)
            self.disconnectButton.setEnabled(True)
            self.forceButton.setEnabled(True)
            self.connectionForm.hide()
            self.connectButton.hide()
            self.mainLayout.insertWidget(0,self.informationWidget)
            self.buttonLayout.insertWidget(0,self.forceButton)
            self.buttonLayout.insertWidget(0,self.disconnectButton)
            self.mainLayout.removeWidget(self.connectionForm)
            self.buttonLayout.removeWidget(self.connectButton)
            self.informationWidget.show()
            self.disconnectButton.show()
            self.forceButton.show()
        else:
            self.connectButton.setEnabled(True)
            self.disconnectButton.setEnabled(False)
            self.forceButton.setEnabled(False)
            self.informationWidget.hide()
            self.disconnectButton.hide()
            self.forceButton.hide()
            self.mainLayout.insertWidget(0,self.connectionForm)
            self.buttonLayout.insertWidget(0,self.connectButton)
            self.mainLayout.removeWidget(self.informationWidget)
            self.buttonLayout.removeWidget(self.disconnectButton)
            self.buttonLayout.removeWidget(self.forceButton)
            self.connectionForm.show()
            self.connectButton.show()

    def onFormInformationsChanged(self,username,password):
        valid = self.connectionForm.checkInformations()
        self.connectButton.setEnabled(valid)
        if valid:
            self.controller.username = username
            self.controller.password = password

    def onQuitAction(self):
        self.readyToQuit = True
        self.controller.stopAutomaticConnection()
        self.close()

    def onConnectAction(self):
        self.connectButton.setEnabled(False)
        self.controller.startAutomaticConnection()

    def onDisconnectAction(self):
        self.disconnectButton.setEnabled(False)
        self.controller.stopAutomaticConnection()
        self.controller.performDisconnect()
        self.doLayout()

    def onConnectionError(self,message):
        msgBox = QMessageBox(self)
        msgBox.setText(message)
        msgBox.exec_()
        self.connectButton.setEnabled(True)

    def forceConnection(self):
        self.controller.performConnect()

    def onSystrayActivated(self):
        self.setVisible(not self.isVisible())

    def closeEvent(self, event):
        if not self.readyToQuit:
            event.ignore()
            self.hide()
        else:
            event.accept()

    @Slot(str)
    def onNetworkStateUpdate(self,date):
        self.doLayout()
