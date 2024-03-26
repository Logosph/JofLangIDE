from PyQt6.QtGui import QCursor, QIcon, QPixmap, QImage
from PyQt6.QtWidgets import QPushButton, QRubberBand, QLabel, QDialog
import sys
from resources.layout.python.window_main import *
from run import paths, path
from python.domain.blockResources import blocksArray

savingInvisibleInfo = None

ui = Ui_MainWindow()

blocksNames = []
blocksCurrentCout = 0
lastDraggedBlockName = "init"
globalMainWindow = 0
extraHeight = 0
extraWidth = 0

# Элементы интерфейса при запуске записываются сюда, для возможности к ним обращаться
globalJofLangLogo = None
globalBlockConstructor = None
globalInfoCheckTextArea = None
globalCurrentBlockInfoTextArea = None

currentProjectFileName = None
currentProjectFilePath = None

needSave = False
notLoading = True


class SaveBeforeExitModalWindow(QDialog):  # Модальное окно перед выходом из приложения
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Сохранение перед закрытием")
        self.text = QLabel("Сохранить проект перед закрытием приложения?")
        self.cancelButton = QPushButton("Отмена")
        self.acceptButton = QPushButton("Да")
        self.denyButton = QPushButton("Нет")

        self.cancelButton.setMaximumWidth(100)
        self.acceptButton.setMaximumWidth(100)
        self.denyButton.setMaximumWidth(100)

        self.acceptButton.clicked.connect(self.acceptEvent)
        self.denyButton.clicked.connect(self.denyEvent)
        self.cancelButton.clicked.connect(self.cancelEvent)

        buttonsLayout = QGridLayout()
        buttonsLayout.addWidget(self.acceptButton, 0, 0)
        buttonsLayout.addWidget(self.denyButton, 0, 1)
        buttonsLayout.addWidget(self.cancelButton, 0, 2)

        modalLayout = QGridLayout()
        modalLayout.addWidget(self.text, 0, 0)
        modalLayout.addLayout(buttonsLayout, 1, 0)

        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        self.setLayout(modalLayout)

    def acceptEvent(self):  # Да, сохранить проект
        global currentProjectFilePath, currentProjectFileName
        if (currentProjectFileName == None):
            currentProjectFilePath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                                  filetypes=[("Text files", "*.txt")])
            currentProjectFileName = os.path.basename(currentProjectFilePath)
        if currentProjectFilePath:
            with open(currentProjectFilePath, 'w') as file:
                savingVisibleProjectInfo = ui.allBlocksInfoTextArea.toPlainText()
                file.write(savingVisibleProjectInfo)
            globalMainWindow.setWindowTitle("JofLang IDE - " + currentProjectFileName.replace(".txt", ""))
            MainWindow.needSave = False
            print("Сохранено!")
            self.accept()
        else:
            self.reject()

    def denyEvent(self):  # Нет, не сохраняем проект
        self.accept()

    def cancelEvent(self):  # Отмена, не выходим из приложения
        self.reject()


class MainWindowC(QMainWindow):
    def __init__(self):
        super().__init__()

    def resizeEvent(self, event):
        global ElementsHeight, ElementsWidth

        ElementsWidth = self.width()
        ElementsHeight = self.height()

    def closeEvent(self, event):
        if MainWindow.needSave:  # Вызов модального окна, если проект не сохранён
            modal = SaveBeforeExitModalWindow(self)
            if modal.exec() != QDialog.DialogCode.Accepted:
                event.ignore()


def clicked():  # Открытие меню по нажатии кнопки "Файл"
    global ui, globalMainWindow
    ui.context_menu = QMenu()
    createProjectAction = ui.context_menu.addAction("Создать")
    saveProjectAction = ui.context_menu.addAction("Сохранить")
    loadProjectAction = ui.context_menu.addAction("Загрузить")

    window_pos = globalMainWindow.pos()
    global_pos = globalMainWindow.mapToGlobal(window_pos)

    currentX = QCursor.pos().x()
    currentY = QCursor.pos().y()

    point = QPoint(currentX, currentY)

    createProjectAction.triggered.connect(lambda: createProject())
    saveProjectAction.triggered.connect(lambda: saveProject())
    loadProjectAction.triggered.connect(lambda: loadProject())

    ui.context_menu.exec(point)


def createProject():  # Создание нового проекта; не доведено до ума
    pass


def saveProject():  # Сохранение проекта
    global globalMainWindow, currentProjectFilePath, currentProjectFileName
    printGlobalElements()
    if (currentProjectFileName == None):
        currentProjectFilePath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                              filetypes=[("Text files", "*.txt")])
        currentProjectFileName = os.path.basename(currentProjectFilePath)

    if currentProjectFilePath:
        with open(currentProjectFilePath, 'w') as file:
            savingVisibleProjectInfo = ui.allBlocksInfoTextArea.toPlainText()
            file.write(savingVisibleProjectInfo)
        globalMainWindow.setWindowTitle("JofLang IDE - " + currentProjectFileName.replace(".txt", ""))
        MainWindow.needSave = False
        print("Сохранено!")


