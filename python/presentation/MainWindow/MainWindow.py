from resources.layout.python.window_main import *
import sys

def execute():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # На label ui.runButton навешиваем обработчик события нажатия
    ui.runButton.clicked.connect(lambda: print('Hello, World!'))

    MainWindow.show()
    sys.exit(app.exec())
