import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from Form import Ui_Form


if __name__ == '__main__':
    # connect()
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
