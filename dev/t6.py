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

mpl.rcParams['toolbar'] = 'None'
plt.rc('xtick',labelsize=8)
plt.rc('ytick',labelsize=8)

#==========================================================
fig, axs = plt.subplots(2, 1, figsize=(10,8), num='Lineage')

#======================================================
curve1Color = 'red'
curve1 = Line2D(x1, y1, color=curve1Color, picker=True, pickradius=5, linewidth=0.5, label='curve', 
                marker='o', markersize=2 , markerfacecolor=curve1Color, markeredgecolor=curve1Color)
axs[0].add_artist(curve1)
axs[0].grid(visible=True, which='major', color='lightgray', linestyle='dashed', linewidth=0.5)
axs[0].set_xlim(min(x1), max(x1))
axs[0].set_ylim(min(y1), max(y1))
linecursor1 = axs[0].axvline(color='k', alpha=0.2)

#======================================================
curve2Color = 'forestgreen'
curve2 = Line2D(x2, y2, color=curve2Color, picker=True, pickradius=5, linewidth=0.5, label='curve',
                marker='o', markersize=2 , markerfacecolor=curve2Color, markeredgecolor=curve2Color)
axs[1].add_artist(curve2)
axs[1].grid(visible=True, which='major', color='lightgray', linestyle='dashed', linewidth=0.5)
axs[1].set_xlim(min(x2), max(x2))
axs[1].set_ylim(min(y2), max(y2))
linecursor2 = axs[1].axvline(color='k', alpha=0.2)

#======================================================
keyX = False
keyShift = False
point1 = None
point2 = None
vsine1 = None
vline2 = None
press = None
cur_xlim = None
cur_ylim = None
xpress = None
ypress = None
mousepress = None
artistsList_Dict = {} 
point1List = []
point2List = []

#------------------------------------------------------
def onpickLine(event):
    global point1, point2, vline1, vline2, artistsList_Dict, point1List, point2List

    artistLabel = event.artist.get_label()
    print(artistLabel)

    if artistLabel == 'connection':
        if keyX:
            objectId = id(event.artist)
            for artist in artistsList_Dict[objectId]:
                artist.remove()
            del artistsList_Dict[objectId]
            plt.draw()

    elif artistLabel == 'vline':
        if keyShift:
            xdata = event.artist.get_xdata()
            ydata = event.artist.get_ydata()
            ind = event.ind[0]
            coordPoint = [xdata[ind], ydata[ind]]
            #point1.set_data([coordPoint[0]], [coordPoint[1]])
            event.artist.set_data([coordPoint[0], coordPoint[0]], [0,1])
            plt.draw()

    elif artistLabel == 'curve':
        if keyShift:
            xdata = event.artist.get_xdata()
            ydata = event.artist.get_ydata()
            ind = event.ind[0]
            coordPoint = [xdata[ind], ydata[ind]]
            if event.artist == curve1:
                if point1 == None:
                    point1, = axs[0].plot(coordPoint[0], coordPoint[1], marker='.', color='b')
                    vline1 = axs[0].axvline(coordPoint[0], color='b', linestyle='--', linewidth=1, picker=True, pickradius=5, label='vline')
                    plt.draw()
            elif event.artist == curve2:
                if point2 == None:
                    point2, = axs[1].plot(coordPoint[0], coordPoint[1], marker='.', color='b')
                    vline2 = axs[1].axvline(coordPoint[0], color='b', linestyle='--', linewidth=1, picker=True, pickradius=5, label='vline')
                    plt.draw()

        if point1 != None and point2 != None :
            connect = ConnectionPatch(color='b', picker=5, clip_on=True, label='connection',
                        xyA=(point1.get_xdata()[0], axs[0].get_ylim()[0]), coordsA=axs[0].transData,
                        xyB=(point2.get_xdata()[0], axs[1].get_ylim()[1]), coordsB=axs[1].transData)
            fig.add_artist(connect)
            artistsList_Dict[id(connect)] = [connect, point1, point2, vline1, vline2]
            point1List.append(point1)
            point2List.append(point2)
            point1 = None
            point2 = None
            plt.draw()

#------------------------------------------------------
def updateConnect():
    for artistsList in artistsList_Dict.values():
        if isinstance(artistsList[0], ConnectionPatch):
            connect = artistsList[0]
            x1, y1 = connect.xy1
            connect.xy1 = (x1, axs[0].get_ylim()[0]) 
            x2, y2 = connect.xy2
            connect.xy2 = (x2, axs[1].get_ylim()[1]) 

#------------------------------------------------------
def zoom(event):
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
    
    event.inaxes.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
    event.inaxes.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
    
    updateConnect()
    event.inaxes.figure.canvas.draw()
    
#------------------------------------------------------
def onKeyPress(event):
    global keyX, keyShift

    sys.stdout.flush()
    if event.key == 'x':
        keyX = True
    elif event.key == 'shift':
        keyShift = True

#------------------------------------------------------
def onKeyRelease(event):
    global keyX, keyShift

    sys.stdout.flush()
    if event.key == 'x':
        keyX = False 
    elif event.key == 'shift':
        keyShift = False 
    elif event.key == 'i':
        print('Points1')
        coordsX = [float(point.get_xdata()[0]) for point in point1List]
        coordsY = [float(point.get_ydata()[0]) for point in point1List]
        print(coordsX, coordsY)
        print('Points2')
        coordsX = [float(point.get_xdata()[0]) for point in point2List]
        coordsY = [float(point.get_ydata()[0]) for point in point2List]
        print(coordsX, coordsY)

#------------------------------------------------------
def onPress(event):
    global cur_xlim, cur_ylim, press, xpress, ypress, mousepress

    if event.inaxes not in axs: return

    if event.button == 3:
        mousepress = "right"
    elif event.button == 1:
        mousepress = "left"
    cur_xlim = event.inaxes.get_xlim()
    cur_ylim = event.inaxes.get_ylim()
    press = event.xdata, event.ydata
    xpress, ypress = press

#------------------------------------------------------
def onRelease(event):
    global press
    press = None

#------------------------------------------------------
def onMotion(event):
    global cur_xlim, cur_ylim, press

    if event.inaxes not in axs:
        press = None
        return

    if event.inaxes is axs[0]:
        linecursor1.set_xdata([event.xdata])
    elif event.inaxes is axs[1]:
        linecursor2.set_xdata([event.xdata])
    event.inaxes.figure.canvas.draw()

    if press is None: return

    if mousepress == "left":
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        cur_xlim -= dx
        cur_ylim -= dy
        event.inaxes.set_xlim(cur_xlim)
        event.inaxes.set_ylim(cur_ylim)
    elif mousepress == "right":
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        event.inaxes.set_xlim([cur_xlim[0] + dx, cur_xlim[1] - dx])
        event.inaxes.set_ylim([cur_ylim[0] + dy, cur_ylim[1] - dy])

    updateConnect()
    event.inaxes.figure.canvas.draw()
    

#======================================================
fig.canvas.mpl_connect('key_press_event', onKeyPress)
fig.canvas.mpl_connect('key_release_event', onKeyRelease)
fig.canvas.mpl_connect('button_press_event',onPress)
fig.canvas.mpl_connect('button_release_event',onRelease)
fig.canvas.mpl_connect('motion_notify_event',onMotion)
fig.canvas.mpl_connect('pick_event', onpickLine)
fig.canvas.mpl_connect('scroll_event', zoom)

#======================================================
plt.show()
