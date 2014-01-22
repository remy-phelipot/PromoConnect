from PySide.QtCore import *
from Network import *
import time, threading

class Controller(QObject):
    connected = Signal()
    disconnected = Signal()
    connectionError = Signal(str)

    def __init__(self):
        super(Controller, self).__init__()
        self.disconnectionTokken = ''
        self.username = ''
        self.password = ''
        self.connectionInterval = 1
        self.lastUpdate = "never"
        self.connectionTimer = None
        self.isConnected = False

    def performConnect(self):
        self.disconnectionTokken = connect(self.username,
                                           self.password)
        self.lastUpdate = time.strftime("%c")
        self.isConnected = True
        self.connected.emit()

    def performDisconnect(self):
        self.stopAutomaticConnection()
        disconnect(self.disconnectionTokken)
        self.isConnected = False
        self.disconnected.emit()

    def startAutomaticConnection(self):
        try:
            self.performConnect()
            self.connectionTimer = threading.Timer(self.connectionInterval*60,
                                                   self.startAutomaticConnection)
            self.connectionTimer.start()
        except Exception as e:
            self.connectionError.emit(str(e))

    def stopAutomaticConnection(self):
        if(self.connectionTimer != None):
            self.connectionTimer.cancel()
            self.connectionTimer = None
