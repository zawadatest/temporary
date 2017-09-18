import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Window 2.0
import QtQuick.Dialogs 1.2
import Charts 1.0

ApplicationWindow {
	id: rootRect
    signal clicked()
    signal clicked2()
    signal clicked3(string text)
    signal actionClicked(string dev, string reg, int opt, string port, string speed, string write, int row)
    visible: true
    x: Screen.width / 2 - width / 2
    y: Screen.height / 2 - height / 2
    width: 480
    height: 480
    property var portArray: []
    property int opt: (read.checked == true) ? 1 : ((write.checked == true) ? 2 : ((walk.checked == true) ? 3 : 4)) 
    statusBar: StatusBar {
    	objectName: "statusBar"
    	function setStatus(statusString){
    		status.text = JSON.parse(statusString)
    	}
        Row {
            anchors.fill: parent
            Label { id: status; text: "Not connected" }
        }
    }
	Text {
		objectName: "hello"
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
    	objectName: "entryVal"
    	function setPortList(x){
        	rootRect.portArray = JSON.parse(x)
    	}
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
        	text: '0x5a'
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
        	text: '0'
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
    ExclusiveGroup { id: group }
	Row {
		anchors.top: entryValues.bottom
		anchors.topMargin: 10
		anchors.left: parent.left
		anchors.right: parent.right
        anchors.leftMargin: 20
        spacing: 5
	    id: radioButtons
	    RadioButton {
	        id: read
	        text: "Read"
	        exclusiveGroup: group
	        checked: true
	    }
	    RadioButton {
	        id: write
	        text: "Write"
	        exclusiveGroup: group
	    }
	    RadioButton {
	        id: walk
	        text: "Walk"
	        exclusiveGroup: group
	    }
	    RadioButton {
	        id: upgrade
	        text: "Upgrade"
	        exclusiveGroup: group
	    }
	    Button {
			id: browse
			text: "Browse"
			MouseArea {
	    	    anchors.fill: parent
	        	onClicked: fileDialog.open()
			}
		}
	}
    Row {
    	id: apearWrite
		anchors.top: radioButtons.bottom
		anchors.topMargin: 10
		anchors.left: parent.left
		anchors.leftMargin: 20
		visible: (tableV.currentRow > -1) ? true : false
    	Text {
    		id: writeLabel
    		font.family: "Helvetica"
    		font.pointSize: 10
    		text:"Write data:"
    	}
    	TextField {
        	id: writeE
        	anchors.verticalCenter: writeLabel.verticalCenter
        	width: 200
    		placeholderText: qsTr("Enter write data")
		}
	}
	Row {
		id: apearFilepath
		anchors.top: apearWrite.bottom
		anchors.topMargin: 10
		anchors.left: parent.left
		anchors.leftMargin: 20
		visible: false	
		Text {
			id: filepathLabel
	        width: 150
	        text: "Filepath:"
	        font.family: "Helvetica"
	        font.pointSize: 10
    	}
    	Text {
			id: filepathValue
	        width: 150
	        font.family: "Helvetica"
	        font.pointSize: 10
    	}
	}
	TextArea {
		objectName: "textArea"
		function printData(data){
			text = JSON.parse(data)
		}
	    id: txtArea
	    width: parent.width-10
	    anchors.top: apearFilepath.bottom
	    anchors.horizontalCenter: parent.horizontalCenter
	    anchors.bottom: quit.top
	    visible: (tableV.visible == true) ? false : true
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
        	onClicked: rootRect.close()
		}
	}
	Button {
		id: action
		text: "Action"
		anchors.right: quit.left
		anchors.bottom: quit.bottom
		MouseArea {
    	    anchors.fill: parent
        	onClicked: rootRect.actionClicked(devE.text, regE.text, opt, portBox.currentText, speedBox.currentText, writeE.text, tableV.currentRow)
		}
	}

	MessageDialog {
		objectName: "message"
		function error(x){
        	title = JSON.parse(x)[0]
        	text = JSON.parse(x)[1]
        	visible = true
    	}
		visible: false
	    id: messageDialog
	    Component.onCompleted: visible = false
	}
	FileDialog {
	    id: fileDialog
	    title: "Please choose a file"
	    onAccepted: {
	        filepathValue.text = fileDialog.fileUrl
	        apearFilepath.visible = true
	    }
	    onRejected: {
	        console.log("Canceled")
	    }
	}
	ListModel {
	    id: libraryModel
	    
	}
	TableView {
		id: tableV
		objectName: "table"
		function printWalk(data){
	    	var dat = JSON.parse(data)
    		console.log(dat)
    		console.log(dat.length)
    		var i = 0	  
    		for(i=0; i<dat.length; i++){
    			libraryModel.append({regN:i, data:dat[i]})
    		}  		
	    	
		} 
		function showRegs(regTab){
			var rT = JSON.parse(regTab)
			var i = 0
			var w = rT['0'];
			for(i = 0; i<rT.quantity; i++){
				var tmp = rT[i.toString()]
				if(libraryModel.count < i+1){
					libraryModel.append({regN:tmp.name, address: tmp.address, data: tmp.data})
				}else{
					libraryModel.setProperty(i, "data", tmp.data)
				}
				
			}
		}
		width: parent.width-10
		anchors.top: apearFilepath.bottom
	    anchors.horizontalCenter: parent.horizontalCenter
	    anchors.bottom: quit.top
	    visible: (walk.checked == true) ? true : false
	    TableViewColumn {
	    	role: "regN"
	        title: "Register"
	        width: 100
	    }
	    TableViewColumn {
	    	role: "address"
	        title: "Address"
	        width: 200
	    }
	    TableViewColumn {
	    	role: "data"
	        title: "Data"
	        width: 200
	    }
	    model: libraryModel
	     
	}
}