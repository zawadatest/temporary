import sys
from PyQt5.QtCore import QUrl, QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, QMetaObject, Q_ARG, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QMessageBox
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlApplicationEngine, QQmlEngine, QQmlComponent, qmlRegisterType
from json import dumps
import lpc
import serial.tools.list_ports

class MainApp(QObject):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.connection = None
        self.port_list = []
        for port in serial.tools.list_ports.comports():
            self.port_list.append(port[0])
        self.port_list.sort()


    @pyqtSlot(QVariant)
    def sendPortList(self, myengine):
        result = self.port_list
        obj = myengine.rootObjects()
        myObject = obj[0].findChild(QObject, 'entryVal')
        QMetaObject.invokeMethod(myObject, "setPortList", Qt.DirectConnection, Q_ARG("QVariant", dumps(result)))

        return 0

    @pyqtSlot(QVariant)
    def error(self, myengine, errTitle, errText):
        send = [errTitle, errText]
        obj = myengine.rootObjects()
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
        myObject = obj[0].findChild(QObject, 'textArea')
        QMetaObject.invokeMethod(myObject, "printData", Qt.DirectConnection, Q_ARG("QVariant", dumps(data)))
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

    def actionMethod(self, dev, reg, opt, port, speed, write):
        dev_val = self.OnValidate(dev, 127, 'device address')
        reg_val = self.OnValidate(reg, 65535, 'register address')
        write_val = None
        # opt = self..get()
        if dev_val != None:
            if reg_val != None:
                if self.connection == None:
                    try:    
                        self.connection = lpc.LPC(port, speed)
                        self.connection.enter_in_i2c_mode()

                    except Exception as e:
                        self.error(engine, 'Error', 'Connection problem. {}'.format(e))
                        self.setStatus('Not connected')
                        return
            else:
                self.error(engine, 'Error', 'Invalid register address.')
                return
        else:
            self.error(engine, 'Error', 'Invalid device address.')
            return
        if opt == 1: # read
            try:
                # data = self.connection.read_cmd(dev_val, reg_val)
                data = self.connection.walk(dev_val)
                self.setStatus('Connected')
                
                self.printData(str(data))

            except Exception as e:
                self.error(engine, 'Error', 'Read problem. {}'.format(e))
        
        elif opt == 2: # write
            try:
                write_val = self.OnValidate(write, 4294967295, 'write value')
                if write_val != None:
                    val = [(write_val >> 24) & 0xFF, (write_val >> 16) & 0xFF, (write_val >> 8) & 0xFF, write_val & 0xFF]
                    self.connection.write_cmd(dev_val, reg_val, val)
                else:
                    self.error(engine, 'Error', 'Invalid write data')
            except Exception as e:
                self.error(engine, 'Error', 'Write problem. {}'.format(e))

        elif opt == 3: # upgrade
            print opt


# Main Function
if __name__ == '__main__':
    # Create main app
    qmlRegisterType(MainApp, "Charts", 1, 0, "MainApp")
    myApp = QApplication(sys.argv)
    engine = QQmlApplicationEngine(myApp)
    engine.load(QUrl.fromLocalFile('basic.qml'))
    x = MainApp()
    x.sendPortList(engine)
    ctx = engine.rootContext()
    ctx.setContextProperty("mainAppPy", engine)
    window = engine.rootObjects()[0]
    def mouse_clicked():
        print 'mouse clicked'
    def mouse_clicked3(x):
        print x
    window.show()
    window.clicked.connect(mouse_clicked)
    window.clicked2.connect(mouse_clicked)
    window.clicked3.connect(mouse_clicked3)
    window.actionClicked.connect(x.actionMethod)
    # Execute the Application and Exit
    myApp.exec_()
    sys.exit()