from PyQt6.QtGui import QCursor, QIcon, QPixmap, QImage
from PyQt6.QtWidgets import QPushButton, QRubberBand, QLabel, QDialog
import sys
from resources.layout.python.window_main import *
from run import paths, path
from python.domain.blockResources import blocksArray

itsDeleteOperation = False

savingInvisibleInfo = None

ui = Ui_MainWindow()
widthFix = 0
blocksInfo = [[0, 0, "init0"]]
blocksCurrentCout = 0
lastDraggedBlockName = "init"
globalMainWindow = 0
extraHeight = 0
extraWidth = 0

# Элементы интерфейса при запуске записываются сюда, для возможности к ним обращаться
globalJofLangLogo = None
globalBlockList = None
globalBlockConstructor = None
globalInfoCheckTextArea = None
globalCurrentBlockInfoTextArea = None

needSave = False


def execute():
    global ui, widthFix, globalMainWindow, globalJofLangLogo, globalBlockList, \
        globalBlockConstructor, globalInfoCheckTextArea, globalCurrentBlockInfoTextArea

    app = QtWidgets.QApplication(sys.argv)
    globalMainWindow = MainWindowC()
    ui.setupUi(globalMainWindow)
    globalJofLangLogo = ui.JofLangLogo
    globalBlockList = ui.block_list
    globalBlockConstructor = ui.block_constructor
    globalCurrentBlockInfoTextArea = ui.currentBlockInfoTextArea
    ui.block_constructor.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, ui.block_constructor)
    ui.block_constructor.rubberBand.origin = None
    globalInfoCheckTextArea = ui.allBlocksInfoTextArea
    widthFix = ui.tableView_6.width() + ui.scrollArea_2.width()

    ui.VariablesCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 0))
    ui.OperationsCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 1))
    ui.ControlCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 2))
    ui.Control2CategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 3))
    ui.SchemaCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 4))
    ui.SpecialCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 5))

    formatBlocksToCategory(ui, 0)  # Метод, что прорисовывает текущий список блоков

    globalMainWindow.show()
    sys.exit(app.exec())


grabber = False
consist = False
freeX = 0


