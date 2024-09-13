#=========================================================================================
# Author: Patrick Brockmann CEA/DRF/LSCE - September 2024
#=========================================================================================

import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import ConnectionPatch
from matplotlib.lines import Line2D
import matplotlib.patches as patches
from scipy import interpolate

import matplotlib as mpl

mpl.rcParams['toolbar'] = 'None'
mpl.rcParams['axes.labelsize'] = 10
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8

#=========================================================================================
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
coordsX1 = []
coordsX2 = []
curve1 = None
curve2 = None
curve2Interp = None
x1 = None
y1 = None
x2 = None
y2 = None
x2Interp = None
showInterp = False

curve1Color = 'red'
curve2Color = 'forestgreen'

#=========================================================================================
def readData(file, x1Name, y1Name, x2Name, y2Name):
    global x1, y1, x2, y2

    try:
        df = pd.read_csv(file)
        #print(df.columns)

        x1 = df[x1Name].to_numpy()
        y1 = df[y1Name].to_numpy()
        x2 = df[x2Name].to_numpy()
        y2 = df[y2Name].to_numpy()

    except:
        print("Error: reading data file")

#=========================================================================================
def readPointers(file):
    global coordsX1, coordsX2

    try:
        df = pd.read_csv(file, names=['coordsX1','coordsX2'])
        print(df.to_string(index=False, header=False, float_format="%.8f"))
        coordsX1 = df['coordsX1'].to_numpy()
        coordsX2 = df['coordsX2'].to_numpy()

    except:
        print("Error: reading pointers file")

#=========================================================================================
def updateConnections():

    for artistsList in artistsList_Dict.values():
        if isinstance(artistsList[0], ConnectionPatch):
            connect = artistsList[0]
            x1, y1 = connect.xy1
            connect.xy1 = (x1, axs[0].get_ylim()[0]) 
            x2, y2 = connect.xy2
            connect.xy2 = (x2, axs[1].get_ylim()[1])
            if ((axs[0].get_xlim()[0] < x1 < axs[0].get_xlim()[1]) and
                (axs[1].get_xlim()[0] < x2 < axs[1].get_xlim()[1])):
                connect.set_visible(True)
            else:
                connect.set_visible(False)

#=========================================================================================
def drawConnections(interpolate=False):
    global artistsList_Dict, vline1List, vline2List

    for objectId in artistsList_Dict.keys():
        for artist in artistsList_Dict[objectId]:
            artist.remove()
    artistsList_Dict = {}
    vline1List = []
    vline2List = []

    for i in range(len(coordsX1)):
        coordX1 = coordsX1[i]
        coordX2 = coordsX2[i]
        if interpolate: coordX2 = coordX1
        vline1 = axs[0].axvline(coordX1, color='b', alpha=0.5, linestyle='--', linewidth=1, label='vline')
        vline2 = axs[1].axvline(coordX2, color='b', alpha=0.5, linestyle='--', linewidth=1, label='vline')
        vline1List.append(vline1)
        vline2List.append(vline2)
        connect = ConnectionPatch(color='b', alpha=0.5, linewidth=1, picker=5, clip_on=True, label='connection',
                    xyA=(coordX1, axs[0].get_ylim()[0]), coordsA=axs[0].transData,
                    xyB=(coordX2, axs[1].get_ylim()[1]), coordsB=axs[1].transData)
        fig.add_artist(connect)
        artistsList_Dict[id(connect)] = [connect, vline1, vline2]

    axs[0].autoscale()
    axs[1].autoscale()
    updateConnections()

#=========================================================================================
def displayInterp(visible):
    global x2Interp, curve2Interp

    if len(vline1List) <= 1:
        print("Warning: interpolation needs a minimum of 2 pointers")
        return 

    if curve2Interp:
        curve2Interp.remove()
        curve2Interp = None
        x2Interp = []

    if visible:
        cur_xlim = axs[0].get_xlim()
        axsInterp.set_visible(True)
        coordsX1 = sorted([float(line.get_xdata()[0]) for line in vline1List])
        coordsX2 = sorted([float(line.get_xdata()[0]) for line in vline2List])
        f = interpolate.interp1d(coordsX2, coordsX1, fill_value="extrapolate")
        x2Interp = f(x2)
        curve2Interp, = axsInterp.plot(x2Interp, y2, color=curve2Color, linewidth=0.5)
        axsInterp.set_xlim(cur_xlim)
        axsInterp.set_ylabel(y2Name)
        plt.draw()
    else:
        axsInterp.set_visible(False)
        plt.draw()

