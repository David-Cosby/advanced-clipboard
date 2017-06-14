#! /usr/bin/python3




#							DISCLAIMER								#

# ADVANCED CLIPBOARD IS A MULTI-PLATFORM SOFTWARE DEVELOPED BY DAVID
# COSBY, A 15 YEAR OLD KID WHO HAS NO IDEA WHAT HE IS DOING.

# THE FOLLOWING CODE HAS SEVERAL EXAMPLES OF BAD PRACTICE, AND HURTS
# TO LOOK AT.

# BY DOWNLOADING THIS APPLICATION, YOU UNDERSTAND THAT THE AUTHOR OF
# THIS CATASTROPHE IS IN NO WAY, SHAPE, OR FORM RESPONSIBLE FOR LOSS
# OR DAMAGE OF ANY SORTS.

# AS THIS USES THE OPEN SOURCE MIT LICENSE, YALL CAN DO WHATEVER YOU
# FEEL LIKE WITH IT.

# I KINDLY ASK YOU, HOWEVER, TO ACCREDIT ME ALONG WITH ANY POTENTIAL
# COPIES OF THIS APPLICATION THAT YOU MAY PUBLISH. 

# 	THANKS, AND GOOD LUCK.
# 	DAVID COSBY, 6.13.17







version = "0.1.9"

enabled = False #will be enabled under initialization, disabling will turn off keyPress tracking

keysDown = []


import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui, QtWidgets, QtCore
import platform
from inputs import get_key
import os.path
import pyautogui
import pyperclip

from PyQt5.QtGui import *
from PyQt5.QtCore import *


#save file

import json
global saveFile #dictionary value. Will be either loaded or created


def buildDefaultFile():
	file = {}
	file["colorPicker"] = {}
	file["colorPicker"]["enabled"] = False
	file["colorPicker"]["format"] = 1 #enumerator index

	file["enablingShortCut"] = 2 #also an enumerator index

	with open("saveFile.json", "w") as json_file:
		json.dump(file, json_file)
	return file


def getSaveFile():


	json_fileFound = os.path.isfile("saveFile.json")

	if json_fileFound == True:
		with open("saveFile.json") as json_file:
			file = json.load(json_file)
			return file
	elif json_fileFound == False:
		file = buildDefaultFile()
		return file

	
	
def overrideSaveFile(file):
	with open("saveFile.json", "w") as json_file:
		json.dump(file, json_file)





