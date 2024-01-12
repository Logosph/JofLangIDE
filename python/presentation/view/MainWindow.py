from resources.layout.python.window_main import *
import sys
from MainWindowPresenter import MainWindowPresenter

presenter = MainWindowPresenter()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

ui.one_button.clicked.connect(presenter.button_clicked)

MainWindow.show()
sys.exit(app.exec_())