class BlockForField(QLabel):  # Блок в конструкторе блоков
    def __init__(self, ui, category, styleSheet, blockName):  # Создание блока на поле
        global globalStylesheet, blocksCurrentCout, \
            lastDraggedBlockName, blocksInfo, consist, globalInfoCheckTextArea, lastDraggedBlockName, needSave
        super().__init__()

        if needSave:
            pass
        else:
            needSave = True
            globalMainWindow.setWindowTitle(globalMainWindow.windowTitle() + "*")

        self.inChainInFront = False
        self.inChainInBack = False
        self.inChain = False

        self.frontBlockInChain = None
        self.backBlockInChain = None
        self.defaultStyleSheet = styleSheet  # Надо определять по нажимаемой кнопке
        self.selectedStyleSheet = styleSheet + "border-style: solid; border-width: 1px; border-color: black;"

        self.blockCategory = category

        self.xOnMap = self.x()
        self.yOnMap = self.y()  # Для сохранённых проектов
        self.name = blockName
        self.initName = blockName + str(blocksCurrentCout)
        self.setText(self.name)
        pixmap = QPixmap(QPixmap(paths["blocksIcons"] + self.name + ".jpg"))
        self.setFixedWidth(175)
        self.setFixedHeight(100)
        pixmap = pixmap.scaled(int(self.width()), int(self.height()))
        self.setPixmap(pixmap)
        blocksCurrentCout = blocksCurrentCout + 1
        self.setStyleSheet(styleSheet)

        printInfoAboutBlock(self)
        self.setStyleSheet(self.selectedStyleSheet)

        blocks = globalBlockConstructor.findChildren(BlockForField)
        for block in blocks:
            if block.name == lastDraggedBlockName:
                block.setStyleSheet(block.defaultStyleSheet)
                break
            lastDraggedBlockName = self.name

    # def __init__(self, initName, category, x, y, blockInChain, inBackInChain, inFrontInChain, blockInBack, blockInFront):
    #     super().__init__()
    #     self.initName = initName
    #     self.blockCategory = category
    #     self.xOnMap = x
    #     self.yOnMap = y
    #     self.blockInChain = blockInChain
    #     self.inBackInChain = inBackInChain
    #     self.inFrontInChain = inFrontInChain
    #     self.blockInBack = blockInBack
    #     self.blockInFront = blockInFront
    #     self.setFixedWidth(175)
    #     self.setFixedHeight(100)


    def mousePressEvent(self, event):
        global grabber, globalBlockConstructor, lastDraggedBlockName, needSave
        grabber = True
        if needSave:
            pass
        else:
            needSave = True
            globalMainWindow.setWindowTitle(globalMainWindow.windowTitle() + "*")
        globalCurrentBlockInfoTextArea.setText(str(self.x()))
        printInfoAboutBlock(self)
        self.setStyleSheet(self.selectedStyleSheet)

        if lastDraggedBlockName != self.name:
            blocks = globalBlockConstructor.findChildren(BlockForField)
            for block in blocks:
                if block.name == lastDraggedBlockName:
                    block.setStyleSheet(block.defaultStyleSheet)
                    break
        lastDraggedBlockName = self.name

    def mouseMoveEvent(self, ev):
        global grabber, widthFix, globalMainWindow, extraHeight, extraWidth, consist, globalBlockConstructor

        if grabber:
            window_pos = globalMainWindow.pos()
            global_pos = globalMainWindow.mapToGlobal(window_pos)

            extraHeight = globalJofLangLogo.height() + 20 + 50 + int(global_pos.y()) // 2
            extraWidth = ui.JofLangLogo.width() + ui.block_list.width() + 50 + int(global_pos.x()) // 2

            currentX = QCursor.pos().x() - extraWidth
            currentY = QCursor.pos().y() - extraHeight
            self.move(currentX, currentY)

            blocks = globalBlockConstructor.findChildren(BlockForField)

            for block in blocks:
                if block.name == self.backBlockInChain:
                    block.inChainInBack = False
                    block.frontBlockInChain = None
                    block.inChain = False
                if block.name == self.frontBlockInChain:
                    block.inChainInFront = False
                    block.backBlockInChain = None
                    block.inChain = False

            self.inChain = False
            self.backBlockInChain = None
            self.frontBlockInChain = None
            self.inChainInFront = False
            self.inChainInBack = False

            printInfoAboutBlock(self)

    def mouseReleaseEvent(self, ev):
        global grabber, lastDraggedBlockX, lastDraggedBlockY, globalBlockConstructor
        grabber = False

        blocks = globalBlockConstructor.findChildren(BlockForField)

        selfXCenter = self.x() + self.width() / 2
        selfYCenter = self.y() + self.height() / 2

        for button in reversed(blocks):
            if (self.initName != button.initName):
                if (button.x() - 50 < selfXCenter < button.x() + 150):
                    if (button.y() - 50 < selfYCenter < button.y() + 50):  # Прикрепление блока сверху
                        if self.inChain == True:
                            self.inChainInBack = False
                            self.inChainInFront = False
                        self.frontBlockInChain = button.name
                        button.backBlockInChain = self.name
                        self.move(button.x(), button.y() - 100)
                        self.inChain = True
                        self.inChainInBack = True
                        button.inChain = True
                        button.inChainInFront = True
                        break
                    else:
                        if (button.y() + 50 < selfYCenter < button.y() + 150):  # Прикрепление блока снизу
                            if self.inChain == True:
                                self.inChainInFront = False
                                self.inChainInBack = False
                            self.backBlockInChain = button.name
                            button.frontBlockInChain = self.name
                            self.move(button.x(), button.y() + button.height() - 20)
                            self.inChain = True
                            self.inChainInFront = True
                            button.inChain = True
                            button.inChainInBack = True
                            break

        printInfoAboutBlock(self)
        printGlobalElements()

    def mouseDoubleClickEvent(self, a0):  # Удаление блока с поля
        global blocksCurrentCout, globalInfoCheckTextArea, lastDraggedBlockName, itsDeleteOperation, needSave  # , deletingObject
        if needSave:
            pass
        else:
            needSave = True
            globalMainWindow.setWindowTitle(globalMainWindow.windowTitle() + "*")
        blocksCurrentCout = blocksCurrentCout - 1
        self.deleteLater()
        globalCurrentBlockInfoTextArea.setText(None)

        if lastDraggedBlockName != self.name:
            blocks = globalBlockConstructor.findChildren(BlockForField)
            for block in blocks:
                if block.name == lastDraggedBlockName:
                    block.setStyleSheet(block.defaultStyleSheet)
                    break

        lastDraggedBlockName = self.name
        printGlobalElements()


