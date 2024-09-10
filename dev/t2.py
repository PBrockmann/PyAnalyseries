#=========================================================================================
import pandas as pd

df = pd.read_csv('testFile.csv')

x1 = df['Time (ka)'].to_numpy()
y1 = df['Stack Benthic d18O (per mil)'].to_numpy()
x2 = df['depthODP849cm'].to_numpy()
y2 = df['d18Oforams-b'].to_numpy()

#=========================================================================================
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch
from matplotlib.lines import Line2D
import matplotlib.patches as patches

import matplotlib as mpl

plt.rc('xtick',labelsize=8)
plt.rc('ytick',labelsize=8)
plt.rcParams['toolbar'] = 'None'

#==========================================================
fig, axs = plt.subplots(2, 1, figsize=(10,8))

#======================================================
line1 = Line2D(x1, y1, color='red', picker=True, pickradius=5, linewidth=0.5)
axs[0].add_artist(line1)
axs[0].grid(visible=True, which='major', color='lightgray', linestyle='dashed', linewidth=0.5)
axs[0].set_xlim(min(x1), max(x1))
axs[0].set_ylim(min(y1), max(y1))
linecursor1 = axs[0].axvline(color='k', alpha=0.2)

#======================================================
line2 = Line2D(x2, y2, color='steelblue', picker=True, pickradius=5, linewidth=0.5)
axs[1].add_artist(line2)
axs[1].grid(visible=True, which='major', color='lightgray', linestyle='dashed', linewidth=0.5)
axs[1].set_xlim(min(x2), max(x2))
axs[1].set_ylim(min(y2), max(y2))
linecursor2 = axs[1].axvline(color='k', alpha=0.2)

#======================================================
pressX = False
point1 = None
point2 = None
vline1 = None
vline2 = None
connect = None

def onpickLine(event):
        global point1, point2, vline1, vline2, connect
        #print(event.artist)
        if isinstance(event.artist, ConnectionPatch):
                print("connection picked")
                if pressX:
                        event.artist.remove()
                        plt.draw()
        elif isinstance(event.artist, Line2D):
                thisline = event.artist
                xdata = thisline.get_xdata()
                ydata = thisline.get_ydata()
                ind = event.ind
                coordPoint = [xdata[ind][0], ydata[ind][0]]
                print('onpick point:', coordPoint)
                if thisline == line1:
                        print("line 1 picked")
                        if point1 != None:
                            point1.set_data([coordPoint[0]], [coordPoint[1]])
                            vline1.set_data([coordPoint[0], coordPoint[0]], [0,1])
                        else:
                            point1, = axs[0].plot(coordPoint[0], coordPoint[1], marker='o', color='b')
                            vline1 = axs[0].axvline(coordPoint[0], color='b', linestyle='--', lw=1)
                        plt.draw()
                elif thisline == line2:
                        print("line 2 picked")
                        if point2 != None:
                            point2.set_data([coordPoint[0]], [coordPoint[1]])
                            vline2.set_data([coordPoint[0], coordPoint[0]], [0,1])
                        else:
                            point2, = axs[1].plot(coordPoint[0], coordPoint[1], marker='o', color='b')
                            vline2 = axs[1].axvline(coordPoint[0], color='b', linestyle='--', lw=1)
                if point1 != None and point2 != None :
                        print(point1.get_data()[0], axs[0].get_ylim()[0])
                        connect = ConnectionPatch(color='b', picker=5, clip_on=True,
                                xyA=(point1.get_xdata()[0], axs[0].get_ylim()[0]), coordsA=axs[0].transData,
                                xyB=(point2.get_xdata()[0], axs[1].get_ylim()[1]), coordsB=axs[1].transData)
                        fig.add_artist(connect)
                        point1 = None
                        point2 = None
                plt.draw()

fig.canvas.mpl_connect('pick_event', onpickLine)

#======================================================
def onpress(event):
    global pressX
    #print('press', event.key)
    sys.stdout.flush()
    if event.key == 'x':
        pressX = True

#======================================================
def onmove(event):
    if not event.inaxes: return
    if event.inaxes is axs[0]: 
        linecursor1.set_xdata([event.xdata])
    elif event.inaxes is axs[1]: 
        linecursor2.set_xdata([event.xdata])
    plt.draw()

#======================================================
def func(axes):
    print("New axis y-limits are", axes.get_ylim())

cb_registry = axs[0].callbacks
cid = cb_registry.connect('ylim_changed', func)

#======================================================
fig.canvas.mpl_connect('key_press_event', onpress)
fig.canvas.mpl_connect('motion_notify_event', onmove)

plt.show()
