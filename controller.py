from PySide.QtCore import *
from network import *
import time, threading

class Controller(QObject):
    networkUpdate = Signal(str)
    connectionError = Signal(str)

    def __init__(self):
        super(Controller, self).__init__()
        self.disconnectionTokken = ''
        self.username = ''
        self.password = ''
        self.refreshDuration = 60 # 60 minutes
        self.lastUpdate = "never"
        self.connectionTimer = None
        self.connected = False

    def performConnect(self):
        self.disconnectionTokken = connect(self.username,
                                           self.password)
        self.lastUpdate = time.strftime("%c")
        self.connected = True
        self.networkUpdate.emit(self.lastUpdate)

    def performDisconnect(self):
        self.stopAutomaticConnection()
        disconnect(self.disconnectionTokken)
        self.connected = False

    def startAutomaticConnection(self):
        self.connectLoop()

    def stopAutomaticConnection(self):
        if(self.connectionTimer != None):
            self.connectionTimer.cancel()
            self.connectionTimer = None

    def connectLoop(self):
        try:
            self.performConnect()
            self.connectionTimer = threading.Timer(self.refreshDuration*60,
                                                   self.connectLoop)
            self.connectionTimer.start()
        except Exception as e:
            self.connectionError.emit(str(e))


    def getLastUpdate(self):
        return self.lastUpdate

    def isConnected(self):
        return self.connected
