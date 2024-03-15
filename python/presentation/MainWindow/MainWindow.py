from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QPushButton, QRubberBand, QLabel

from resources.layout.python.window_main import *
import sys


globalStylesheet = ""
applicationElementWidth = 10
applicationElementHeight = 10
ui = Ui_MainWindow()
widthFix = 0
ElementsHeight = 0
ElementsWidth = 0
blocksInfo = [[0, 0, "init0"]]
blocksCurrentCout = 0
lastDraggedBlockName = "init"
globalMainWindow = 0
extraHeight = 0
extraWidth = 0

globalJofLangLogo = None
globalBlockList = None
globalBlockConstructor = None
globalInfoCheckTextArea = None
globalCurrentBlockInfoTextArea = None
globalCategory = None
globalSelectedStylesheet = None

def execute():
    global ui, widthFix, globalMainWindow, globalJofLangLogo, globalBlockList,\
        globalBlockConstructor, globalInfoCheckTextArea, globalCurrentBlockInfoTextArea

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
    globalCurrentBlockInfoTextArea = ui.currentBlockInfoTextArea
    ui.block_constructor.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, ui.block_constructor)
    ui.block_constructor.rubberBand.origin = None
    globalInfoCheckTextArea = ui.allBlocksInfoTextArea
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
    def __init__(self, ui, category):
        global globalStylesheet, blocksCurrentCout, lastDraggedBlockX,\
            lastDraggedBlockY, lastDraggedBlockName, blocksInfo, consist, globalInfoCheckTextArea, lastDraggedBlockName

        super().__init__()

        lastDraggedBlockX = self.x() #Координата X последнего тронутого блока на поле
        lastDraggedBlockY = self.y() #Координата Y последнего тронутого блока на поле

        self.inChainInFront = False
        self.inChainInBack = False
        self.inChain = False

        self.frontBlockInChain = None
        self.backBlockInChain = None
        self.defaultStyleSheet = globalStylesheet
        self.selectedStyleSheet = globalStylesheet + "border-style: solid; border-width: 1px; border-color: black;"

        self.blockCategory = category

        self.xOnMap = self.x() #Текущая координата X текущего блока
        self.yOnMap = self.y() #Текущая координата Y текущего блока
        self.name = "init" + str(blocksCurrentCout) #Имя блока

        # print(self.name)

        #####

        # globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + self.name + "\n")

        self.setText(self.name)

        blocksCurrentCout = blocksCurrentCout+1
        self.setStyleSheet(globalStylesheet)

        printInfoAboutBlock(self)
        self.setStyleSheet(self.selectedStyleSheet)

        blocks = globalBlockConstructor.findChildren(BlockForField)
        for block in blocks:
            if block.name == lastDraggedBlockName:
                block.setStyleSheet(block.defaultStyleSheet)
                break
        lastDraggedBlockName = self.name


    def mousePressEvent(self, event):
        global grabber, globalBlockConstructor, lastDraggedBlockName
        grabber = True
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
            # consist = False

            window_pos = globalMainWindow.pos()
            global_pos = globalMainWindow.mapToGlobal(window_pos)

            extraHeight = globalJofLangLogo.height() + 20 + 50 + int(global_pos.y())//2
            extraWidth = ui.JofLangLogo.width() + ui.block_list.width() + 50 + int(global_pos.x())//2

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
        # itsNotConnection = True

        blocks = globalBlockConstructor.findChildren(BlockForField)

        selfXCenter = self.x() + 50
        selfYCenter = self.y() + 50

        for button in reversed (blocks):
            if (self.name != button.name):
                if (button.x() - 50 < selfXCenter < button.x() + 150):
                    if (button.y() - 50 < selfYCenter < button.y() + 50): #Прикрепление блока наверх
                        if self.inChain == True:
                            # if self.inChainInFront:
                            #     globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText().replace("-" + self.name, ""))
                            # if self.inChainInBack:
                            #     globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText().replace(self.name + "-", ""))
                            self.inChainInBack = False
                            self.inChainInFront = False
                        # else:
                        #     globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText().replace(self.name + "\n", ""))

                        # globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText().replace(button.name + "\n", self.name + "-" + button.name + "\n"))

                        self.frontBlockInChain = button.name
                        button.backBlockInChain = self.name
                        self.move(button.x(), button.y() - 100)
                        self.inChain = True
                        self.inChainInBack = True
                        button.inChain = True
                        button.inChainInFront = True
                        # itsNotConnection = False
                        break
                    else:
                        if (button.y() + 50 < selfYCenter < button.y() + 150): #Прикрепление блока вниз
                            if self.inChain == True:
                                # if self.inChainInFront:
                                #     globalInfoCheckTextArea.setText(
                                #         globalInfoCheckTextArea.toPlainText().replace("-" + self.name, ""))
                                # if self.inChainInBack:
                                #     globalInfoCheckTextArea.setText(
                                #         globalInfoCheckTextArea.toPlainText().replace("-" + self.name , ""))
                                self.inChainInFront = False
                                self.inChainInBack = False
                            # else:
                            #     globalInfoCheckTextArea.setText(
                            #         globalInfoCheckTextArea.toPlainText().replace(self.name + "\n", ""))
                            # globalInfoCheckTextArea.setText(
                            #     globalInfoCheckTextArea.toPlainText().replace(button.name + "\n",
                            #                                                    button.name + "-" + self.name + "\n"))
                            self.backBlockInChain = button.name
                            button.frontBlockInChain = self.name
                            self.move(button.x(), button.y() + 100)
                            self.inChain = True
                            self.inChainInFront = True
                            button.inChain = True
                            button.inChainInBack = True
                            #itsNotConnection = False
                            break


        printInfoAboutBlock(self)
        printGlobalElements()
        #if itsNotConnection:

