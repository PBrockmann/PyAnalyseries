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

#======================================================
key_x = False
key_shift = False
key_control = False
vline1 = None
vline2 = None
press = None
cur_xlim = None
cur_ylim = None
xpress = None
ypress = None
mousepress = None
artistsList_Dict = {} 
vline1List = []
vline2List = []

#------------------------------------------------------
# From https://matplotlib.org/stable/gallery/event_handling/pick_event_demo.html
def linePicker(line, mouseevent):
    """
    Find the points within a certain distance from the mouseclick in
    data coords and attach some extra attributes, pickx and picky
    which are the data points that were picked.
    """
    if mouseevent.xdata is None:
        return False, dict()

    if key_shift:
        print("shift")
        ind = None
        pickx = mouseevent.xdata
        picky = mouseevent.ydata
        props = dict(ind=ind, pickx=pickx, picky=picky)
        return True, props

    elif key_control:
        print("ctrl")
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        maxd = 0.05
        d = np.sqrt(
            #(xdata - mouseevent.xdata)**2 + (ydata - mouseevent.ydata)**2)
            (xdata - mouseevent.xdata)**2)
        ind, = np.nonzero(d <= maxd)
        print(ind)
        if len(ind):
            pickx = xdata[ind]
            picky = ydata[ind]
            props = dict(ind=ind, pickx=pickx, picky=picky)
            return True, props
        else:
            return False, dict()

    else:
            return False, dict()

#------------------------------------------------------
def onPick(event):
    global vline1, vline2, artistsList_Dict, vline1List, vline2List

    artistLabel = event.artist.get_label()
    #print(artistLabel)

    if artistLabel == 'connection':
        if key_x:
            objectId = id(event.artist)
            for artist in artistsList_Dict[objectId]:
                artist.remove()
                if artist in vline1List:
                    vline1List.remove(artist)
                if artist in vline2List:
                    vline2List.remove(artist)
            del artistsList_Dict[objectId]
            plt.draw()

    elif artistLabel == 'curve':

        #coordPoint = [event.pickx, event.picky]
        coordPoint = [event.mouseevent.xdata, event.mouseevent.ydata]

        if key_shift or key_control:
            if event.artist == curve1:
                if vline1 != None:
                    vline1.set_data([coordPoint[0], coordPoint[0]], [0,1])
                else:
                    vline1 = axs[0].axvline(coordPoint[0], color='b', linestyle='--', linewidth=1, label='vline')
                plt.draw()
            elif event.artist == curve2:
                if vline2 != None:
                    vline2.set_data([coordPoint[0], coordPoint[0]], [0,1])
                else:
                    vline2 = axs[1].axvline(coordPoint[0], color='b', linestyle='--', linewidth=1, label='vline')
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
    global key_x, key_shift, key_control, vline1, vline2

    sys.stdout.flush()

    if event.key == 'x':
        key_x = True

    if event.key == 'c':
        if vline1 != None and vline2 != None :
            coordx1 = float(vline1.get_xdata()[0])
            coordx2 = float(vline2.get_xdata()[0])
            connect = ConnectionPatch(color='b', picker=5, clip_on=True, label='connection',
                        xyA=(coordx1, axs[0].get_ylim()[0]), coordsA=axs[0].transData,
                        xyB=(coordx2, axs[1].get_ylim()[1]), coordsB=axs[1].transData)
            fig.add_artist(connect)
            artistsList_Dict[id(connect)] = [connect, vline1, vline2]
            vline1List.append(vline1)
            vline2List.append(vline2)
            vline1 = None
            vline2 = None
            plt.draw()

    elif event.key == 'i':
        print('Points1')
        coordX = [float(line.get_xdata()[0]) for line in vline1List]
        print(coordX)
        print('Points2')
        coordX = [float(line.get_xdata()[0]) for line in vline2List]
        print(coordX)

    elif event.key == 'shift':
        key_shift = True

    elif event.key == 'control':
        key_control = True
        if event.inaxes == axs[0]:
            curve1.set_markersize(2)
        elif event.inaxes == axs[1]:
            curve2.set_markersize(2)
        plt.draw()

#------------------------------------------------------
def onKeyRelease(event):
    global key_x, key_shift, key_control

    sys.stdout.flush()
    if event.key == 'x':
        key_x = False

    elif event.key == 'shift':
        key_shift = False 

    elif event.key == 'control':
        key_control = False 
        if event.inaxes == axs[0]:
            curve1.set_markersize(0)
        elif event.inaxes == axs[1]:
            curve2.set_markersize(0)
        plt.draw()

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
fig, axs = plt.subplots(2, 1, figsize=(10,8), num='Lineage')

#======================================================
curve1Color = 'red'
curve1 = Line2D(x1, y1, color=curve1Color, picker=True, pickradius=1, linewidth=0.5, label='curve', 
                marker='o', markersize=0 , markerfacecolor=curve1Color, markeredgecolor=curve1Color)
axs[0].add_artist(curve1)
axs[0].grid(visible=True, which='major', color='lightgray', linestyle='dashed', linewidth=0.5)
axs[0].set_xlim(min(x1), max(x1))
axs[0].set_ylim(min(y1), max(y1))

#======================================================
curve2Color = 'forestgreen'
curve2 = Line2D(x2, y2, color=curve2Color, picker=True, pickradius=1, linewidth=0.5, label='curve',
                marker='o', markersize=0 , markerfacecolor=curve2Color, markeredgecolor=curve2Color)
axs[1].add_artist(curve2)
axs[1].grid(visible=True, which='major', color='lightgray', linestyle='dashed', linewidth=0.5)
axs[1].set_xlim(min(x2), max(x2))
axs[1].set_ylim(min(y2), max(y2))

#======================================================
fig.canvas.mpl_connect('key_press_event', onKeyPress)
fig.canvas.mpl_connect('key_release_event', onKeyRelease)
fig.canvas.mpl_connect('button_press_event',onPress)
fig.canvas.mpl_connect('button_release_event',onRelease)
fig.canvas.mpl_connect('motion_notify_event',onMotion)
fig.canvas.mpl_connect('pick_event', onPick)
fig.canvas.mpl_connect('scroll_event', zoom)

#======================================================
plt.show()
