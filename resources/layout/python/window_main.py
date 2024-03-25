import os
from tkinter import filedialog

import win32api
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRect, QSize, Qt, QPoint, QEvent
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication, QScrollArea, QMenu, QDialog, QLabel, QPushButton, QLayout, QGridLayout, \
    QMainWindow

from python.presentation.MainWindow import MainWindow
#from python.presentation.MainWindow.MainWindow import BlockForField

from run import paths

from PyQt6.QtWidgets import QMainWindow, QDialog, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

from tkinter import *

globalUi = None
globalMainWindow = None


# class BlockForField(QLabel):  # Блок в конструкторе блоков
#     def __init__(self, initName, category, x, y, blockInChain, inBackInChain, inFrontInChain, blockInBack, blockInFront):
#         super().__init__()
#         self.initName = initName
#         self.blockCategory = category
#         self.xOnMap = x
#         self.yOnMap = y
#         self.blockInChain = blockInChain
#         self.inBackInChain = inBackInChain
#         self.inFrontInChain = inFrontInChain
#         self.blockInBack = blockInBack
#         self.blockInFront = blockInFront
#         self.setFixedWidth(175)
#         self.setFixedHeight(100)


class SaveBeforeExitModalWindow(QDialog):
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

    def acceptEvent(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        file_name = os.path.basename(file_path)
        if file_path:
            with open(file_path, 'w') as file:
                savingVisibleProjectInfo = globalUi.allBlocksInfoTextArea.toPlainText()
                # for child in globalUi.block_constructor.findChildren(QtWidgets.QWidget):
                #     currentChildInfo = (str(child.initName) + " " +
                #                         str(child.blockCategory) + " " +
                #                         str(child.x()) + " " +
                #                         str(child.y()) + " " +
                #                         str(child.inChain) + " " +
                #                         str(child.inChainInBack) + " " +
                #                         str(child.inChainInFront) + " " +
                #                         str(child.backBlockInChain) + " " +
                #                         str(child.frontBlockInChain) + "\n\n")
                #     savingInvisibleInfo = savingInvisibleInfo + currentChildInfo

                file.write(savingVisibleProjectInfo)
            globalMainWindow.setWindowTitle("JofLang IDE - " + file_name.replace(".txt", ""))
            MainWindow.needSave = False
            print("Сохранено!")
            self.accept()
        else:
            self.reject()

    def denyEvent(self):
        self.accept()

    def cancelEvent(self):
        self.reject()


class MainWindowC(QMainWindow):
    def __init__(self):
        super().__init__()

    def resizeEvent(self, event):
        global ElementsHeight, ElementsWidth

        ElementsWidth = self.width()
        ElementsHeight = self.height()

    # def closeEvent(self, event):
    #     global needSave
    #     needSave = returnNeedSave()
    #     if needSave:
    #         modal = SaveBeforeExitModalWindow(self)
    #         if modal.exec() != QDialog.DialogCode.Accepted:
    #             event.ignore()

    def closeEvent(self, event):
        if MainWindow.needSave:
            modal = SaveBeforeExitModalWindow(self)
            if modal.exec() != QDialog.DialogCode.Accepted:
                event.ignore()


globalMainWindow = None
globalBlockConstructor = None


class block_constructorr(QScrollArea):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.origin = event.pos()
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if self.origin:
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.origin:
            self.rubberBand.hide()
            self.origin = None


class Ui_MainWindow(object):
    def __init__(self):
        global globalUi
        self.block_constructor = None
        self.iconsDir = paths["icons"]
        globalUi = self

    def setupUi(self, MainWindow):
        global globalMainWindow
        globalMainWindow = MainWindow
        MainWindow.setWindowTitle("JofLang IDE - Untitled")
        MainWindow.setWindowIcon(QtGui.QIcon(self.iconsDir + "JofLangIcon.png"))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setSizeIncrement(QtCore.QSize(-31072, 0))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.JofLangLogo = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.JofLangLogo.sizePolicy().hasHeightForWidth())
        self.JofLangLogo.setSizePolicy(sizePolicy)
        self.JofLangLogo.setMaximumSize(QtCore.QSize(65, 65))
        self.JofLangLogo.setText("")
        self.JofLangLogo.setPixmap(QtGui.QPixmap(self.iconsDir + "JofLangIcon.png"))
        self.JofLangLogo.setScaledContents(True)
        self.JofLangLogo.setObjectName("JofLangLogo")
        self.horizontalLayout_2.addWidget(self.JofLangLogo)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fileBarButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileBarButton.sizePolicy().hasHeightForWidth())
        self.fileBarButton.setSizePolicy(sizePolicy)
        self.fileBarButton.setMinimumSize(QtCore.QSize(75, 20))
        self.fileBarButton.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fileBarButton.setFont(font)
        self.fileBarButton.setObjectName("fileBarButton")
        self.horizontalLayout_3.addWidget(self.fileBarButton)
        self.optionsBarButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.optionsBarButton.sizePolicy().hasHeightForWidth())
        self.optionsBarButton.setSizePolicy(sizePolicy)
        self.optionsBarButton.setMinimumSize(QtCore.QSize(75, 20))
        self.optionsBarButton.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.optionsBarButton.setFont(font)
        self.optionsBarButton.setObjectName("optionsBarButton")
        self.horizontalLayout_3.addWidget(self.optionsBarButton)
        self.executeBarButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.executeBarButton.sizePolicy().hasHeightForWidth())
        self.executeBarButton.setSizePolicy(sizePolicy)
        self.executeBarButton.setMinimumSize(QtCore.QSize(75, 20))
        self.executeBarButton.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.executeBarButton.setFont(font)
        self.executeBarButton.setObjectName("executeBarButton")
        self.horizontalLayout_3.addWidget(self.executeBarButton)
        self.helpBarButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.helpBarButton.sizePolicy().hasHeightForWidth())
        self.helpBarButton.setSizePolicy(sizePolicy)
        self.helpBarButton.setMinimumSize(QtCore.QSize(75, 20))
        self.helpBarButton.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.helpBarButton.setFont(font)
        self.helpBarButton.setObjectName("helpBarButton")
        self.horizontalLayout_3.addWidget(self.helpBarButton)
        spacerItem = QtWidgets.QSpacerItem(230, 20, QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(28, 36, QtWidgets.QSizePolicy.Policy.Fixed,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.categoryName = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoryName.sizePolicy().hasHeightForWidth())
        self.categoryName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.categoryName.setFont(font)
        self.categoryName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.categoryName.setObjectName("categoryName")
        self.horizontalLayout_5.addWidget(self.categoryName)
        spacerItem2 = QtWidgets.QSpacerItem(28, 20, QtWidgets.QSizePolicy.Policy.Fixed,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_5)
        spacerItem3 = QtWidgets.QSpacerItem(130, 20, QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.runButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setMaximumSize(QtCore.QSize(25, 25))
        self.runButton.setStyleSheet("background: none; border: none;")
        self.runButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.iconsDir + "Run.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.runButton.setIcon(icon)
        self.runButton.setIconSize(QtCore.QSize(25, 25))
        self.runButton.setObjectName("runButton")
        self.horizontalLayout.addWidget(self.runButton)
        self.debugButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.debugButton.sizePolicy().hasHeightForWidth())
        self.debugButton.setSizePolicy(sizePolicy)
        self.debugButton.setMaximumSize(QtCore.QSize(25, 25))
        self.debugButton.setStyleSheet("background: none; border: none;")
        self.debugButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.iconsDir + "Debug.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.debugButton.setIcon(icon1)
        self.debugButton.setIconSize(QtCore.QSize(25, 25))
        self.debugButton.setObjectName("debugButton")
        self.horizontalLayout.addWidget(self.debugButton)
        self.stopButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy)
        self.stopButton.setMaximumSize(QtCore.QSize(25, 25))
        self.stopButton.setStyleSheet("background: none; border: none;")
        self.stopButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.iconsDir + "Stop.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.stopButton.setIcon(icon2)
        self.stopButton.setIconSize(QtCore.QSize(25, 25))
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        spacerItem4 = QtWidgets.QSpacerItem(110, 20, QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(270, 20, QtWidgets.QSizePolicy.Policy.Fixed,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.scrollArea_2 = QtWidgets.QScrollArea(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy)
        self.scrollArea_2.setMinimumSize(QtCore.QSize(65, 0))
        self.scrollArea_2.setMaximumSize(QtCore.QSize(65, 16777215))
        self.scrollArea_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea_2.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.scrollArea_2.setWidgetResizable(False)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 79, 519))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(parent=self.scrollAreaWidgetContents_3)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(0, 0, 62, 431))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.group = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.group.setContentsMargins(0, 0, 0, 0)
        self.group.setSpacing(0)
        self.group.setObjectName("group")
        self.VariablesCategoryLayout = QtWidgets.QVBoxLayout()
        self.VariablesCategoryLayout.setObjectName("VariablesCategoryLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.VariablesCategoryButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VariablesCategoryButton.sizePolicy().hasHeightForWidth())
        self.VariablesCategoryButton.setSizePolicy(sizePolicy)
        self.VariablesCategoryButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.NoAntialias)
        self.VariablesCategoryButton.setFont(font)
        self.VariablesCategoryButton.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.VariablesCategoryButton.setAccessibleName("")
        self.VariablesCategoryButton.setStyleSheet("background: none; border: none;")
        self.VariablesCategoryButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.iconsDir + "Variable.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.VariablesCategoryButton.setIcon(icon3)
        self.VariablesCategoryButton.setIconSize(QtCore.QSize(50, 50))
        self.VariablesCategoryButton.setObjectName("VariablesCategoryButton")
        self.horizontalLayout_8.addWidget(self.VariablesCategoryButton)
        self.VariablesCategoryLayout.addLayout(self.horizontalLayout_8)
        self.VariablesCategoryLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VariablesCategoryLabel.sizePolicy().hasHeightForWidth())
        self.VariablesCategoryLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.VariablesCategoryLabel.setFont(font)
        self.VariablesCategoryLabel.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.VariablesCategoryLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.VariablesCategoryLabel.setObjectName("VariablesCategoryLabel")
        self.VariablesCategoryLayout.addWidget(self.VariablesCategoryLabel)
        self.group.addLayout(self.VariablesCategoryLayout)
        self.OperationsCategoryLayout = QtWidgets.QVBoxLayout()
        self.OperationsCategoryLayout.setSpacing(0)
        self.OperationsCategoryLayout.setObjectName("OperationsCategoryLayout")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.OperationsCategoryButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_7)
        self.OperationsCategoryButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.NoAntialias)
        self.OperationsCategoryButton.setFont(font)
        self.OperationsCategoryButton.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.OperationsCategoryButton.setAccessibleName("")
        self.OperationsCategoryButton.setStyleSheet("background: none; border: none;")
        self.OperationsCategoryButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.iconsDir + "Operators.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.OperationsCategoryButton.setIcon(icon4)
        self.OperationsCategoryButton.setIconSize(QtCore.QSize(50, 50))
        self.OperationsCategoryButton.setObjectName("OperationsCategoryButton")
        self.horizontalLayout_9.addWidget(self.OperationsCategoryButton)
        self.OperationsCategoryLayout.addLayout(self.horizontalLayout_9)
        self.OperationsCategoryLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OperationsCategoryLabel.sizePolicy().hasHeightForWidth())
        self.OperationsCategoryLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.OperationsCategoryLabel.setFont(font)
        self.OperationsCategoryLabel.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.OperationsCategoryLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.OperationsCategoryLabel.setObjectName("OperationsCategoryLabel")
        self.OperationsCategoryLayout.addWidget(self.OperationsCategoryLabel)
        self.group.addLayout(self.OperationsCategoryLayout)
        self.ControlCategoryLayout = QtWidgets.QVBoxLayout()
        self.ControlCategoryLayout.setObjectName("ControlCategoryLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.ControlCategoryButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_7)
        self.ControlCategoryButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.NoAntialias)
        self.ControlCategoryButton.setFont(font)
        self.ControlCategoryButton.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.ControlCategoryButton.setAccessibleName("")
        self.ControlCategoryButton.setStyleSheet("background: none; border: none;")
        self.ControlCategoryButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(self.iconsDir + "Control.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ControlCategoryButton.setIcon(icon5)
        self.ControlCategoryButton.setIconSize(QtCore.QSize(50, 50))
        self.ControlCategoryButton.setObjectName("ControlCategoryButton")
        self.horizontalLayout_10.addWidget(self.ControlCategoryButton)
        self.ControlCategoryLayout.addLayout(self.horizontalLayout_10)
        self.ControlCategoryLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ControlCategoryLabel.sizePolicy().hasHeightForWidth())
        self.ControlCategoryLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.ControlCategoryLabel.setFont(font)
        self.ControlCategoryLabel.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.ControlCategoryLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ControlCategoryLabel.setObjectName("ControlCategoryLabel")
        self.ControlCategoryLayout.addWidget(self.ControlCategoryLabel)
        self.group.addLayout(self.ControlCategoryLayout)
        self.Control2CategoryLayout = QtWidgets.QVBoxLayout()
        self.Control2CategoryLayout.setSpacing(0)
        self.Control2CategoryLayout.setObjectName("Control2CategoryLayout")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.Control2CategoryButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Control2CategoryButton.sizePolicy().hasHeightForWidth())
        self.Control2CategoryButton.setSizePolicy(sizePolicy)
        self.Control2CategoryButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.NoAntialias)
        self.Control2CategoryButton.setFont(font)
        self.Control2CategoryButton.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.Control2CategoryButton.setAccessibleName("")
        self.Control2CategoryButton.setStyleSheet("background: none; border: none;")
        self.Control2CategoryButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(self.iconsDir + "Control_1.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Control2CategoryButton.setIcon(icon6)
        self.Control2CategoryButton.setIconSize(QtCore.QSize(50, 50))
        self.Control2CategoryButton.setObjectName("Control2CategoryButton")
        self.horizontalLayout_11.addWidget(self.Control2CategoryButton)
        self.Control2CategoryLayout.addLayout(self.horizontalLayout_11)
        self.Control2CategoryLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Control2CategoryLabel.sizePolicy().hasHeightForWidth())
        self.Control2CategoryLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.Control2CategoryLabel.setFont(font)
        self.Control2CategoryLabel.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.Control2CategoryLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Control2CategoryLabel.setObjectName("Control2CategoryLabel")
        self.Control2CategoryLayout.addWidget(self.Control2CategoryLabel)
        self.group.addLayout(self.Control2CategoryLayout)
        self.SchemaCategoryLayout = QtWidgets.QVBoxLayout()
        self.SchemaCategoryLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.SchemaCategoryLayout.setSpacing(0)
        self.SchemaCategoryLayout.setObjectName("SchemaCategoryLayout")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.SchemaCategoryButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_7)
        self.SchemaCategoryButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.NoAntialias)
        self.SchemaCategoryButton.setFont(font)
        self.SchemaCategoryButton.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.SchemaCategoryButton.setAccessibleName("")
        self.SchemaCategoryButton.setStyleSheet("background: none; border: none;")
        self.SchemaCategoryButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(self.iconsDir + "Schema.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.SchemaCategoryButton.setIcon(icon7)
        self.SchemaCategoryButton.setIconSize(QtCore.QSize(50, 50))
        self.SchemaCategoryButton.setObjectName("SchemaCategoryButton")
        self.horizontalLayout_12.addWidget(self.SchemaCategoryButton)
        self.SchemaCategoryLayout.addLayout(self.horizontalLayout_12)
        self.SchemaCategoryLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SchemaCategoryLabel.sizePolicy().hasHeightForWidth())
        self.SchemaCategoryLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.SchemaCategoryLabel.setFont(font)
        self.SchemaCategoryLabel.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.SchemaCategoryLabel.setScaledContents(False)
        self.SchemaCategoryLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SchemaCategoryLabel.setObjectName("SchemaCategoryLabel")
        self.SchemaCategoryLayout.addWidget(self.SchemaCategoryLabel)
        self.group.addLayout(self.SchemaCategoryLayout)
        self.SpecialCategoryLayout = QtWidgets.QVBoxLayout()
        self.SpecialCategoryLayout.setObjectName("SpecialCategoryLayout")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.SpecialCategoryButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SpecialCategoryButton.sizePolicy().hasHeightForWidth())
        self.SpecialCategoryButton.setSizePolicy(sizePolicy)
        self.SpecialCategoryButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.NoAntialias)
        self.SpecialCategoryButton.setFont(font)
        self.SpecialCategoryButton.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.SpecialCategoryButton.setAccessibleName("")
        self.SpecialCategoryButton.setStyleSheet("background: none; border: none;")
        self.SpecialCategoryButton.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(self.iconsDir + "Special.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.SpecialCategoryButton.setIcon(icon8)
        self.SpecialCategoryButton.setIconSize(QtCore.QSize(50, 50))
        self.SpecialCategoryButton.setObjectName("SpecialCategoryButton")
        self.horizontalLayout_13.addWidget(self.SpecialCategoryButton)
        self.SpecialCategoryLayout.addLayout(self.horizontalLayout_13)
        self.SpecialCategoryLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SpecialCategoryLabel.sizePolicy().hasHeightForWidth())
        self.SpecialCategoryLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.SpecialCategoryLabel.setFont(font)
        self.SpecialCategoryLabel.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.SpecialCategoryLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpecialCategoryLabel.setObjectName("SpecialCategoryLabel")
        self.SpecialCategoryLayout.addWidget(self.SpecialCategoryLabel)
        self.group.addLayout(self.SpecialCategoryLayout)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_7.addWidget(self.scrollArea_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.block_list = QtWidgets.QScrollArea(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.block_list.sizePolicy().hasHeightForWidth())
        self.block_list.setSizePolicy(sizePolicy)
        self.block_list.setMaximumSize(QtCore.QSize(150, 16777215))
        self.block_list.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.block_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.block_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.block_list.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.block_list.setWidgetResizable(False)
        self.block_list.setObjectName("block_list")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 135, 468))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.scrollAreaWidgetContents_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 131, 511))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.block_list.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.block_list)
        self.tableView_6 = QtWidgets.QTableView(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_6.sizePolicy().hasHeightForWidth())
        self.tableView_6.setSizePolicy(sizePolicy)
        self.tableView_6.setMaximumSize(QtCore.QSize(150, 35))
        self.tableView_6.setObjectName("tableView_6")
        self.verticalLayout_2.addWidget(self.tableView_6)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.block_constructor = block_constructorr()
        self.block_constructor.setMinimumSize(QtCore.QSize(0, 0))
        self.block_constructor.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.block_constructor.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.block_constructor.setWidgetResizable(False)
        self.block_constructor.setObjectName("block_constructor")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -423, 100000, 100000))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(250, 250))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.block_constructor.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.block_constructor)
        self.tableView_7 = QtWidgets.QTableView(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_7.sizePolicy().hasHeightForWidth())
        self.tableView_7.setSizePolicy(sizePolicy)
        self.tableView_7.setMaximumSize(QtCore.QSize(1000000, 35))
        self.tableView_7.setObjectName("tableView_7")
        self.verticalLayout_3.addWidget(self.tableView_7)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.allBlocksInfoTextArea = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.allBlocksInfoTextArea.setReadOnly(True)
        self.allBlocksInfoTextArea.setMaximumSize(QtCore.QSize(267, 16777215))
        self.allBlocksInfoTextArea.setObjectName("allBlocksInfoTextArea")
        self.verticalLayout_4.addWidget(self.allBlocksInfoTextArea)
        self.currentBlockInfoTextArea = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.currentBlockInfoTextArea.setMaximumSize(QtCore.QSize(267, 16777215))
        self.currentBlockInfoTextArea.setObjectName("currentBlockInfoTextArea")
        self.currentBlockInfoTextArea.setReadOnly(True)
        self.verticalLayout_4.addWidget(self.currentBlockInfoTextArea)
        self.tableView_8 = QtWidgets.QTableView(parent=self.centralwidget)
        self.tableView_8.setMaximumSize(QtCore.QSize(267, 35))
        self.tableView_8.setObjectName("tableView_8")
        self.verticalLayout_4.addWidget(self.tableView_8)
        self.horizontalLayout_7.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        spacerItem6 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_5.addItem(spacerItem6)
        MainWindow.setCentralWidget(self.centralwidget)
        screen = QApplication.primaryScreen()

        width = win32api.GetSystemMetrics(0) // 2
        height = win32api.GetSystemMetrics(1) // 2

        window_width = MainWindow.width()
        window_height = MainWindow.height()

        self.retranslateUi(MainWindow)

        MainWindow.move(width // 2 - window_width // 2, height // 2 - window_height // 2 + 100)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.fileBarButton.clicked.connect(lambda: self.clicked(self, MainWindow))

    def clicked(self, elements, MainWindow):
        self.context_menu = QMenu()
        createProjectAction = self.context_menu.addAction("Создать")
        saveProjectAction = self.context_menu.addAction("Сохранить")
        loadProjectAction = self.context_menu.addAction("Загрузить")

        window_pos = MainWindow.pos()
        global_pos = MainWindow.mapToGlobal(window_pos)

        currentX = QCursor.pos().x()
        currentY = QCursor.pos().y()

        point = QPoint(currentX, currentY)

        createProjectAction.triggered.connect(lambda: self.createProject())
        saveProjectAction.triggered.connect(lambda: self.saveProject())
        loadProjectAction.triggered.connect(lambda: self.loadProject())

        self.context_menu.exec(point)

    def createProject(self): #Создание нового проекта
        global globalMainWindow
        MainWindow.needSave = False
        globalMainWindow.setWindowTitle("JofLang IDE - Untitled")
        for child in globalUi.block_constructor.findChildren(QtWidgets.QWidget):
            child.deleteLater()
        globalUi.currentBlockInfoTextArea.clear()
        globalUi.allBlocksInfoTextArea.clear()
        print("Создано!")

    def saveProject(self):
        global globalMainWindow
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        file_name = os.path.basename(file_path)

        if file_path:
            with open(file_path, 'w') as file:
                savingVisibleProjectInfo = globalUi.allBlocksInfoTextArea.toPlainText()
                file.write(savingVisibleProjectInfo)
            globalMainWindow.setWindowTitle("JofLang IDE - " + file_name.replace(".txt", ""))
            MainWindow.needSave = False
            print("Сохранено!")

    def loadProject(self):
        global globalMainWindow, globalUi
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt")])
        if file_path:  # Проверяем, что пользователь выбрал файл
            file_name = os.path.basename(file_path)
            with open(file_path, 'r') as file:
                file_content = file.read()

            # Поиск строки, содержащей "Blocks Info:"
            blocks_info_index = file_content.find("Blocks Info:")

            # Если строка найдена, разделить содержимое файла на строки
            if blocks_info_index != -1:
                lines_after_blocks_info = file_content[blocks_info_index + len("Blocks Info:"):].splitlines()[
                                          1:-1]  # Избавляемся от первой и последней строки после "Blocks Info:"
                # Инициализация списка для хранения данных блоков
                blocks_data = []
                for line in lines_after_blocks_info:
                    # Пропустить пустые строки
                    if line.strip():
                        # Разделить строку по пробелам и добавить данные в список
                        blocks_data.append(line.strip().split())

                # Теперь в blocks_data содержатся данные блоков
                print(f"Загружен файл: {file_name}")
                print("Содержимое файла:")

                for child in globalUi.scrollAreaWidgetContents.findChildren(QtWidgets.QWidget):
                    child.deleteLater()

                for block in blocks_data:
                    globalUi.scrollAreaWidgetContents.newBlock = BlockForField(block[0], block[1], block[2], block[3], block[4],
                                                                        block[5], block[6], block[7], block[8])
                    globalUi.scrollAreaWidgetContents.newBlock.setGeometry(0, 0, 100, 100)
                    globalUi.scrollAreaWidgetContents.newBlock.setParent(globalUi.scrollAreaWidgetContents)
                    globalUi.scrollAreaWidgetContents.newBlock.setStyleSheet("background-color: rgb(0, 170, 255);")
                    globalUi.scrollAreaWidgetContents.newBlock.show()
                    print(block)

                MainWindow.needSave = False
            else:
                print("Не найдена информация о блоках в файле.")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.fileBarButton.setText(_translate("MainWindow", "Файл"))
        self.optionsBarButton.setText(_translate("MainWindow", "Опции"))
        self.executeBarButton.setText(_translate("MainWindow", "Выполнение"))
        self.helpBarButton.setText(_translate("MainWindow", "Помощь"))
        self.categoryName.setText(_translate("MainWindow", "Название категории"))
        self.VariablesCategoryLabel.setText(_translate("MainWindow", "Переменные"))
        self.OperationsCategoryLabel.setText(_translate("MainWindow", "Операторы"))
        self.ControlCategoryLabel.setText(_translate("MainWindow", "Контроль"))
        self.Control2CategoryLabel.setText(_translate("MainWindow", "Контроль_2"))
        self.SchemaCategoryLabel.setText(_translate("MainWindow", "Схема"))
        self.SpecialCategoryLabel.setText(_translate("MainWindow", "Особенное"))
