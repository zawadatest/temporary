import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Window 2.0
import Charts 1.0

ApplicationWindow {
	id: rootRect
    signal clicked()
    signal clicked2()
    signal clicked3(string text)
    visible: true
    x: Screen.width / 2 - width / 2
    y: Screen.height / 2 - height / 2
    width: 480
    height: 480
    property var portArray: []
    statusBar: StatusBar {
        Row {
            anchors.fill: parent
            Label { id: status; text: "Read Only" }
        }
    }
	Text {
		objectName: "hello"
		function myTest1(x){
            console.log("result 1 is : ", x)
            rootRect.portArray = JSON.parse(x)
        }
        id: hello
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        text: "LPC app"
        font.family: "Helvetica"
        font.pointSize: 14
        horizontalAlignment: Text.AlignHCenter
    }
    Grid {	
    	id: entryValues
        anchors.left: parent.left
        anchors.leftMargin: 20
        anchors.top: hello.bottom
        anchors.topMargin: 20

        rows: 4; columns: 2; spacing: 5

        Text {
	        id: devLabel
	        width: 150
	        text: "Device address:"
	        font.family: "Helvetica"
	        font.pointSize: 10
    	}
        TextField {
        	id: devE
        	width: 200
    		placeholderText: qsTr("Enter name")
		}
		Text {
	        id: regLabel
	        width: 150
	        text: "Register address:"
	        font.family: "Helvetica"
	        font.pointSize: 10
    	}
    	TextField {
        	id: regE
        	width: 200
    		placeholderText: qsTr("Enter register address")
		}
        Text {
	        id: speedLabel
	        width: 150
	        text: "Speed:"
	        font.family: "Helvetica"
	        font.pointSize: 10
    	}
    	ComboBox {
    		id: speedBox
		    width: 200
		    model: [ 5, 50, 100, 400 ]
		}
        Text {
	        id: portLabel
	        width: 150
	        text: "Port:"
	        font.family: "Helvetica"
	        font.pointSize: 10
    	}
    	ComboBox {
    		id: portBox
		    width: 200
		    model: rootRect.portArray
		}
    }
    ExclusiveGroup { id: group
    	anchors.bottom: parent.bottom }
	Row {
	    id: row
	    RadioButton {
	        id: button1
	        text: "1"
	        exclusiveGroup: group
	    }
	    RadioButton {
	        id: button2
	        text: "2"
	        exclusiveGroup: group
	    }
	    RadioButton {
	        id: button3
	        text: "3"
	        exclusiveGroup: group
	        checked: true
	    }
	}
	Button {
		id: quit
		text: "Quit"
		anchors.right: parent.right
		anchors.bottom: parent.bottom
		anchors.rightMargin: 5
		anchors.bottomMargin: 5
		MouseArea {
    	    anchors.fill: parent
        	onClicked: status.text = "nowy"
		}
	}
	Button {
		id: action
		text: "Action"
		anchors.right: quit.left
		anchors.bottom: quit.bottom
		MouseArea {
    	    anchors.fill: parent
        	onClicked: rootRect.clicked3(devE.text)
		}
	}
	
}