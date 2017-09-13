import sys
from PyQt5.QtCore import QUrl, QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, QMetaObject, Q_ARG, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
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
    def funct1(self, myengine):

        result = self.port_list

        obj = myengine.rootObjects()
        myObject = obj[0].findChild(QObject, 'hello')
        QMetaObject.invokeMethod(myObject, "myTest1", Qt.DirectConnection, Q_ARG("QVariant", dumps(result)))

        return 0

class Window(QMainWindow):
    def __init__(self):
        QMainWindowglobal.__init__(self)
        self.connection = None
        self.port_list = []
        for port in serial.tools.list_ports.comports():
            self.port_list.append(port[0])
        self.port_list.sort()
        self.initUI()


# Main Function
if __name__ == '__main__':
    # Create main app
    qmlRegisterType(MainApp, "Charts", 1, 0, "MainApp")
    myApp = QApplication(sys.argv)
    engine = QQmlApplicationEngine(myApp)
    # engine.rootContext().setContextProperty('store', store)
    engine.load(QUrl.fromLocalFile('basic.qml'))
    x = MainApp()
    x.funct1(engine)
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
    # Execute the Application and Exit
    myApp.exec_()
    sys.exit()