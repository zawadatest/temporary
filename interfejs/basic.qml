import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Window 2.0
import QtQuick.Dialogs 1.2
import Charts 1.0

ApplicationWindow {
	id: rootRect
    signal actionClicked(string dev, int opt, string port, string speed, string write, int row)
    signal liveChecking(string dev, int row)
    signal notChecking(int row)
    signal kill()
    visible: true
    x: Screen.width / 2 - width / 2
    y: Screen.height / 2 - height / 2
    width: 480
    height: 480
    property var portArray: []
    property int opt: 4
    property string tmpstr: ""
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
		}/*
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
		}*/
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
    
	Button {
		id: quit
		text: "Quit"
		anchors.right: parent.right
		anchors.bottom: parent.bottom
		anchors.rightMargin: 5
		anchors.bottomMargin: 5
		MouseArea {
    	    anchors.fill: parent    	    
        	onClicked: {rootRect.kill(); rootRect.close()}
		}
	}
	Button {
		id: action
		text: "Connect"
		anchors.right: quit.left
		anchors.bottom: quit.bottom
		MouseArea {
    	    anchors.fill: parent
        	onClicked: {
        		rootRect.actionClicked(devE.text, 4, portBox.currentText, speedBox.currentText, tmpstr, tableV.currentRow)
        		if(action.text == "Connect"){
        			action.text = "Disconnect"
        		}else{
        			action.text = "Connect"
        		}
    		}
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
		function showRegs(regTab){
			var rT = JSON.parse(regTab)
			var i = 0
			var w = rT['0'];
			for(i = 0; i<rT.quantity; i++){
				var tmp = rT[i.toString()]
				if(libraryModel.count < i+1){
					libraryModel.append({regN: tmp.name, address: tmp.address, readOnly: tmp.readOnly ? tmp.readOnly : 'false', data: tmp.data})
				}else{
					libraryModel.setProperty(i, "data", tmp.data)
				}
				
			}
		}
		width: parent.width-10
		anchors.top: entryValues.bottom
	    anchors.horizontalCenter: parent.horizontalCenter
	    anchors.bottom: quit.top
	    visible: true
	    TableViewColumn {
            id: checkedCol
            role:  "checked"
            title: "Live check"
            width: tableV.width / 6
            delegate: Item {
            	anchors.fill: parent
            	CheckBox{
            		id: liveCheck
            		anchors.centerIn: parent
            		enabled: true
            		onClicked: {
            			if(checked == true){
            				liveChecking(devE.text, styleData.row)
            			}else{
            				notChecking(styleData.row)
            			}
            		}
				}
            }
        }
	    TableViewColumn {
	    	role: "regN"
	        title: "Register"
	        width: tableV.width/4
	    }
	    TableViewColumn {
	    	role: "address"
	        title: "Address"
	        width: tableV.width/6
	    }
	    TableViewColumn {
	    	role: "readOnly"
	    	title: "Read-Only"
	    	width: tableV.width/6
	    }
	    TableViewColumn {
	    	objectName: "dataColumn"
	    	function setData(newData){
	    		var temp = JSON.parse(newData)
    			libraryModel.get(temp.row).data = temp.data
    		}
	    	role: "data"
	        title: "Data"
	        width: tableV.width/4
	        delegate:  Component {	        	
			    Loader {
			        id: loader
			        anchors { verticalCenter: parent.verticalCenter; left: parent.left}
	                height: parent.height
	                width: parent.width
	                visible: true

	                sourceComponent: (libraryModel.get(styleData.row).readOnly == 'true') ? textItem : input
	                Component {
	                    id: input
	                    TextField {
	                    	
	                    	id: inpt
	                    	style: Component{Text{}   }
	                        anchors { fill: parent }
	                        text: styleData.value
	                        
	                        onAccepted:{
	                            // DO STUFF
	                            inpt.focus =  false	
	                            rootRect.actionClicked(devE.text, 2, portBox.currentText, speedBox.currentText, text, tableV.currentRow)	                            
	                            //loader.visible = false
	                        }

	                        onActiveFocusChanged: {
	                            if (!activeFocus) {
	                            }
	                        }
	                    }
	                }
	                Component {
		                id: textItem
		                TextField {
		                	id: txt
					    	style: Component{Text{}   }
					        text: styleData.value
					        visible: true
				    	
				    	}
			    	}
	            }
		    } 
	    }
	    model: libraryModel	    
	    	    
	}
}