def printGlobalElements():
    global globalInfoCheckTextArea, globalBlockConstructor

    firstBlocks = []
    lastBlocks = []
    promejBlocks = []
    radicalBlocks = []
    cepochki = []

    allBlocks = globalBlockConstructor.findChildren(BlockForField)
    allBlocksCount = len(allBlocks)
    globalInfoCheckTextArea.setText("")
    # doubleMoment = False
    # constructionMode = False
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
        #     if constructionMode:
        #         if block.inChainInFront:
        #
        #         if block.inChainInBack:
        #             buffer = str(globalInfoCheckTextArea.toPlainText())
        #             buffer.replace("")
        #
        #     else:
        #         if block.inChainInBack:
        #             constructionMode = True
        #             currentString = str(block.name) + "+" + str(block.frontBlockInChain)
        #             globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + "\n" + currentString)
        #             doubleMoment = True
        #
        #         if block.inChainInFront:
        #             if doubleMoment:
        #                 globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + "+" + str(block.name))
        #             else:
        #                 constructionMode = True
        #                 currentString = block.backBlockInChain + "+" + str(block.name)
        #                 globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + "\n" + currentString)
        #         if block.inChainInBack:
        #             constructionMode = True
        #             currentString = str(block.name) + "+" + str(block.frontBlockInChain)
        #             globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + "\n" + currentString)
        #             doubleMoment = True
        #
        # else:
        #     if constructionMode:
        #         constructionMode = False
        #         globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + "\n" + block.name + "\n")
        #     else:
        #         globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + block.name + "\n")

            radicalBlocks.append(block.name)

    # globalInfoCheckTextArea.setText("Firsts - " + str(len(firstBlocks)) +
    #                                 "\nLasts - " + str(len(lastBlocks)) +
    #                                 "\nPromejs - " + str(len(promejBlocks)) +
    #                                 "\nRadicals - " + str(len(radicalBlocks)) + "\n\n")
    someString = "Amount of blocks  " + str(allBlocksCount) + "\n"
    globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")

    someString = "Firsts " + str(len(firstBlocks)) + ": \n"
    for i in firstBlocks:
        someString = someString + "          " + i + "\n"

    globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")

    someString = "Lasts " + str(len(lastBlocks)) + ": \n"
    for i in lastBlocks:
        someString = someString + "          " + i + "\n"

    globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")

    someString = "Promejs " + str(len(promejBlocks)) + ": \n"
    for i in promejBlocks:
        someString = someString + "          " + i + "\n"

    globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")

    someString = "Radicals " + str(len(radicalBlocks)) + ": \n"
    for i in radicalBlocks:
        someString = someString + "          " + i + "\n"

    globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")

    if len(firstBlocks) > 0:
        for i in range(len(firstBlocks)):
            cepochki.append(firstBlocks[i] + " - ")
            afterLastFound = False
            beforeLastFound = False
            lastBlock = None
            maybeItsTheLast = True
            blocksCount = 0


            for block in allBlocks:
                if block.backBlockInChain == firstBlocks[i]:
                    cepochki[i] = cepochki[i] + block.name + " - "
                    maybeItsTheLast = True
                    blocksCount = 2
                    lastBlock = block
                    break

            lastFound = False
            for j in range(len(promejBlocks)):
                for block in allBlocks:
                    if (block.name == lastBlock.frontBlockInChain) & (block.frontBlockInChain != None):
                        cepochki[i] = cepochki[i] + block.name + " - "
                        maybeItsTheLast = False
                        blocksCount = blocksCount + 1
                        lastBlock = block
                        break
                    if (block.name == lastBlock.frontBlockInChain) & (block.frontBlockInChain == None):
                    #     beforeLastFound = True
                        lastFound = True
                        blocksCount = blocksCount + 1
                        cepochki[i] = cepochki[i] + block.name
                        break
                if lastFound:
                    break


            if blocksCount == 2:
                stringB = cepochki[i]
                cepochki[i] = stringB[0: int(len(stringB) - 3)]

            someString = cepochki[i]
            globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText() + someString + "\n")


    # doubleMoment = False

    def mouseDoubleClickEvent(self, a0):
        global blocksCurrentCout, globalInfoCheckTextArea, lastDraggedBlockName
        # if self.inChain:
        #     if self.inChainInFront:
        #         globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText().replace("-" + self.name, ""))
        #     if self.inChainInBack:
        #         globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText().replace(self.name + "-", ""))
        # else:
        #     globalInfoCheckTextArea.setText(globalInfoCheckTextArea.toPlainText().replace(self.name + "\n", ""))
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



