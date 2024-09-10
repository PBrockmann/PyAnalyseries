import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import numpy as np

class SnaptoCursor(object):
    def __init__(self, ax, x, y):
        self.ax = ax
        self.ly = ax.axvline(color='k', alpha=0.2)  # the vert line
        self.marker, = ax.plot([0],[0], marker="o", color="crimson", zorder=3) 
        self.x = x
        self.y = y
        self.txt = ax.text(0.7, 0.9, '')

    def mouse_move(self, event):
        if not event.inaxes: return
        x, y = event.xdata, event.ydata
        indx = min(np.searchsorted(self.x, x), self.x.size-1)
        print(np.searchsorted(self.x, [x])[0])
        x = self.x[indx]
        y = self.y[indx]
        self.ly.set_xdata([x])
        self.marker.set_data([x],[y])
        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        self.txt.set_position((x,y))
        self.ax.figure.canvas.draw_idle()

t = np.arange(0.0, 1.0, 0.1)
s = np.sin(2*2*np.pi*t)
fig, ax = plt.subplots()

#cursor = Cursor(ax)
cursor = SnaptoCursor(ax, t, s)
cid =  plt.connect('motion_notify_event', cursor.mouse_move)

ax.plot(t, s, marker='.')
plt.axis([0, 1, -1, 1])
plt.show()
