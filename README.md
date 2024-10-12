# PyAnalyseries

Python version for Analyseries

Select interactively match points on 2 curves to visualize the resulting interpolated curve. 

Based on:
 * matplotlib
 * scipy
 * openpyxl

## Captures

![Capture 01](savePyAnalyseries_pngFile_01.png)  

![Capture 02](savePyAnalyseries_pngFile_02.png)  

## Usage

```
####################################################################################################################
Usage:  PyAnalyseries_v1.0.py [-h]
        [-k kindInterpolation]
        fileXLSX

Options:
        -h, -?, --help, -help
                Print this manual
        -k, --kind
                Interpolation kind 'linear' or 'quadratic' (default 'linear')

Examples:
        PyAnalyseries_v1.0.py testFile.xlsx
```

## Interactions 

```
####################################################################################################################
Interactions:

-------------------------------------------------------------------------------
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
Use wheel mouse on axis
    Zoom in/out on horizontal/vertical axis
-------------------------------------------------------------------------------
Hold down right key mouse on a plot
    Pan in the plot
-------------------------------------------------------------------------------
Press 'a' key on a plot
    Plot the 2 curves with an automatic vertical range and a horizontal range according to pointers
-------------------------------------------------------------------------------
Press 'A' key on a plot
    Plot the curve with automatic vertical and horizontal ranges
-------------------------------------------------------------------------------
Press 'p' key
    Save figure as pdf file and png file
-------------------------------------------------------------------------------
Press 'X' key
    Delete all pointers and connections 
-------------------------------------------------------------------------------
Press 'z' key
    Display/Hide interpolated curve
-------------------------------------------------------------------------------
Press 's' key
    Save data and pointers as excel file
-------------------------------------------------------------------------------
Press 'q' key
    Quit the application
```
 
