import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Window 2.0
import QtQuick.Dialogs 1.2
import Charts 1.0


				    MouseArea {
	                id: cellMouseArea
	                anchors.fill: parent
	                onClicked: {
	                    // Column index are zero based
	                    if(styleData.column === 4){
	                    	if(libraryModel.get(styleData.row).readOnly == 'false'){
		                        loader.visible = true
	    	                    loader.item.forceActiveFocus()
		                    }
	                    }
	                }
			    }



DelegateOne {
	TextField {
	        	//style: model.get(styleData.row)[styleData.role]
	        	visible: (libraryModel.get(styleData.row).readOnly == 'false') ? true : false
			    Text {
			        id: textItem
			        text: styleData.value
			        visible: true
			    }
			    Loader {
			        id: loader
			        anchors { verticalCenter: parent.verticalCenter; left: parent.left}
	                height: parent.height
	                width: parent.width
	                visible: false
	                sourceComponent: visible ? input : undefined
	                Component {
	                    id: input
	                    TextField {
	                        anchors { fill: parent }
	                        text: styleData.value
	                        
	                        onAccepted:{
	                            // DO STUFF
	                            rootRect.actionClicked(devE.text, regE.text, opt, portBox.currentText, speedBox.currentText, text, tableV.currentRow)
	                            loader.visible = false
	                        }

	                        onActiveFocusChanged: {
	                            if (!activeFocus) {
	                                loader.visible = false

	                            }
	                        }
	                    }
	                }
			    }
			    MouseArea {
	                id: cellMouseArea
	                anchors.fill: parent
	                onClicked: {
	                    // Column index are zero based
	                    if(styleData.column === 4){
	                    	if(libraryModel.get(styleData.row).readOnly == 'false'){
		                        loader.visible = true
	    	                    loader.item.forceActiveFocus()
		                    }
	                    }
	                }
	            }
		    }
}