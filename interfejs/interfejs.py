import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPlainTextEdit, QGroupBox, QRadioButton, QHBoxLayout, QCheckBox, QMainWindow, QLabel, QGridLayout, QWidget, QComboBox, QDesktopWidget, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QSize, QRect   
from PyQt5.QtGui import *
import lpc
import serial.tools.list_ports
     
class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.connection = None
        self.port_list = []
        for port in serial.tools.list_ports.comports():
            self.port_list.append(port[0])
        self.port_list.sort()
        self.initUI()

    def OnValidate(self, addr, maxN, entry):
        reg = 0
        try:
            if addr.startswith('0x'):
                reg = int(addr, 16)
                if reg > maxN:
                	QMessageBox.about(self, 'Error', 'Invalid {}.'.format(entry))
                    # tkMessageBox.showerror('Error', 'Invalid {}.'.format(entry))
                    return None   
            elif addr.startswith('0'):
                reg = int(addr, 8)
                if reg > maxN:
                	QMessageBox.about(self, 'Error', 'Invalid {}.'.format(entry))
                    # tkMessageBox.showerror('Error', 'Invalid {}.'.format(entry))
                    return False
            else:
                reg = int(addr)
                if reg > maxN:
                	QMessageBox.about(self, 'Error', 'Invalid {}.'.format(entry))
                    # tkMessageBox.showerror('Error', 'Invalid {}.'.format(entry))
                    return False
        except ValueError:
        	QMessageBox.about(self, 'Error', 'Invalid {}.'.format(entry))
            # tkMessageBox.showerror('Error', 'Invalid {}.'.format(entry))
            return False
        return reg

    def initUI(self):
        self.setMinimumSize(QSize(420, 480))    
        self.setWindowTitle("LPC") 
        
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)  

        # set in center of screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # gridLayout = QGridLayout(self)     
        # gridLayout.addWidget(self.createExampleGroup())
        # centralWidget.setLayout(gridLayout)
        # normal label in center
        self.devLabel = QLabel(self)
        self.devLabel.setText('Device address:')
        self.devLabel.resize(150,30)
        self.devLabel.move(20, 20)
        # entry textfield
        self.devLine = QLineEdit(self)
        self.devLine.move(150, 20)
        self.devLine.resize(260, 32)

        self.regLabel = QLabel(self)
        self.regLabel.setText('Register address:')
        self.regLabel.resize(150, 30)
        self.regLabel.move(20, 60)
        # entry textfield
        self.regLine = QLineEdit(self)
        self.regLine.move(150, 60)
        self.regLine.resize(260, 32)

        self.statusBar().showMessage('Not connected.')        
        # some label
        # title = QLabel("Hello World from PyQt", self) 
        # title.setAlignment(QtCore.Qt.AlignCenter) 
        # gridLayout.addWidget(title, 0, 0)

        self.speedLabel = QLabel(self)
        self.speedLabel.setText('Speed:')
        self.speedLabel.resize(150,30)
        self.speedLabel.move(20, 100)

        # Create combobox and add items.
        self.comboBox = QComboBox(centralWidget)
        self.comboBox.setGeometry(QRect(40, 40, 91, 31))
        self.comboBox.move(150, 100)
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.addItem("5")
        self.comboBox.addItem("50")
        self.comboBox.addItem("100")
        self.comboBox.addItem("400")

        self.speedLabel = QLabel(self)
        self.speedLabel.setText('Connect to:')
        self.speedLabel.resize(150,30)
        self.speedLabel.move(20, 140)

        self.portBox = QComboBox(centralWidget)
        self.portBox.setGeometry(QRect(40, 40, 191, 31))
        self.portBox.move(150, 140)
        self.portBox.setObjectName(("comboBox"))
        for i in self.port_list:
        	self.portBox.addItem(str(i))

        self.radio1 = QRadioButton("Read", self)
        self.radio1.move(20, 170)
        self.radio2 = QRadioButton("Write", self)
        self.radio2.move(100, 170)
        self.radio3 = QRadioButton("Upgrade", self)
        self.radio3.move(180, 170)
 
        self.radio1.setChecked(True)

        # add text field
        self.b = QPlainTextEdit(self)
        self.b.insertPlainText("You can write data here.\n")
        self.b.move(10,200)
        self.b.resize(400,200)

        # button action
        pybutton = QPushButton('Action', self)
        pybutton.resize(100, 32)
        pybutton.move(200, 420)        
        pybutton.clicked.connect(self.actionMethod)

        # button quit
        pybutton = QPushButton('Quit', self)
        pybutton.resize(100, 32)
        pybutton.move(310, 420)        
        pybutton.clicked.connect(self.actionMethod)


    def createExampleGroup(self):
        groupBox = QGroupBox("Best Food")

        radio1 = QRadioButton("&Radio pizza")
        radio2 = QRadioButton("R&adio taco")
        radio3 = QRadioButton("Ra&dio burrito")
 
        radio1.setChecked(True)
 
        vbox = QHBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox) 
        return groupBox

    def actionMethod(self):
    	dev_val = self.OnValidate(self.devLine.text(), 127, 'device address')
        reg_val = self.OnValidate(self.regLine.text(), 65535, 'register address')
        write_val = None
        # opt = self..get()
        if dev_val != None and reg_val != None:           
            # try:
            if self.connection == None:
                tkMessageBox.showerror('Error', 'sdfsdf')
            if opt == 1: #write
                write_val = self.OnValidate(self.writeEntry.get(), 4294967295, 'write value')
                val = [(write_val >> 24) & 0xFF, (write_val >> 16) & 0xFF, (write_val >> 8) & 0xFF, write_val & 0xFF]
                self.connection.write_cmd(dev_val, reg_val, val)
            elif opt == 2: #read                        
                data = self.connection.read_cmd(dev_val, reg_val)
                t.set(str(data))
            elif opt == 3: #upgrade
                return  
            # except Exception:
            #     tkMessageBox.showerror('Error', 'Action problem')
            #     return
        print('Clicked Pyqt button.')
        QMessageBox.about(self, "Title", "Message")
        print('Your name: ' + self.devLine.text())
 
 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit( app.exec_() )