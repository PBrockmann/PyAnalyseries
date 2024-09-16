import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    #------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        label = QtWidgets.QLabel("Hello!")
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.setCentralWidget(label)

        button1_action = QtWidgets.QAction("Your button1", self)
        button1_action.setStatusTip("This is your button1")
        button1_action.triggered.connect(self.onMyToolBarButtonClick)

        button2_action = QtWidgets.QAction("Your button2", self)
        button2_action.setStatusTip("This is your button2")
        button2_action.triggered.connect(self.onMyToolBarButtonClick)

        exit_action = QtWidgets.QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit")
        exit_action.triggered.connect(self.exitCall)

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(button1_action)
        file_menu.addAction(button2_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        about_menu = menu.addMenu("&About")

        self.setStatusBar(QtWidgets.QStatusBar(self))
        
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.setCentralWidget(sc)

        self.show()

    #------------------------------------------------------------------
    def onMyToolBarButtonClick(self):
        print("click")

    #------------------------------------------------------------------
    def exitCall(self):
        self.close()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
