import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication

# Default url
url = ''
 
# Main Canvas and Functions
class Main(QtWidgets.QMainWindow):
 
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.CreateUI()
 
	def CreateUI(self):
 		
 		# Create Necessary Widgets 
		self.centralwidget = QtWidgets.QWidget(self)
 			
		self.line = QtWidgets.QLineEdit(self)
		self.line.setMinimumSize(500, 20)
		self.line.setStyleSheet('font-size:15px;')
 		
 			# Enter URL
		self.enter = QtWidgets.QPushButton(self)
		self.enter.resize(0,0)
		self.enter.clicked.connect(self.set_url)
		self.enter.setShortcut('Return')
 		
 			# Reload Button
		self.reload = QtWidgets.QPushButton('↻',self)
		self.reload.setMinimumSize(20, 20)
		self.reload.setShortcut('F5')
		self.reload.setStyleSheet('font-size:23px;')
		self.reload.clicked.connect(self.reload_page)
 			
 			# Back Button
		self.back = QtWidgets.QPushButton('←',self)
		self.back.setMinimumSize(20, 20)
		self.back.setStyleSheet('font-size:23px;')
		self.back.clicked.connect(self.go_back)
 		
 			# Forward Button
		self.forward = QtWidgets.QPushButton('→',self)
		self.forward.setMinimumSize(20, 20)
		self.forward.setStyleSheet('font-size:23px;')
		self.forward.clicked.connect(self.go_forwardard)
 		
 			# Create Progress Bar
		self.pbar = QtWidgets.QProgressBar()
		self.pbar.setMaximumWidth(120)
 		
 			# Update Progress Bar, Window Title etc.
		self.web = QWebEngineView(loadProgress = self.pbar.setValue, loadFinished = self.pbar.hide, loadStarted = self.pbar.show, titleChanged = self.setWindowTitle)
		self.web.setMinimumSize(1200, 600)
 		
 			# Check for url changes
		self.web.urlChanged.connect(self.if_url_changed)
		
			# Check for user liink hovering
		self.web.page().linkHovered.connect(self.if_link_hover)
 		
 			# Set Grid
		grid = QtWidgets.QGridLayout()
 
 			# Set Widget Locations
		grid.addWidget(self.back,0,0, 1, 1)
		grid.addWidget(self.line,0,3, 1, 1)
		grid.addWidget(self.forward,0,1, 1, 1)
		grid.addWidget(self.reload,0,2, 1, 1)
		grid.addWidget(self.web, 2, 0, 1, 6)
 
		self.centralwidget.setLayout(grid)
 
		# Window Settings
 			# Default Window Size and Location
		self.setGeometry(25, 100, 1200, 600)
			# Window Title
		self.setWindowTitle('Browsey')
			# Window Icon
		self.setWindowIcon(QtGui.QIcon(''))
			# Window Colour
		self.setStyleSheet('background-color:')
			# Window Status Bar 
		self.status = self.statusBar()
		self.status.addPermanentWidget(self.pbar)
		self.status.hide()
 
		self.setCentralWidget(self.centralwidget)

 	# Function to Handle URLs
	def set_url(self):

		# Get default URL
		global url
		 
		url = self.line.text()

 		# Set URL Prefixes
		http = 'http://'
		www = 'www.'
		
		# Check and Set
		if www in url and http not in url:
			url = http + url			 
			 
		elif http in url and www not in url:
			url = url[:7] + www + url[7:]
			
		# If no suffix used make it a google search
		elif '.' not in url:
			url = 'http://www.google.com/search?q='+url
 
		elif http and www not in url:
			url = http + www + url
 
		self.line.setText(url)
 		
 		# Load site at URL
		self.web.load(QtCore.QUrl(url))

 		# Show URL
		self.status.show()

 	# Navigation functions
	def go_back(self):
		self.web.back()
		 
	def go_forwardard(self):
		self.web.forwardard()

	def reload_page(self):
		self.web.reload()

 	#Check if user has entered new URL
	def if_url_changed(self):
		self.line.setText(self.web.url().toString())

 	# Show link in statusbar if user hovers
	def if_link_hover(self, l):
		self.status.showMessage(l)
 
# The usual
def main():

	app = QtWidgets.QApplication(sys.argv)

	main = Main()
	main.show()
 
	sys.exit(app.exec_())
 
if __name__ == '__main__':
	main()