import sys
import time
import threading
import ConfigParser
from PyQt5.QtCore import QUrl, QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, QMetaObject, Q_ARG, Qt, QMetaType
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QMessageBox
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlApplicationEngine, QQmlEngine, QQmlComponent, qmlRegisterType
from json import dumps
import lpc
import serial.tools.list_ports

class MainApp(QObject):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.checkList = []
        self.devGlobal = ''
        self.config = ConfigParser.ConfigParser()
        self.config.read("cfg.ini")
        self.connection = None
        self.port_list = []
        for port in serial.tools.list_ports.comports():
            self.port_list.append(port[0])
        self.port_list.sort()


    @pyqtSlot(QVariant)
    def sendPortList(self):
        result = self.port_list
        obj = engine.rootObjects()
        myObject = obj[0].findChild(QObject, 'entryVal')
        QMetaObject.invokeMethod(myObject, "setPortList", Qt.DirectConnection, Q_ARG("QVariant", dumps(result)))
        return 0

    @pyqtSlot(QVariant)
    def error(self, errTitle, errText):
        send = [errTitle, errText]
        obj = engine.rootObjects()
        myObject = obj[0].findChild(QObject, 'message')
        QMetaObject.invokeMethod(myObject, "error", Qt.DirectConnection, Q_ARG("QVariant", dumps(send)))
        return 0

    @pyqtSlot(QVariant)
    def setStatus(self, status):
        obj = engine.rootObjects()
        myObject = obj[0].findChild(QObject, 'statusBar')
        QMetaObject.invokeMethod(myObject, "setStatus", Qt.DirectConnection, Q_ARG("QVariant", dumps(status)))
        return 0

    

    @pyqtSlot(QVariant)
    def printData(self, data):
        obj = engine.rootObjects()
        myObject = obj[0].findChild(QObject, 'dataColumn')
        QMetaObject.invokeMethod(myObject, "setData", Qt.DirectConnection, Q_ARG("QVariant", dumps(data)))
        return 0

    @pyqtSlot(QVariant)
    def showRegisters(self, regTab):
        obj = engine.rootObjects()
        myObject = obj[0].findChild(QObject, 'table')
        QMetaObject.invokeMethod(myObject, "showRegs", Qt.DirectConnection, Q_ARG("QVariant", dumps(regTab)))
        return 0

    def OnValidate(self, addr, maxN, entry):
        reg = 0
        try:
            if addr.startswith('0x'):
                reg = int(addr, 16)
                if reg > maxN:
                    return None   
            elif addr.startswith('0'):
                reg = int(addr, 8)
                if reg > maxN:
                    return None
            else:
                reg = int(addr)
                if reg > maxN:
                    return None
        except ValueError:
            return None
        return reg

    def checkReg(self):
        t = threading.Timer(1.0, self.checkReg)
        t.start()
        thread.append(t)
        dev_val = self.OnValidate(self.devGlobal, 127, 'device address')
        for row in self.checkList:   
            reg_val = int(self.config.get(self.config.sections()[row], 'address'))
            newData ={}
            newData['data'] = self.connection.read_cmd(dev_val, reg_val)
            newData['row'] = str(row)
            self.printData(newData)

    def liveChecking(self, dev, row):
        self.devGlobal = dev
        self.checkList.append(row)

    def notChecking(self, row):
        self.checkList.remove(row)

    def kill(self):
        for t in thread:
            t.cancel()
        self.checkList = []

    def disconnect(self):
        self.checkList = []
        self.connection = None
    
    def walk(self, dev_val):
        registers = {}
        i = 0
        for sect in self.config.sections():
            regDict = {}
            regDict['name'] = sect
            regDict['address'] = self.config.get(sect, 'address')
            if self.config.has_option(sect, 'readOnly'):
                regDict['readOnly'] = self.config.get(sect, 'readOnly')
            regAddr = self.OnValidate(self.config.get(sect, 'address'), 65535, 'register address')
            regDict['data'] = self.connection.read_cmd(dev_val, regAddr)
            registers[str(i)]=regDict
            i+=1
        registers['quantity'] = i
        self.showRegisters(registers)

    def actionMethod(self, dev, opt, port, speed, write, row):
        dev_val = self.OnValidate(dev, 127, 'device address')
        write_val = None
        if dev_val != None:
            if self.connection == None:
                try:    
                    self.connection = lpc.LPC(port, speed)
                    self.connection.enter_in_i2c_mode()
                except Exception as e:
                    self.error('Error', 'Connection problem. {}'.format(e))
                    self.setStatus('Not connected')
                    return
        else:
            self.error( 'Error', 'Invalid device address.')
            return
        if opt == 'write': # write
            try:
                write_val = self.OnValidate(write, 4294967295, 'write value')
                reg_val = int(self.config.get(self.config.sections()[row], 'address'))
                if write_val != None:
                    val = [(write_val >> 24) & 0xFF, (write_val >> 16) & 0xFF, (write_val >> 8) & 0xFF, write_val & 0xFF]
                    self.connection.write_cmd(dev_val, reg_val, val)
                else:
                    self.error('Error', 'Invalid write data')
                newData = {}
                newData['data'] = self.connection.read_cmd(dev_val, reg_val)
                newData['row'] = row
                self.printData(newData)
            except Exception as e:
                self.error('Error', 'Write problem. {}'.format(e))
        elif opt == 'walk': # upgrade
            self.walk(dev_val)
            self.setStatus('Connected')

# Main Function
if __name__ == '__main__':
    # Create main app
    qmlRegisterType(MainApp, "Charts", 1, 0, "MainApp")
    # qRegisterMetaType<QVector<int>>("QVector<int>");
    somesignal = pyqtSignal(QVariant)
    myApp = QApplication(sys.argv)
    engine = QQmlApplicationEngine(myApp)
    engine.load(QUrl.fromLocalFile('basic.qml'))
    mainApp = MainApp()
    mainApp.sendPortList()
    thread = []
    mainApp.checkReg()
    window = engine.rootObjects()[0]
    window.show()
    window.actionClicked.connect(mainApp.actionMethod)
    window.liveChecking.connect(mainApp.liveChecking)
    window.notChecking.connect(mainApp.notChecking)
    window.delConnection.connect(mainApp.disconnect)
    window.kill.connect(mainApp.kill)
    # Execute the Application and Exit
    myApp.exec_()
    sys.exit(mainApp.kill())