#=========================================================================================
def onPick(event):
    global vline1, vline2, artistsList_Dict, vline1List, vline2List

    artistLabel = event.artist.get_label()
    #print(artistLabel)

    #-----------------------------------------------
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

    #-----------------------------------------------
    elif artistLabel == 'curve':
        if key_shift:
            coordPoint = [event.mouseevent.xdata, event.mouseevent.ydata]
            if event.artist == curve1:
                if vline1 != None:
                    vline1.set_data([coordPoint[0], coordPoint[0]], [0,1])
                else:
                    vline1 = axs[0].axvline(coordPoint[0], color='b', alpha=0.5, linestyle='--', linewidth=1, label='vline')
            elif event.artist == curve2:
                if vline2 != None:
                    vline2.set_data([coordPoint[0], coordPoint[0]], [0,1])
                else:
                    vline2 = axs[1].axvline(coordPoint[0], color='b', alpha=0.5, linestyle='--', linewidth=1, label='vline')
            plt.draw()

    #-----------------------------------------------
    elif artistLabel == 'points':
        if key_control:
            ind = event.ind[0]
            if event.artist == points1:
                coordPoint = [x1[ind], y1[ind]]
                if vline1 != None:
                    vline1.set_data([coordPoint[0], coordPoint[0]], [0,1])
                else:
                    vline1 = axs[0].axvline(coordPoint[0], color='b', linestyle='--', linewidth=1, label='vline')
            elif event.artist == points2:
                coordPoint = [x2[ind], y2[ind]]
                if vline2 != None:
                    vline2.set_data([coordPoint[0], coordPoint[0]], [0,1])
                else:
                    vline2 = axs[1].axvline(coordPoint[0], color='b', linestyle='--', linewidth=1, label='vline')
            plt.draw()

#=========================================================================================
def zoom(event):
    
    if event.inaxes in axs:
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
        
        updateConnections()
        event.inaxes.figure.canvas.draw()
    