class BlockLabel(QPushButton):
    def __init__(self, BlockName, ui, styleSheet):
        super().__init__()
        self.setText(BlockName)
        self.setStyleSheet(styleSheet)
        self.setGeometry(300, 300, 300, 300)
        self.clicked.connect(lambda: self.justAClicked(ui))
    def justAClicked(self, ui):
        global consist, freeX, globalCategory
        ui.scrollAreaWidgetContents.label = BlockForField(ui, globalCategory)
        if consist: freeX = freeX + 150
        else:
            freeX = 0
            consist = True
        ui.scrollAreaWidgetContents.label.setGeometry(freeX, 0, 100, 100)
        ui.scrollAreaWidgetContents.label.setParent(ui.scrollAreaWidgetContents)
        ui.scrollAreaWidgetContents.label.show()
        printInfoAboutBlock(ui.scrollAreaWidgetContents.label)



def formatBlocksToCategory(ui, blocksArray, categoryNumber, blocknumber):
    global globalStylesheet, globalCategory
    match categoryNumber:
        case 0:
            ui.categoryName.setText("Переменные")
            globalStylesheet = "background-color:  rgb(255, 170, 0);"
            globalCategory = "Variables"
        case 1:
            ui.categoryName.setText("Операторы")
            globalStylesheet = "background-color:  rgb(170, 85, 255);"
            globalCategory = "Operators"
        case 2:
            ui.categoryName.setText("Контроль")
            globalStylesheet = "background-color: rgb(0, 170, 255);"
            globalCategory = "Control"
        case 3:
            ui.categoryName.setText("Контроль_2")
            globalStylesheet = "background-color: rgb(239, 0, 0);"
            globalCategory = "Control_2"
        case 4:
            ui.categoryName.setText("Схема")
            globalStylesheet = "background-color: rgb(255, 255, 255);"
            globalCategory = "Schema"
        case 5:
            ui.categoryName.setText("Особенные")
            globalStylesheet = "background-color: rgb(255, 255, 0);"
            globalCategory = "Special"

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
        ui.verticalLayout_6.addWidget(BlockLabel(blockName, ui, globalStylesheet))

def printInfoAboutBlock(block):
    global ui, globalCurrentBlockInfoTextArea
    # print(block.name)
    globalCurrentBlockInfoTextArea.setText("X - " + str(block.x()) + "\nY - " + str(block.y()) +
                                           "\nName - " + block.name + "\nblockCategory - " + block.blockCategory +
                                           "\ninChain - " + str(block.inChain) + "\ninChainInFront - " + str(
                                            block.inChainInFront) +
                                           "\ninChainInBack - " + str(block.inChainInBack) + "\nfrontBlockInChain - " +
                                           str(block.frontBlockInChain) + "\nbackBlockInChain - " + str(
                                            block.backBlockInChain))

if __name__ == "__main__":
    execute()