class App(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Advanced Clipboard v'+version)
		self.resize(600, 350)
		self.home()
 
	def home(self):


		self.settingsOpen = False

		grid = QtWidgets.QGridLayout()

		# defining blank rows
		left = QtWidgets.QLabel("") #trust me I'm a pro.
		left1 = QtWidgets.QLabel("")
		right = QtWidgets.QLabel("")
		right1 = QtWidgets.QLabel("")

		grid.addWidget(left, 0, 0)
		grid.addWidget(left1, 0,1)
		grid.addWidget(right, 2,4)
		grid.addWidget(right1, 2,3)

		#Title
		font = QtGui.QFont("Segoe UI Light", 36, QtGui.QFont.Normal)
		
		title = QtWidgets.QLabel("Advanced Clipboard") # temporary
		title.setFont(font)
		title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
		grid.addWidget(title, 0, 1, 1, 3)

		#Informational text
		font2 = QtGui.QFont("Segoe UI Light", 11, QtGui.QFont.Normal)

		description = "You may minimize this window anytime you like.\n Advanced Clipboard will run in the background."
		desc = QtWidgets.QLabel(description)
		desc.setFont(font2)
		desc.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

		grid.addWidget(desc, 1, 1, 1, 3)

	   

		#Buttons
		settings = QtWidgets.QPushButton("Settings",self)
		info = QtWidgets.QPushButton("Help",self)
		manage = QtWidgets.QPushButton("Manage Clipboards",self)
		
		#button fonts
		font3 = QtGui.QFont("Segoe UI Light", 9, QtGui.QFont.Light)
		settings.setFont(font3)
		info.setFont(font3)
		manage.setFont(font3)

		manage.setEnabled(False)
		info.setEnabled(False)
		
		#Button Connections
		settings.clicked.connect(self.settingsGui)


		#option Buttons


		vertical = QtWidgets.QVBoxLayout()
		vertical.addWidget(settings)
		vertical.addWidget(info)
		vertical.addWidget(manage)
		grid.addLayout(vertical, 2, 2)

		
		self.setLayout(grid)
		self.show()



	def settingsGui(self):
			global win
			win = QtWidgets.QWidget()
			win.setWindowTitle('Settings')
			win.resize(400, 400)
			win.show()
			#ui components

			rows = QtWidgets.QFormLayout()
			form = QtWidgets.QFormLayout()
			grid = QtWidgets.QGridLayout()
			
			#title
			titleFont = QtGui.QFont("Segoe UI", 18, QtGui.QFont.Normal)
			title = QtWidgets.QLabel("Settings")
			title.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
			title.setFont(titleFont)

			#options
				#shortcut choices
			shortCutLabel = QtWidgets.QLabel("Which two keys will advanced clipboard respond to?")
			shortCutDropDown = QtWidgets.QComboBox()
			shortCutDropDown.addItem("Ctrl + Alt (Windows, OS X, Linux)")
			shortCutDropDown.addItem("META + Alt (OS X and Linux only)")            

			def updateEnablingShortCut(enum):
				saveFile["enablingShortCut"] = enum
			shortCutDropDown.setCurrentIndex(saveFile["enablingShortCut"])
			shortCutDropDown.currentIndexChanged.connect(updateEnablingShortCut)

			#todo: user changing the index should effect "saveFile"


			form.addRow(shortCutLabel)
			form.addRow(shortCutDropDown)

			blankSpace = QtWidgets.QLabel()
			form.addRow(blankSpace)
			# Color Picker
			colorPickerEnabled = QtWidgets.QCheckBox("Color Picker")
			colorPickerEnabled.setChecked(saveFile["colorPicker"]["enabled"])
			colorPickerEnabled.setEnabled(False)

			form.addRow(colorPickerEnabled)

			# Color Options
			colorOptionsLabel = QtWidgets.QLabel("Color Format")
			colorDropDown = QtWidgets.QComboBox()
				#color format choices
			colorDropDown.addItem("Hex")
			colorDropDown.addItem("Rgb")
			colorDropDown.addItem("Hsv")
			colorDropDown.addItem("Hsl (hsb)")
			colorDropDown.setEnabled(saveFile["colorPicker"]["enabled"])
			colorDropDown.setCurrentIndex(saveFile["colorPicker"]["format"])

			form.addRow(colorDropDown)

				#color picker signals
			def updateColorPickerEnabled(int):
				if int == 2: #True
					saveFile["colorPicker"]["enabled"] = True
					colorDropDown.setEnabled(True)
				elif int == 0: #False
					saveFile["colorPicker"]["enabled"] = False
					colorDropDown.setEnabled(False)
					
			colorPickerEnabled.stateChanged.connect(updateColorPickerEnabled)
			
			def updateColorFile(enum):
				saveFile["colorPicker"]["format"] = enum

			colorDropDown.currentIndexChanged.connect(updateColorFile)

			
			#buttons

			horizontal = QtWidgets.QHBoxLayout()


			def submitButton(self):
				overrideSaveFile(saveFile)
				win.close()
				## todo: save file
			def cancelButton(self):
				win.close()

			submit = QtWidgets.QPushButton("Submit")
			submit.clicked.connect(submitButton)
			cancel = QtWidgets.QPushButton("Cancel")
			cancel.clicked.connect(cancelButton)
			horizontal.addWidget(submit)
			horizontal.addWidget(cancel)


			rows.addRow(title)
			rows.addRow(form)
			blankSpace = QtWidgets.QLabel()

			grid.addLayout(rows,0,0)
			grid.addLayout(horizontal, 1, 0)
			win.setLayout(grid)
	def startKeyStuff(self):
		trackKeysDown()



# Keyboard stuffs

def firstEnabler():#reading from user settings, it will return the key code for the left enabler
	shortCutEnum = saveFile["enablingShortCut"]
	if shortCutEnum == 0: #Control
		return "KEY_LEFTCTRL"
	else:
		return "KEY_LEFTMETA"

def secondEnabler():#reading from user settings, it will return the key code for the left enabler
	shortCutEnum = saveFile["enablingShortCut"]
	return "KEY_LEFTALT"
def altSecondEnabler():
	shortCutEnum = saveFile["enablingShortCut"]
	return "KEY_RIGHTALT"



keys = {}
keys["C"] = False
keys["V"] = False
keys["FirstEnabler"] = False
keys["SecondEnabler"] = False


def listenForShortCuts(app):
	if keys["FirstEnabler"] and keys["SecondEnabler"]:
		if keys["C"] is True:
			keys["C"] = False #debounce
			copyClipboardMenu(app)
		if keys["V"] is True:
			keys["V"] = False #debounce
			pasteClipboardMenu(app)




def trackKeysDown(): #only keeps track of what keys are currently down.
	app = QApplication(sys.argv)
	while enabled:
		events = get_key()
		for event in events:
			if event.state is not 2:
				#We're about to do this the hard way, but it is also the way that makes me not feel worried about tracking the user's keys.
				down = event.state == 1
				if event.code is "KEY_C":
					keys["C"] = down
				elif event.code is "KEY_V":
					keys["V"] = down
				elif event.code is firstEnabler():
					keys["FirstEnabler"] = down
				elif event.code is secondEnabler():
					keys["SecondEnabler"] = down
				elif event.code is altSecondEnabler(): #support for left and right alt buttons
					keys["SecondEnabler"] = down
				listenForShortCuts(app)



#clipboards

clipboards = []

def canAddClipboard():
	return len(clipboards) < 9


def newClipboard():
	if canAddClipboard():
		name =  "Clipboard " + str(len(clipboards)+1)
		clipboard = {}
		clipboard["Name"] = name
		clipboard["Value"] = ""
		clipboards.append(clipboard)





def copy(index, app):
	clipboard = app.clipboard()
	Mode = clipboard.Clipboard

	initialMimeData = clipboard.text(mode = Mode)
	
	pyautogui.hotkey('ctrl', 'c') #copy

	
	mimeData = clipboard.text(mode = Mode)
	clipboards[index-1]["Data"] = mimeData

	pyperclip.copy(initialMimeData) 


def paste(index, app):
	
	clipboard = app.clipboard()
	Mode = clipboard.Clipboard
	data = clipboards[index-1]["Data"]

	initialMimeData = clipboard.text(mode = Mode)

	pyperclip.copy(data) 
	
	pyautogui.hotkey('ctrl', 'v') #paste

	pyperclip.copy(initialMimeData) 





def copyClipboardMenu(app):

#sloppy fix?

	def ct1():
		copy(1, app)
	def ct2():
		copy(2, app)
	def ct3():
		copy(3, app)
	def ct4():
		copy(4, app)
	def ct5():
		copy(5, app)
	def ct6():
		copy(6, app)
	def ct7():
		copy(7, app)
	def ct8():
		copy(8, app)
	def ct9():
		copy(9, app)
	def ct10():
		copy(10, app)




	Menu = QtWidgets.QMenu("Copy")
	Menu.addSection("Copy to:")
	index = 0
	actions = []

	for clipboard in clipboards:
		index = (index + 1) % 10
		newaction = QtWidgets.QAction(clipboard["Name"])
		newaction.setToolTip("Copy data to " + clipboard["Name"])

	
		actions.append(newaction)

		if index == 1:
			newaction.triggered.connect(ct1)
		elif index == 2:
			newaction.triggered.connect(ct2)
		elif index == 3:
			newaction.triggered.connect(ct3)
		elif index == 4:
			newaction.triggered.connect(ct4)
		elif index == 5:
			newaction.triggered.connect(ct5)
		elif index == 6:
			newaction.triggered.connect(ct6)
		elif index == 7:
			newaction.triggered.connect(ct7)
		elif index == 8:
			newaction.triggered.connect(ct8)
		elif index == 9:
			newaction.triggered.connect(ct9)
		elif index == 10:
			newaction.triggered.connect(ct10)


	for action in actions:
		Menu.addAction(action)


	if canAddClipboard():
		Menu.addSeparator()
		
		def newTriggerFunc():
			index = len(clipboards) + 1
			newClipboard()
			copy(index, app)

		new = Menu.addAction("New Clipboard")
		new.triggered.connect(newTriggerFunc)

	position = QtGui.QCursor.pos()
	Menu.exec(position)


def pasteClipboardMenu(app):

	#sloppy fix?

	def pt1():
		paste(1, app)
	def pt2():
		paste(2, app)
	def pt3():
		paste(3, app)
	def pt4():
		paste(4, app)
	def pt5():
		paste(5, app)
	def pt6():
		paste(6, app)
	def pt7():
		paste(7, app)
	def pt8():
		paste(8, app)
	def pt9():
		paste(9, app)
	def pt10():
		paste(10, app)



	menu = QtWidgets.QMenu("Paste")
	menu.addSection("Paste from:")

	index = 0

	actions = []

	for clipboard in clipboards:
		index = (index + 1) % 10
		action = QtWidgets.QAction(clipboard["Name"])
		action.setToolTip("Paste data from " + clipboard["Name"])

		def triggerFunc():
			paste(index, app)
			menu.setParent(None)


		if index == 1:
			action.triggered.connect(pt1)
		elif index == 2:
			action.triggered.connect(pt2)
		elif index == 3:
			action.triggered.connect(pt3)
		elif index == 4:
			action.triggered.connect(pt4)
		elif index == 5:
			action.triggered.connect(pt5)
		elif index == 6:
			action.triggered.connect(pt6)
		elif index == 7:
			action.triggered.connect(pt7)
		elif index == 8:
			action.triggered.connect(pt8)
		elif index == 9:
			action.triggered.connect(pt9)
		elif index == 10:
			action.triggered.connect(pt10)

		actions.append(action)

	for action in actions:
		menu.addAction(action)

	position = QtGui.QCursor.pos()
	menu.exec(position)



def isPlatformSupported():
	#if platform.system() == "Windows" or platform.system() == "Linux": #due to current method of creating new threads, OS X (Darwin Platform) may or may not be supported. I'll have to check.
	#	return True
	#else:
	#	return False

	return True #until I experiment with other platforms, Let's just leave this on


# INITIALIZATION


from multiprocessing import Process

def exitHandler():
	enabled = False #disable key tracking
	if secondThread:
		secondThread.terminate()

if __name__ == '__main__':
	if isPlatformSupported():
		print("oh good, you are on a supported platform!")

		enabled = True
		saveFile = getSaveFile()

		# create default clipboard
		newClipboard()

		global secondThread #i'm such a cheater.
		secondThread = Process(target = trackKeysDown) #tracking key input in the background
		secondThread.start()

		global app
		app = QApplication(sys.argv)
		app.aboutToQuit.connect(exitHandler)
		ex = App()
		
		sys.exit(app.exec_())


	else:
		print('Your platform is not supported!')
		