#=========================================================================================
def onKeyPress(event):
    global key_x, key_shift, key_control, vline1, vline2
    global showInterp

    sys.stdout.flush()

    #-----------------------------------------------
    if event.key == 'a':
        linecursor1.set_visible(False)
        linecursor2.set_visible(False)

        axs[0].autoscale()
        axs[1].autoscale()
        ylim_axs0 = axs[0].get_ylim()
        ylim_axs1 = axs[1].get_ylim()

        curve1.set_visible(False)
        curve2.set_visible(False)
        if curve2Interp: curve2Interp.set_visible(False)
        axs[0].relim(visible_only=True)
        axs[1].relim(visible_only=True)
        axsInterp.relim(visible_only=True)
        curve1.set_visible(True)
        curve2.set_visible(True)
        if curve2Interp: curve2Interp.set_visible(showInterp)
        plt.draw()

        axs[0].set_ylim(ylim_axs0)
        axs[1].set_ylim(ylim_axs1)

        updateConnections()
        plt.draw()

    #-----------------------------------------------
    if event.key == 'x':
        key_x = True

    #-----------------------------------------------
    if event.key == 'c':
        if vline1 != None and vline2 != None :
            coordX1 = float(vline1.get_xdata()[0])
            coordX2 = float(vline2.get_xdata()[0])
            # Check positions
            coordsX1 = [float(line.get_xdata()[0]) for line in vline1List]
            coordsX2 = [float(line.get_xdata()[0]) for line in vline2List]
            if np.searchsorted(coordsX1, coordX1) != np.searchsorted(coordsX2, coordX2):
                print("Error: Connection not possible because it would cross existing connections") 
                return
            connect = ConnectionPatch(color='b', alpha=0.5, linewidth=1, picker=5, clip_on=True, label='connection',
                        xyA=(coordX1, axs[0].get_ylim()[0]), coordsA=axs[0].transData,
                        xyB=(coordX2, axs[1].get_ylim()[1]), coordsB=axs[1].transData)
            fig.add_artist(connect)
            artistsList_Dict[id(connect)] = [connect, vline1, vline2]
            vline1List.append(vline1)
            vline2List.append(vline2)
            vline1 = None
            vline2 = None
        
            displayInterp(showInterp)
            plt.draw()

    #-----------------------------------------------
    elif event.key == 'h':
        print('''
===============================================================================
Press h
    Display this help 
-------------------------------------------------------------------------------
Hold shift key while right click on a curve
    Create or move a pointer
-------------------------------------------------------------------------------
Hold down ctrl key on a plot
    Display points of the curve
-------------------------------------------------------------------------------
Hold down ctrl key on a plot while right click on a curve
    Create or move a pointer hooked on a point
-------------------------------------------------------------------------------
Press c key
    Connect pointers
-------------------------------------------------------------------------------
Hold down x key while right click on a connection
    Delete the connection and its associated pointers
-------------------------------------------------------------------------------
Use wheel mouse on a plot
    Zoom in/out in the plot
-------------------------------------------------------------------------------
Hold down right key mouse on a plot
    Pan in the plot
-------------------------------------------------------------------------------
Hold down left key mouse on a plot
    Expand horizontal/vertical axis depending horizontal/vertical movement
-------------------------------------------------------------------------------
Press p key
    Save figure as pdf file
-------------------------------------------------------------------------------
Press i key
    Save pointers to csv file
-------------------------------------------------------------------------------
Press z key
    Display/Hide interpolated curve
-------------------------------------------------------------------------------
Press s key
    Save data to csv file
-------------------------------------------------------------------------------
Press q key
    Quit
===============================================================================
''')

    #-----------------------------------------------
    elif event.key == 'p':
        plt.savefig('figure.pdf')
        print("Info: saved pdf in file figure.pdf")

    #-----------------------------------------------
    elif event.key == 's':
        df = pd.DataFrame({x1Name: x1, y1Name: y1, x2Name: x2, y2Name: y2, 
                           y2Name + ' interpolated on ' + x1Name: x2Interp})
        print("Info: saved data in file data.csv")
        df.to_csv('data.csv', index=False, float_format="%.8f")

    #-----------------------------------------------
    elif event.key == 'i':
        coordsX1 = sorted([float(line.get_xdata()[0]) for line in vline1List])
        coordsX2 = sorted([float(line.get_xdata()[0]) for line in vline2List])
        df = pd.DataFrame({'coordsX1': coordsX1, 'coordsX2': coordsX2})
        print("Info: saved pointers in file pointers.csv")
        df.to_csv('pointers.csv', index=False, header=False, float_format="%.8f")
        print(df.to_string(index=False, header=False, float_format="%.8f"))

    #-----------------------------------------------
    elif event.key == 'z':
        showInterp = not showInterp
        displayInterp(showInterp)

    #-----------------------------------------------
    elif event.key == 'shift':
        key_shift = True

    #-----------------------------------------------
    elif event.key == 'control':
        key_control = True
        if event.inaxes == axs[0]:
            points1.set_visible(True)
        elif event.inaxes == axs[1]:
            points2.set_visible(True)
        plt.draw()

#=========================================================================================
def onKeyRelease(event):
    global key_x, key_shift, key_control

    sys.stdout.flush()

    #-----------------------------------------------
    if event.key == 'x':
        key_x = False

    #-----------------------------------------------
    elif event.key == 'shift':
        key_shift = False 

    #-----------------------------------------------
    elif event.key == 'control':
        key_control = False 
        if event.inaxes == axs[0]:
            points1.set_visible(False)
        elif event.inaxes == axs[1]:
            points2.set_visible(False)
        plt.draw()

#=========================================================================================
def onPress(event):
    global cur_xlim, cur_ylim, press, xpress, ypress, mousepress

    if event.inaxes not in axs: return

    #-----------------------------------------------
    if event.button == 3:
        mousepress = 'right'

    #-----------------------------------------------
    elif event.button == 1:
        mousepress = 'left'

    cur_xlim = event.inaxes.get_xlim()
    cur_ylim = event.inaxes.get_ylim()
    press = event.xdata, event.ydata
    xpress, ypress = press

#=========================================================================================
def onRelease(event):
    global press
    press = None

