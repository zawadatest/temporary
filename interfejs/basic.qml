import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Window 2.0
import QtQuick.Dialogs 1.2
import Charts 1.0

ApplicationWindow {
	id: rootRect
    signal actionClicked(string dev, string opt, string port, string speed, string toWrite, int row)
    signal liveChecking(string dev, int row)
    signal notChecking(int row)
    signal kill()
    signal delConnection()
    //signal startCl()
    visible: true
    x: Screen.width / 2 - width / 2
    y: Screen.height / 2 - height / 2
    width: 480
    height: 480
    property var portArray: []
    property int opt: 4
    property bool writing: false
    //property string tmpstr: ""

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
        	onClicked: {
	        	rootRect.delConnection();
	        	rootRect.kill(); 
	        	rootRect.close()
        	}
		}
	}

	Button {
		id: action
		objectName: "action"
		text: "Connect"
		anchors.right: quit.left
		anchors.bottom: quit.bottom
		MouseArea {
    	    anchors.fill: parent
        	onClicked: {
        		if(action.text == "Connect"){
        			rootRect.actionClicked(devE.text, "walk", portBox.currentText, speedBox.currentText, "", tableV.currentRow)
        			action.text = "Disconnect"
        		}else{
        			//rootRect.kill()
        			rootRect.delConnection()

        			if(libraryModel.count){
        				libraryModel.clear()
        			}
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

	ListModel {
	    id: libraryModel
	}

	Component {
		id: emptyComponent
		Text{}
	}

	TableView {
		id: tableV
		objectName: "table"
		width: parent.width-10
		anchors.top: entryValues.bottom
	    anchors.horizontalCenter: parent.horizontalCenter
	    anchors.bottom: quit.top
	    visible: true

		function showRegs(regTab){
			var rT = JSON.parse(regTab)
			var i = 0
			var w = rT['0'];
			for(i = 0; i<rT.quantity; i++){
				var tmp = rT[i.toString()]
				if(libraryModel.count < i+1){
					libraryModel.append({regN: tmp.name, address: tmp.address, readOnly: tmp.readOnly ? tmp.readOnly : 'false', data: parseInt(tmp.data)})
				}else{
					libraryModel.setProperty(i, "data", parseInt(tmp.data))
				}
				
			}
		}
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
            				console.log(styleData.row)
            				liveChecking(devE.text, styleData.row)
            				console.log(styleData.row)
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
	    	id: dataColumn
	    	objectName: "dataColumn"
	    	role: "data"
	        title: "Data"
	        width: tableV.width/4
	    	function setData(newData){
	    		console.log(newData)
	    		var temp = JSON.parse(newData)
	    		console.log(temp.data)
	    		console.log("sldjflksjdf")
	    		console.log(temp.row)
	    		if(libraryModel.count){
	    			console.log(libraryModel.get(temp.row).data)
	    			var tttt = String(temp.data)
	    			console.log('czy tu')
	    			libraryModel.setProperty(temp.row, "data", parseInt(temp.data))
	    			//libraryModel.get(temp.row).data = temp.data
	    			//libraryModel.get(1).data = '12'
    				console.log("tu dupa")
    			}
    		}
	        delegate: Component {	        	
			    Loader {
			        id: loader
			        anchors { verticalCenter: parent ? parent.verticalCenter : undefined; left: parent ? parent.left : undefined}
	                height: parent ? parent.height : undefined
	                width: parent ? parent.width : undefined
	                visible: true
	                sourceComponent: (libraryModel.count) ? ((libraryModel.get(styleData.row).readOnly == 'true') ? textItem : inputDelegate) : undefined 
	                Component {
	                    id: inputDelegate
	                    TextField {
	                    	id: input
	                    	property int opt: styleData.row
	                    	style: Component{Text{}   }
	                        text: styleData.value
	                        visible: true
	                        focus: writing
	                        onAccepted:{
	                            rootRect.actionClicked(devE.text, "write", portBox.currentText, speedBox.currentText, text, tableV.currentRow)
	                            text = styleData.value
	                            writing = false	
	                        }
	                        MouseArea{
        						anchors.fill: parent
        						onClicked: {
        							writing = true
        							tableV.selection.forEach(function(rowIndex){tableV.selection.deselect(rowIndex)})
        							tableV.selection.select(styleData.row)
        							if(writing){
	        							input.forceActiveFocus()
        							}
        						}
        					}
	                    }
	                }
	                Component {
		                id: textItem
		                Text {
		                	id: txt
					    	style: Component{Text{font.weight: Font.Black}   }
        					MouseArea{
        						anchors.fill: parent
        						onClicked: {
        							tableV.selection.forEach(function(rowIndex){tableV.selection.deselect(rowIndex)})
        							tableV.selection.select(styleData.row)
    								writing = false
        						}
        					}
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