def loadProject():  # Загрузка проекта
    global globalMainWindow, ui, currentProjectFilePath, currentProjectFileName, notLoading
    currentProjectFilePath = filedialog.askopenfilename(defaultextension=".txt",
                                                        filetypes=[("Text files", "*.txt")])
    if currentProjectFilePath:
        notLoading = False
        currentProjectFileName = os.path.basename(currentProjectFilePath)
        globalMainWindow.setWindowTitle("JofLang IDE - " + currentProjectFileName.replace(".txt", ""))
        with open(currentProjectFilePath, 'r') as file:
            file_content = file.read()

        blocks_info_index = file_content.find("Blocks Info:")

        if blocks_info_index != -1:
            lines_after_blocks_info = file_content[blocks_info_index + len("Blocks Info:"):].splitlines()[1:-1]
            blocks_data = []
            for line in lines_after_blocks_info:
                if line.strip():
                    blocks_data.append(line.strip().split())

            print(f"Загружен файл: {currentProjectFileName}")
            print("Содержимое файла:")

            for child in ui.scrollAreaWidgetContents.findChildren(QtWidgets.QWidget):
                child.deleteLater()

            for block in blocks_data:
                ui.scrollAreaWidgetContents.newBlock = BlockForField(ui, "", "",
                                                                     "")
                ui.scrollAreaWidgetContents.newBlock.setParent(ui.scrollAreaWidgetContents)
                ui.scrollAreaWidgetContents.newBlock.initName = block[0]
                ui.scrollAreaWidgetContents.newBlock.blockCategory = block[1]
                ui.scrollAreaWidgetContents.newBlock.move(int(block[2]), int(block[3]))
                ui.scrollAreaWidgetContents.newBlock.blockInChain = block[4]
                ui.scrollAreaWidgetContents.newBlock.inBackInChain = block[5]
                ui.scrollAreaWidgetContents.newBlock.inFrontInChain = block[6]
                ui.scrollAreaWidgetContents.newBlock.blockInBack = block[7]
                ui.scrollAreaWidgetContents.newBlock.blockInFront = block[8]
                ui.scrollAreaWidgetContents.newBlock.setFixedWidth(175)
                ui.scrollAreaWidgetContents.newBlock.setFixedHeight(100)

                blockImageLink = block[0]
                blockImageLink = blockImageLink[:-1]

                pixmap = QPixmap(paths["blocksIcons"] + str(blockImageLink))
                pixmap = pixmap.scaled(int(ui.scrollAreaWidgetContents.newBlock.width()),
                                       int(ui.scrollAreaWidgetContents.newBlock.height()))

                ui.scrollAreaWidgetContents.newBlock.setPixmap(pixmap)

                ui.scrollAreaWidgetContents.newBlock.setStyleSheet("background-color: rgb(0, 170, 255);")
                ui.scrollAreaWidgetContents.newBlock.show()
                print(block)

            MainWindow.needSave = False
            printGlobalElements()
            notLoading = True
        else:
            print("Не найдена информация о блоках в файле.")


def execute():  # Запуск приложения
    global ui, globalMainWindow, globalJofLangLogo, \
        globalBlockConstructor, globalInfoCheckTextArea, globalCurrentBlockInfoTextArea

    app = QtWidgets.QApplication(sys.argv)
    globalMainWindow = MainWindowC()
    ui.setupUi(globalMainWindow)
    globalJofLangLogo = ui.JofLangLogo
    globalBlockConstructor = ui.block_constructor
    globalCurrentBlockInfoTextArea = ui.currentBlockInfoTextArea
    ui.block_constructor.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, ui.block_constructor)
    ui.block_constructor.rubberBand.origin = None
    globalInfoCheckTextArea = ui.allBlocksInfoTextArea
    ui.VariablesCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 0))
    ui.OperationsCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 1))
    ui.ControlCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 2))
    ui.Control2CategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 3))
    ui.SchemaCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 4))
    ui.SpecialCategoryButton.clicked.connect(lambda: formatBlocksToCategory(ui, 5))

    ui.fileBarButton.clicked.connect(lambda: clicked())

    formatBlocksToCategory(ui, 0)  # Метод, что прорисовывает текущий список блоков

    globalMainWindow.show()
    sys.exit(app.exec())


grabber = False
consist = False
freeX = 0