def printGlobalElements():
    global globalInfoCheckTextArea, globalBlockConstructor, itsDeleteOperation, savingInvisibleInfo  # , deletingObject

    firstBlocks = []
    lastBlocks = []
    promejBlocks = []
    radicalBlocks = []
    cepochki = []

    savingInvisibleInfo = ""

    allBlocks = globalBlockConstructor.findChildren(BlockForField)
    allBlocksCount = len(allBlocks)
    globalInfoCheckTextArea.setText("")
    for block in allBlocks:
        if block.inChain:
            if (block.inChainInBack & block.inChainInFront):
                promejBlocks.append(block.name)
            else:
                if block.inChainInBack:
                    firstBlocks.append(block.name)
                if block.inChainInFront:
                    lastBlocks.append(block.name)

        else:
            radicalBlocks.append(block.name)

        currentBlockInfo = ("\t" + str(block.initName) + " " +
                            str(block.blockCategory) + " " +
                            str(block.x()) + " " +
                            str(block.y()) + " " +
                            str(block.inChain) + " " +
                            str(block.inChainInBack) + " " +
                            str(block.inChainInFront) + " " +
                            str(block.backBlockInChain) + " " +
                            str(block.frontBlockInChain) + "\n\n")
        savingInvisibleInfo = savingInvisibleInfo + currentBlockInfo

    someString = "Amount " + str(allBlocksCount) + "\n"
    globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")

    someString = "First " + str(len(firstBlocks)) + ": \n"
    for i in firstBlocks:
        someString = someString + "          " + i + "\n"

    globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")

    someString = "Last " + str(len(lastBlocks)) + ": \n"
    for i in lastBlocks:
        someString = someString + "          " + i + "\n"

    globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")

    someString = "Intermediate " + str(len(promejBlocks)) + ": \n"
    for i in promejBlocks:
        someString = someString + "          " + i + "\n"

    globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")

    someString = "Outside chains " + str(len(radicalBlocks)) + ": \n"
    for i in radicalBlocks:
        someString = someString + "          " + i + "\n"

    globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n" + "Blocks Info:\n" + savingInvisibleInfo)

    if len(firstBlocks) > 0:
        for i in range(len(firstBlocks)):
            cepochki.append(firstBlocks[i] + " - ")
            lastBlock = None
            blocksCount = 0

            for block in allBlocks:
                if block.backBlockInChain == firstBlocks[i]:
                    cepochki[i] = cepochki[i] + block.initName + " - "
                    blocksCount = 2
                    lastBlock = block
                    break

            lastFound = False
            for j in range(len(promejBlocks)):
                for block in allBlocks:
                    if (block.initName == lastBlock.frontBlockInChain) & (block.frontBlockInChain != None):
                        cepochki[i] = cepochki[i] + block.initName + " - "
                        blocksCount = blocksCount + 1
                        lastBlock = block
                        break
                    if (block.initName == lastBlock.frontBlockInChain) & (block.frontBlockInChain == None):
                        lastFound = True
                        blocksCount = blocksCount + 1
                        cepochki[i] = cepochki[i] + block.initName
                        break
                if lastFound:
                    break

            if blocksCount == 2:
                stringB = cepochki[i]
                cepochki[i] = stringB[0: int(len(stringB) - 3)]

            someString = cepochki[i]
            globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")