#=========================================================================================
def onMotion(event):
    global cur_xlim, cur_ylim, press

    #-----------------------------------------------
    if event.inaxes not in axs:
        press = None
        linecursor1.set_visible(False)
        linecursor2.set_visible(False)
        plt.draw()
        return

    #-----------------------------------------------
    if event.inaxes is axs[0]:
        linecursor1.set_visible(True)
        linecursor2.set_visible(False)
        linecursor1.set_xdata([event.xdata])
    elif event.inaxes is axs[1]:
        linecursor1.set_visible(False)
        linecursor2.set_visible(True)
        linecursor2.set_xdata([event.xdata])
    event.inaxes.figure.canvas.draw()

    #-----------------------------------------------
    if press is None: return

    #-----------------------------------------------
    if mousepress == 'left':
        linecursor1.set_visible(False)
        linecursor2.set_visible(False)
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        cur_xlim -= dx
        cur_ylim -= dy
        event.inaxes.set_xlim(cur_xlim[0], cur_xlim[1])
        event.inaxes.set_ylim(cur_ylim[0], cur_ylim[1])

    #-----------------------------------------------
    elif mousepress == 'right':
        linecursor1.set_visible(False)
        linecursor2.set_visible(False)
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        zoomFactor = 1.2 
        event.inaxes.set_xlim(cur_xlim[0] + dx * zoomFactor, cur_xlim[1] - dx * zoomFactor)
        event.inaxes.set_ylim(cur_ylim[0] + dy * zoomFactor, cur_ylim[1] - dy * zoomFactor)

    updateConnections()
    event.inaxes.figure.canvas.draw()
    event.inaxes.figure.canvas.flush_events()
    
##########################################################################################
# python lineage.py testFile.csv 'Time (ka)' 'Stack Benthic d18O (per mil)' 'depthODP849cm' 'd18Oforams-b' pointers1.csv

fileData = sys.argv[1]
x1Name = sys.argv[2]
y1Name = sys.argv[3]
x2Name = sys.argv[4]
y2Name = sys.argv[5]
filePointers = sys.argv[6]

#=========================================================================================
readData(fileData, x1Name, y1Name, x2Name, y2Name)

#=========================================================================================
fig, axs = plt.subplots(2, 1, figsize=(10,8), num='Lineage')

#=========================================================================================
curve1, = axs[0].plot(x1, y1, color=curve1Color, picker=True, pickradius=20, linewidth=0.5, label='curve') 
points1 = axs[0].scatter(x1, y1, s=5, marker='o', color=curve1Color, picker=True, pickradius=20, label='points')
points1.set_visible(False)
linecursor1 = axs[0].axvline(color='k', alpha=0.25, linewidth=1)
axs[0].grid(visible=True, which='major', color='lightgray', linestyle='dashed', linewidth=0.5)
axs[0].set_xlabel(x1Name)
axs[0].set_ylabel(y1Name)
axs[0].patch.set_alpha(0)
axs[0].autoscale()

#=========================================================================================
curve2, = axs[1].plot(x2, y2, color=curve2Color, picker=True, pickradius=20, linewidth=0.5, label='curve')
points2 = axs[1].scatter(x2, y2, s=5, marker='o', color=curve2Color, picker=True, pickradius=20, label='points')
points2.set_visible(False)
linecursor2 = axs[1].axvline(color='k', alpha=0.25, linewidth=1)
axs[1].grid(visible=True, which='major', color='lightgray', linestyle='dashed', linewidth=0.5)
axs[1].set_xlabel(x2Name)
axs[1].set_ylabel(y2Name)
axs[1].autoscale()

#=========================================================================================
axsInterp = axs[0].twinx()
axsInterp.set_ylabel(y2Name)
axsInterp.set_zorder(-10)
axsInterp.set_visible(showInterp)

#=========================================================================================
fig.canvas.mpl_connect('key_press_event', onKeyPress)
fig.canvas.mpl_connect('key_release_event', onKeyRelease)
fig.canvas.mpl_connect('button_press_event',onPress)
fig.canvas.mpl_connect('button_release_event',onRelease)
fig.canvas.mpl_connect('motion_notify_event',onMotion)
fig.canvas.mpl_connect('pick_event', onPick)
fig.canvas.mpl_connect('scroll_event', zoom)

#=========================================================================================
readPointers(filePointers)
drawConnections()

#=========================================================================================
plt.show()
