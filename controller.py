from network import *
import connectionWindow

class Controller:
	def __init__(self):
		self.disconnectionTokken = ''
		self.username = ''
		self.password = ''
		
	def connect(self):
		self.disconnectionTokken = connect(self.username,
										   self.password)
		
	def disconnect():
		disconnect(self.disconnectionTokken)
