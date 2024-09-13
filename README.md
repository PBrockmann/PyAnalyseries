# PyAnalyseries

Python version for Analyseries

Select interactively match points on 2 curves to visualize the resulting interpolated curve. 

Based on:
 * matplotlib
 * scipy

## Usage

```python lineage.py testFile.csv 'Time (ka)' 'Stack Benthic d18O (per mil)' 'depthODP849cm' 'd18Oforams-b' pointers2.csv```

## Help

```
===============================================================================
Press 'h'
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
Press 'c' key
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
Press 'a' key on a plot
    Plot the 2 curves with an automatic vertical range and a horizontal range according to pointers
-------------------------------------------------------------------------------
Press 'A' key on a plot
    Plot the curve with automatic vertical and horizontal ranges
-------------------------------------------------------------------------------
Press 'p' key
    Save figure as pdf file
-------------------------------------------------------------------------------
Press 'i' key
    Save pointers to csv file
-------------------------------------------------------------------------------
Press 'z' key
    Display/Hide interpolated curve
-------------------------------------------------------------------------------
Press 's' key
    Save data to csv file
-------------------------------------------------------------------------------
Press 'q' key
    Quit the application
===============================================================================
```
 
## Captures

![Capture 01](pngFile_lineage_01.png)  

![Capture 02](pngFile_lineage_02.png)  

![Capture 03](pngFile_lineage_03.png)  
