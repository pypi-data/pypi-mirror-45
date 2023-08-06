import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from cal_event_search.Form import Ui_Form


def run():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

