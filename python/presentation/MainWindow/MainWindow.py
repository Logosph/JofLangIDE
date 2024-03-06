from PyQt6.QtGui import QCursor, QScreen

from resources.layout.python.window_main import *
import sys



applicationElementWidth = 10
applicationElementHeight = 10
ui = Ui_MainWindow()

def execute():
    global ui

    blocksArray = [[[0, "SomeCode0", "LinkToIllustration"], [1, "SomeCode0", "LinkToIllustration"], [0, "SomeCode0", "LinkToIllustration"], [1, "SomeCode0", "LinkToIllustration"]],
                    [[0, "SomeCode1", "LinkToIllustration"], [1, "SomeCode1", "LinkToIllustration"]],
                    [[0, "SomeCode2", "LinkToIllustration"], [1, "SomeCode2", "LinkToIllustration"]],
                    [[0, "SomeCode3", "LinkToIllustration"], [1, "SomeCode3", "LinkToIllustration"]],
                    [[0, "SomeCode4", "LinkToIllustration"], [1, "SomeCode4", "LinkToIllustration"]],
                    [[0, "SomeCode5", "LinkToIllustration"], [1, "SomeCode5", "LinkToIllustration"]]]
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    ui.VariablesCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 0, 0))
    ui.OperationsCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 1, 0))
    ui.ControlCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 2, 0))
    ui.Control2CategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 3, 0))
    ui.SchemaCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 4, 0))
    ui.SpecialCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 5, 0))
    formatBlocksToCategory(ui, blocksArray,0,0)
    MainWindow.show()
    sys.exit(app.exec())


grabber = False
class BlockForField(QLabel):
    def __init__(self,ui):
        super().__init__()
        self.setText("goyda")
        self.setStyleSheet("background-color: rgb(100, 55, 55);")
    def mousePressEvent(self, event):
        global grabber
        grabber = True
        print("Pressed")

    def mouseMoveEvent(self, ev):
        global grabber, ui

        if grabber:
            self.setGeometry(QCursor.pos().x() - 275, QCursor.pos().y() - 150, 100, 100)

    def mouseReleaseEvent(self, ev):
        global grabber
        grabber = False
        print("Released")

    def mouseDoubleClickEvent(self, a0):
        self.deleteLater()


class BlockLabel(QPushButton):
    def __init__(self, BlockName, ui):
        super().__init__()
        self.setText(BlockName)
        self.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.setGeometry(300, 300, 300, 300)
        self.clicked.connect(lambda: self.justAClicked(ui))
    def justAClicked(self, ui):
        print("goyda")
        ui.scrollAreaWidgetContents.label = BlockForField(ui)
        ui.scrollAreaWidgetContents.label.setGeometry(0, 0, 100, 100)
        ui.scrollAreaWidgetContents.label.setParent(ui.scrollAreaWidgetContents)
        ui.scrollAreaWidgetContents.label.show()


def formatBlocksToCategory(ui, blocksArray, categoryNumber, blocknumber):

    match categoryNumber:
        case 0:
            ui.categoryName.setText("Переменные")
        case 1:
            ui.categoryName.setText("Операторы")
        case 2:
            ui.categoryName.setText("Контроль")
        case 3:
            ui.categoryName.setText("Контроль_2")
        case 4:
            ui.categoryName.setText("Схема")
        case 5:
            ui.categoryName.setText("Особенные")

    print(blocksArray[categoryNumber][blocknumber][1])
    countOfBlocks = ui.scrollAreaWidgetContents_2.findChildren(QLabel)
    for i in countOfBlocks:
        i.deleteLater()
        i.widget_name = None

    countOfBlocks = ui.scrollAreaWidgetContents_2.findChildren(QPushButton)
    for i in countOfBlocks:
        i.deleteLater()
        i.widget_name = None

    for i in range(len(blocksArray[categoryNumber])):
        blockName = "Object" + str(i)
        ui.verticalLayout_6.addWidget(BlockLabel(blockName, ui))



if __name__ == "__main__":
    execute()
