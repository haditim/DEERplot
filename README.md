# DEERplot
DEERplot plots the output from however many DeerAnalysis files that you created and compare them for you and saves the PDF file. For a complete description and downloading packaged .exe file please refer to my website: <a href="http://www.spintoolbox.com/en/offline-tools/deer-plot/">spintoolbox.com</a>
![Sample output](https://https://github.com/haditim/DEERplot/Sample_output.png)
## DEERplot.py and DEERplot_noGUI.py
If you want to use the UI for selecting the files and ploting them interactively, you can use DEERplot.py. The downside though is that you do not get the python code saved anywhere so that it can be changed later on or new data files can be added to it. For removing this problem I added DEERplot_noGUI.py which is essentially only the plot() function to which the filenames, colors, etc. are passed as arrays.
*Please make sure that you have dependencies installed on you system*

## Use DEERplot_noGUI.py with seperate files
You can do the following when using DEERplot_noGUI.py:
```python
from DEERplot_noGUI import *

# Enter the folder name for DeerAnalysis files. You can also leave this empty and add folder to file names
deerFolder = ''
# Enter DeerAnalysis files list here
deerFiles = ['apo_d2_2200ns_DEER_bckg.dat','VO_d2_2200ns_DEER_bckg.dat']
# Enter titles if you want
deerTitles = ['apo','VO']
# And colors if you want
deerColors = ['cyan','magenta']
# Offset for time trace and form factor
offsetArr = [0, .2]
# upper panel or lower panel in distance dist. (only used when using plotType='3plotsWoffset')
deerDistOffset = [0, 1]
# Enter the folder name for simulation files. You can also leave this empty and add folder to file names
simFolder = ''
# Simulations file names
simFiles = ['[4Q4H](A){1}271_[4Q4H](A){1}54_distr.dat']
# Titles for simulation
simTitles = ['4Q4H apo crystal']
# Simulations colors
simColors = ['black']
# upper panel or lower panel in distance dist. (only used when using plotType='3plotsWoffset')
simDistOffset = [0]
# x-range for distance distribution plots. You can also leave this empty
distanceXlim = [1,8]
# Finally, we call the function to plot
plot(
        deerFolder = deerFolder,
        filesArr = deerFiles,
        titlesArr = deerTitles,
        deerColors = deerColors,
        backgroundColors = [], # Color array for backgrounds 
        offsetArr = offsetArr,
        mLineWidthArr = [], # LW for all plots
        oLineWidthArr = [], # LW for time trace and form factor offsets
        deerDistOffset = deerDistOffset,
        simFolder = simFolder,
        simFiles = simFiles,
        simTitles = simTitles,
        simColors = simColors,
        plotType='3plotsWoffset', #'4plots','3plots' and '3plotsWoffset'
        simDistOffset = simDistOffset,
        distanceXlim = [1.3,8]
)
```
If you do not want to copy DEERplot_noGUI.py to every folder you can put it somewhere and do the following on top of your python file:
``` python
import sys
sys.path.insert(0, '/mnt/RUBfileShare/Codes/Python/DEERplot/')
from DEERplot_noGUI import *
```