class BlockLabel(QPushButton):
    def __init__(self, blockName, ui, thisStyleSheet, thisCategory):
        super().__init__()
        self.setIcon(QIcon(paths["blocksIcons"] + blockName + ".jpg"))
        self.setIconSize(QSize(75, 50))
        self.blockStyleSheet = thisStyleSheet
        self.blockCategory = thisCategory
        self.blockName = blockName
        self.setFlat(True)
        self.setGeometry(300, 300, 300, 300)
        self.clicked.connect(lambda: self.justAClicked(ui))

    def justAClicked(self, ui):
        global consist, freeX, needSave
        if needSave:
            pass
        else:
            needSave = True
            globalMainWindow.setWindowTitle(globalMainWindow.windowTitle() + "*")
        ui.scrollAreaWidgetContents.label = BlockForField(ui, self.blockCategory, self.blockStyleSheet, self.blockName)
        if consist:
            freeX = freeX + 150
        else:
            freeX = 0
            consist = True
        ui.scrollAreaWidgetContents.label.setGeometry(freeX, 0, 100, 100)
        ui.scrollAreaWidgetContents.label.setParent(ui.scrollAreaWidgetContents)
        ui.scrollAreaWidgetContents.label.show()
        printInfoAboutBlock(ui.scrollAreaWidgetContents.label)
        printGlobalElements()


def formatBlocksToCategory(ui, categoryNumber):
    match categoryNumber:
        case 0:
            ui.categoryName.setText("Переменные")  # Должен определять по нажатию на категорию
            thisStyleSheet = "background-color:  rgb(255, 170, 0);"
            thisCategory = "Variables"
        case 1:
            ui.categoryName.setText("Операторы")
            thisStyleSheet = "background-color:  rgb(170, 85, 255);"
            thisCategory = "Operators"
        case 2:
            ui.categoryName.setText("Контроль")
            thisStyleSheet = "background-color: rgb(0, 170, 255);"
            thisCategory = "Control"
        case 3:
            ui.categoryName.setText("Контроль_2")
            thisStyleSheet = "background-color: rgb(239, 0, 0);"
            thisCategory = "Control_2"
        case 4:
            ui.categoryName.setText("Схема")
            thisStyleSheet = "background-color: rgb(255, 255, 255);"
            thisCategory = "Schema"
        case 5:
            ui.categoryName.setText("Особенные")
            thisStyleSheet = "background-color: rgb(255, 255, 0);"
            thisCategory = "Special"

    countOfBlocks = ui.scrollAreaWidgetContents_2.findChildren(QPushButton)
    for i in countOfBlocks:
        i.deleteLater()
        i.widget_name = None

    for i in range(len(blocksArray[categoryNumber])):
        blockName = "Block" + str(categoryNumber) + str(i)
        ui.verticalLayout_6.addWidget(BlockLabel(blockName, ui, thisStyleSheet, thisCategory))


def printInfoAboutBlock(block):
    global ui, globalCurrentBlockInfoTextArea
    globalCurrentBlockInfoTextArea.setText("initName - " + block.name + "\nblockCategory - " + block.blockCategory +
                                           "\nX - " + str(block.x()) + "\nY - " + str(block.y()) +
                                           "\ninChain - " + str(block.inChain) +
                                           "\ninChainInBack - " + str(
        block.inChainInBack) + "\ninChainInFront - " + str(block.inChainInFront) +
                                           "\nbackBlockInChain - " + str(
        block.backBlockInChain) + "\nfrontBlockInChain - " +
                                           str(block.frontBlockInChain) + "\n\n")


if __name__ == "__main__":
    execute()
