from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QPushButton, QRubberBand, QLabel

from resources.layout.python.window_main import *
import sys


stylesheet = ""
applicationElementWidth = 10
applicationElementHeight = 10
ui = Ui_MainWindow()
widthFix = 0
ElementsHeight = 0
ElementsWidth = 0
blocksInfo = [[0, 0, "init0"]]
blocksCurrentCout = 0
lastDraggedBlockName = "init"
lastDraggedBlockX = 0
lastDraggedBlockY = 0
globalMainWindow = 0

extraHeight = 0
extraWidth = 0
globalJofLangLogo = None
globalBlockList = None
globalBlockConstructor = None





def execute():
    global ui, widthFix, globalMainWindow, globalJofLangLogo, globalBlockList, globalBlockConstructor

    blocksArray = [[[0, "SomeCode0", "LinkToIllustration"], [1, "SomeCode0", "LinkToIllustration"], [0, "SomeCode0", "LinkToIllustration"], [1, "SomeCode0", "LinkToIllustration"]],
                    [[0, "SomeCode1", "LinkToIllustration"], [1, "SomeCode1", "LinkToIllustration"]],
                    [[0, "SomeCode2", "LinkToIllustration"], [1, "SomeCode2", "LinkToIllustration"]],
                    [[0, "SomeCode3", "LinkToIllustration"], [1, "SomeCode3", "LinkToIllustration"]],
                    [[0, "SomeCode4", "LinkToIllustration"], [1, "SomeCode4", "LinkToIllustration"]],
                    [[0, "SomeCode5", "LinkToIllustration"], [1, "SomeCode5", "LinkToIllustration"]]]

    app = QtWidgets.QApplication(sys.argv)
    globalMainWindow = MainWindowC()
    ui.setupUi(globalMainWindow)
    globalJofLangLogo = ui.JofLangLogo
    globalBlockList = ui.block_list
    globalBlockConstructor = ui.block_constructor
    ui.block_constructor.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, ui.block_constructor)
    ui.block_constructor.rubberBand.origin = None
    widthFix = ui.tableView_6.width() + ui.scrollArea_2.width()
    ui.VariablesCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 0, 0))
    ui.OperationsCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 1, 0))
    ui.ControlCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 2, 0))
    ui.Control2CategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 3, 0))
    ui.SchemaCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 4, 0))
    ui.SpecialCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, blocksArray, 5, 0))
    formatBlocksToCategory(ui, blocksArray,0,0)
    globalMainWindow.show()

    sys.exit(app.exec())


grabber = False
consist = False
freeX = 0
class BlockForField(QLabel):

    def __init__(self, ui):
        global stylesheet, blocksCurrentCout, lastDraggedBlockX,\
            lastDraggedBlockY, lastDraggedBlockName, blocksInfo, consist

        super().__init__()

        lastDraggedBlockX = self.x() #Координата X последнего тронутого блока на поле
        lastDraggedBlockY = self.y() #Координата Y последнего тронутого блока на поле
        lastDraggedBlockName = "init" + str(blocksCurrentCout) #Имя последнего тронутого блока на поле

        self.xOnMap = self.x() #Текущая координата X текущего блока
        self.yOnMap = self.y() #Текущая координата Y текущего блока
        self.name = lastDraggedBlockName #Имя блока

        self.setText(lastDraggedBlockName)

        blocksCurrentCout = blocksCurrentCout+1
        self.setStyleSheet(stylesheet)

    def mousePressEvent(self, event):
        global grabber
        grabber = True

    def mouseMoveEvent(self, ev):
        global grabber, widthFix, globalMainWindow, extraHeight, extraWidth, consist

        if grabber:
            consist = False

            window_pos = globalMainWindow.pos()
            global_pos = globalMainWindow.mapToGlobal(window_pos)

            extraHeight = globalJofLangLogo.height() + 20 + 50 + int(global_pos.y())//2
            extraWidth = ui.JofLangLogo.width() + ui.block_list.width() + 50 + int(global_pos.x())//2

            currentX = QCursor.pos().x() - extraWidth
            currentY = QCursor.pos().y() - extraHeight
            self.move(currentX, currentY)


    def mouseReleaseEvent(self, ev):
        global grabber, lastDraggedBlockX, lastDraggedBlockY, globalBlockConstructor
        grabber = False
        blocks = globalBlockConstructor.findChildren(BlockForField)
        selfXCenter = self.x() + 50
        selfYCenter = self.y() + 50

        for button in reversed (blocks):
            if (self.name != button.name):
                if (button.x() - 50 < selfXCenter < button.x() + 150):
                    if (button.y() - 50 < selfYCenter < button.y() + 50):
                        self.move(button.x(), button.y() - 100)
                        break
                    else:
                        if (button.y() + 50 < selfYCenter < button.y() + 150):
                            self.move(button.x(), button.y() + 100)
                            break

    def mouseDoubleClickEvent(self, a0):
        global blocksCurrentCout
        blocksCurrentCout = blocksCurrentCout - 1
        self.deleteLater()


class BlockLabel(QPushButton):
    def __init__(self, BlockName, ui, styleSheet):
        super().__init__()
        self.setText(BlockName)
        self.setStyleSheet(styleSheet)
        self.setGeometry(300, 300, 300, 300)
        self.clicked.connect(lambda: self.justAClicked(ui))
    def justAClicked(self, ui):
        global consist, freeX
        ui.scrollAreaWidgetContents.label = BlockForField(ui)
        if consist: freeX = freeX + 150
        else:
            freeX = 0
            consist = True
        ui.scrollAreaWidgetContents.label.setGeometry(freeX, 0, 100, 100)
        ui.scrollAreaWidgetContents.label.setParent(ui.scrollAreaWidgetContents)
        ui.scrollAreaWidgetContents.label.show()


def formatBlocksToCategory(ui, blocksArray, categoryNumber, blocknumber):
    global stylesheet
    match categoryNumber:
        case 0:
            ui.categoryName.setText("Переменные")
            stylesheet = "background-color:  rgb(255, 170, 0);"
        case 1:
            ui.categoryName.setText("Операторы")
            stylesheet = "background-color:  rgb(170, 85, 255);"
        case 2:
            ui.categoryName.setText("Контроль")
            stylesheet = "background-color: rgb(0, 170, 255);"
        case 3:
            ui.categoryName.setText("Контроль_2")
            stylesheet = "background-color: rgb(239, 0, 0);"
        case 4:
            ui.categoryName.setText("Схема")
            stylesheet = "background-color: rgb(255, 255, 255);"
        case 5:
            ui.categoryName.setText("Особенные")
            stylesheet = "background-color: rgb(255, 255, 0);"

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
        ui.verticalLayout_6.addWidget(BlockLabel(blockName, ui, stylesheet))



if __name__ == "__main__":
    execute()