class BlockForField(QLabel):  # Блок в конструкторе блоков
    def __init__(self, ui, category, styleSheet, blockName):  # Создание блока на поле
        global globalStylesheet, blocksCurrentCout, \
            lastDraggedBlockName, consist, globalInfoCheckTextArea, lastDraggedBlockName, needSave
        super().__init__()

        if needSave:
            pass
        else:
            if notLoading:
                needSave = True
                globalMainWindow.setWindowTitle(globalMainWindow.windowTitle() + "*")
            else:
                pass

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
        if self.initName in blocksNames:
            self.initName = blockName + str(blocksCurrentCout + 1)
            blocksNames.append(self.initName)
        else:
            blocksNames.append(self.initName)
        self.setText(self.initName)
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
            if block.initName == lastDraggedBlockName:
                block.setStyleSheet(block.defaultStyleSheet)
                break
            lastDraggedBlockName = self.initName

    def mousePressEvent(self, event):  # Нажал на блок - включил режим перетаскивания
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

        if lastDraggedBlockName != self.initName:
            blocks = globalBlockConstructor.findChildren(BlockForField)
            for block in blocks:
                if block.initName == lastDraggedBlockName:
                    block.setStyleSheet(block.defaultStyleSheet)
                    break
        lastDraggedBlockName = self.initName

    def mouseMoveEvent(self, ev):  # Перетаскивание блока
        global grabber, globalMainWindow, extraHeight, extraWidth, consist, globalBlockConstructor

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
                if block.initName == self.backBlockInChain:
                    block.inChainInBack = False
                    block.frontBlockInChain = None
                    block.inChain = False
                if block.initName == self.frontBlockInChain:
                    block.inChainInFront = False
                    block.backBlockInChain = None
                    block.inChain = False

            self.inChain = False
            self.backBlockInChain = None
            self.frontBlockInChain = None
            self.inChainInFront = False
            self.inChainInBack = False

            printInfoAboutBlock(self)

    def mouseReleaseEvent(self, ev):  # Блок "падает", если рядом есть другой - он к нему крепится
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
                        self.frontBlockInChain = button.initName
                        button.backBlockInChain = self.initName
                        self.move(button.x(), button.y() - 100 + 20)
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
                            self.backBlockInChain = button.initName
                            button.frontBlockInChain = self.initName
                            self.move(button.x(), button.y() + button.height() - 20)
                            self.inChain = True
                            self.inChainInFront = True
                            button.inChain = True
                            button.inChainInBack = True
                            break

        printInfoAboutBlock(self)
        printGlobalElements()

    def mouseDoubleClickEvent(self, a0):  # Удаление блока с поля
        global blocksCurrentCout, globalInfoCheckTextArea, lastDraggedBlockName, needSave, globalBlockConstructor
        if needSave:
            pass
        else:
            needSave = True
            globalMainWindow.setWindowTitle(globalMainWindow.windowTitle() + "*")
        blocksCurrentCout = blocksCurrentCout - 1
        blocks = globalBlockConstructor.findChildren(BlockForField)
        for block in blocks:
            if block.inChain:
                if self.backBlockInChain == block.initName:
                    block.frontBlockInChain = None
                    block.inChainInBack = False
                if self.frontBlockInChain == block.initName:
                    block.backBlockInChain = None
                    block.inChainInFront = False

        for block in blocks:
            if (block.inChain & ((self.backBlockInChain == None) & (self.frontBlockInChain == None))):
                block.inChain = False

        self.deleteLater()
        globalCurrentBlockInfoTextArea.setText(None)

        lastDraggedBlockName = self.initName
        printGlobalElements()


def printGlobalElements():  # Обновление информации всего проекта
    global globalInfoCheckTextArea, globalBlockConstructor, savingInvisibleInfo  # , deletingObject

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
                promejBlocks.append(block.initName)
            else:
                if block.inChainInBack:
                    firstBlocks.append(block.initName)
                if block.inChainInFront:
                    lastBlocks.append(block.initName)

        else:
            radicalBlocks.append(block.initName)

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

    globalInfoCheckTextArea.setText(
        globalInfoCheckTextArea.toPlainText() + someString + "\n" + "Blocks Info:\n" + savingInvisibleInfo)

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


class BlockLabel(QPushButton):  # Кнопки справа
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

    def justAClicked(self, ui):  # Нажал на определённый блок - он образовался на поле
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


def formatBlocksToCategory(ui, categoryNumber):  # Прорисовка списка блоков
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


def printInfoAboutBlock(block):  # Вывод информации о последнем блоке
    global ui, globalCurrentBlockInfoTextArea
    globalCurrentBlockInfoTextArea.setText("initName - " + block.initName + "\nblockCategory - " + block.blockCategory +
                                           "\nX - " + str(block.x()) + "\nY - " + str(block.y()) +
                                           "\ninChain - " + str(block.inChain) +
                                           "\ninChainInBack - " + str(
        block.inChainInBack) + "\ninChainInFront - " + str(block.inChainInFront) +
                                           "\nbackBlockInChain - " + str(
        block.backBlockInChain) + "\nfrontBlockInChain - " +
                                           str(block.frontBlockInChain) + "\n\n")


if __name__ == "__main__":
    execute()
