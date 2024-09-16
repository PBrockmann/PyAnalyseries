import sys
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas

from PyQt5.Qt import Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#======================================================
version = "v0.90"

#======================================================

class MainWindow(QMainWindow):

    #------------------------------------------------------------------
    def __init__(self, *args, **kwargs):

        QMainWindow.__init__(self)

        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.xpress = None
        self.ypress = None
        self.mousepress = None

        self.setMinimumSize(QSize(1000, 800))   
        self.setWindowTitle("My Awesome App")

        button1Action = QAction("Your button1", self)
        button1Action.setStatusTip("This is your button1")
        button1Action.triggered.connect(self.buttonCall)

        button2Action = QAction("Your button2", self)
        button2Action.setStatusTip("This is your button2")
        button2Action.triggered.connect(self.buttonCall)

        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit")
        exitAction.triggered.connect(self.exitCall)

        aboutAction = QAction('&About', self)
        aboutAction.setShortcut('F1')
        aboutAction.setStatusTip('About the application')
        aboutAction.triggered.connect(self.aboutCall)

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(button1Action)
        file_menu.addAction(button2Action)
        file_menu.addSeparator()
        file_menu.addAction(exitAction)

        about_menu = menu.addMenu("&About")
        about_menu.addAction(aboutAction)

        self.setStatusBar(QStatusBar(self))
       
        self.fig, self.axs = plt.subplots(nrows=1, figsize=(8,8))

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFocusPolicy(Qt.ClickFocus)
        self.canvas.setFocus()

        self.canvas.mpl_connect('button_press_event', self.onPress)
        self.canvas.mpl_connect('button_release_event', self.onRelease)
        self.canvas.mpl_connect('motion_notify_event', self.onMotion)
        self.canvas.mpl_connect('scroll_event', self.zoom)

        self.setCentralWidget(self.canvas)

        self.axs.plot([0,1,2,3,4], [10,1,20,3,40])
        self.axs.grid(visible=True, which='major', color='lightgray', linestyle='dashed', linewidth=0.5)

        self.canvas.draw()

    #------------------------------------------------------------------
    def buttonCall(self):
        print("click")

    #------------------------------------------------------------------
    def aboutCall(self):
        msg = " Application " + version + """

         * Open an image, optionnaly with a scale and value scale annotation
         * Define new scale and scale value if needed
         * Save the image and the data points, visualize the extracted profile

         * Developped by Patrick Brockmann (LSCE)
        """
        QMessageBox.about(self, "About the Application", msg.strip())

    #------------------------------------------------------------------
    def exitCall(self):
        self.close()

    #------------------------------------------------------------------
    def onPress(self, event):
        if event.inaxes != self.axs: return
        if event.button == 3:
            self.mousepress = "right"
        elif event.button == 1:
            self.mousepress = "left"
        self.cur_xlim = self.axs.get_xlim()
        self.cur_ylim = self.axs.get_ylim()
        self.press = event.xdata, event.ydata
        self.xpress, self.ypress = self.press

    #------------------------------------------------------------------
    def onRelease(self, event):
        self.press = None
        self.axs.figure.canvas.draw()
    
    #------------------------------------------------------------------
    def onMotion(self, event):
        if self.press is None: return
        if event.inaxes != self.axs: return
        if self.mousepress == "left":
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            event.inaxes.set_xlim(self.cur_xlim)
            event.inaxes.set_ylim(self.cur_ylim)
            event.inaxes.figure.canvas.draw()
        elif self.mousepress == "right":
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            event.inaxes.set_xlim([self.cur_xlim[0] + dx, self.cur_xlim[1] - dx])
            event.inaxes.set_ylim([self.cur_ylim[0] + dy, self.cur_ylim[1] - dy])
            event.inaxes.figure.canvas.draw()

    #------------------------------------------------------------------
    def zoom(self, event):
        
        if event.inaxes == self.axs:
            scale_zoom = 1.2
            cur_xlim = event.inaxes.get_xlim()
            cur_ylim = event.inaxes.get_ylim()
            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
            if event.button == 'up':                        # zoom in
                scale_factor = 1 / scale_zoom
            elif event.button == 'down':                    # zoom out
                scale_factor = scale_zoom
            else:
                # deal with something that should never happen
                scale_factor = 1
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
            
            event.inaxes.set_xlim(xdata - new_width * (1-relx), xdata + new_width * (relx))
            event.inaxes.set_ylim(ydata - new_height * (1-rely), ydata + new_height * (rely))
            event.inaxes.figure.canvas.draw()
        
#======================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
