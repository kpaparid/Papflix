import QtQuick 2.13
import QtQuick.Window 2.13

Window {
    title: qsTr("Hello World")
    width: 1000
    height: 800
    color: "#1557af"
    visible: true
    Item {
    ListView {
        id: listView
        x: 522
        y: 332
        width: 281
        height: 243
        pixelAligned: false
        model: ListModel {
            ListElement {
                name: "Grey"
                colorCode: "grey"
            }

            ListElement {
                name: "Red"
                colorCode: "red"
            }
        }
        delegate: Item {
            x: 5
            width: 80
            height: 40
            Row {

                Rectangle {
                    id: rectangle
                    width: 150
                    height: 150
                    color: "#ffffff"
                    anchors.fill: parent

                    Image {
                        id: poster
                        layer.wrapMode: ShaderEffectSource.ClampToEdge
                        layer.enabled: false
                        clip: false
                        anchors.fill: parent
                        fillMode: Image.Stretch
                        source: "https://image.tmdb.org/t/p/w600_and_h900_bestv2/p3pHw85UMZPegfMZBA6dZ06yarm.jpg"

                        Text {
                            id: movie
                            color: "#d00909"
                            //text: qsTr("Movie Title")
                            text: "joker"

                            transformOrigin: Item.Center
                            anchors.fill: parent
                            font.family: "Tahoma"
                            textFormat: Text.PlainText
                            wrapMode: Text.NoWrap
                            font.pixelSize: 40
                        }
                        Text {
                            id: movie2
                            color: "#d00909"
                            text: "joker2"
                        }


                    }

                    MouseArea {
                        id: mouseArea
                        x: 0
                        y: 0
                        anchors.rightMargin: 0
                        anchors.bottomMargin: 0
                        anchors.leftMargin: 0
                        anchors.topMargin: 0
                        anchors.fill: parent

                        Connections {
                            target: mouseArea
                            function onClicked(){

                                MyApp.onClick("text")
                            }
                        }

                    }
                    Connections {
                        target: MyApp
                        function onMovie(text) {
                            // textLabel - was given through arguments=['textLabel']
                            movie.text = text
                        }
                        function onPoster(source){
                            poster.source = source
                        }
                    }
                }








            }
        }
    }

}
}
