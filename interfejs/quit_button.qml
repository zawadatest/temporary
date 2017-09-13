import QtQuick 2.5
import QtQuick.Controls 1.4

ApplicationWindow {

    width: 300
    height: 200
    title: "Quit button"

    Button {
        x: 20
        y: 20
        text: "Quit"
        onClicked: Qt.quit()
    }
}