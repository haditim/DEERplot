import matplotlib.pyplot as plt
import csv
import os
from numpy import *
from collections import namedtuple
import datetime
import time
import sys
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import style
from itertools import cycle
from matplotlib import colors as mcolors

defColorArr = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
defCol = cycle(defColorArr)

class fn():
    def __init__(self, dataFile, folder = '', dataType = ''):
        self.folder = os.path.dirname(dataFile) if os.path.exists(dataFile) else os.path.dirname(os.path.join(folder, dataFile))
        if dataType == 'sim':
            self.distr_file = os.path.basename(dataFile)
            self.distr_ax = []
            self.distr_ax = loadtxt(os.path.join(self.folder, self.distr_file), unpack=True)
            self.title = self.distr_file[:len(self.distr_file) - 4]
        else:
            self.bckg_file = os.path.basename(dataFile)
            self.raw_file = self.bckg_file[:len(self.bckg_file) - 8]
            self.fit_file = self.raw_file + 'fit.dat'
            self.distr_file = self.raw_file + 'distr.dat'
            try:
                date = self.bckg_file[:8]
                self.date = datetime.date(int(date[:4]), int(date[4:6]), int(date[6:8]))
                self.title = self.bckg_file[9:len(self.bckg_file) - 9]
            except ValueError:
                try:
                    self.date = datetime.date.fromtimestamp(os.path.getmtime(os.path.join(self.folder, self.bckg_file)))
                except:
                    self.date = datetime.date(2013,01,01)
                    self.title = self.bckg_file[:len(self.bckg_file) - 9]
            self.BckgIsValid = False if self.bckg_file[len(self.bckg_file) - 8:len(self.bckg_file) - 4] != 'bckg' else True
            self.bckg_ax = []
            self.fit_ax = []
            self.distr_ax = []
            self.bckg_ax = loadtxt(os.path.join(self.folder, self.bckg_file), unpack=True)
            self.fit_ax = loadtxt(os.path.join(self.folder, self.fit_file), unpack=True)
            self.distr_ax = loadtxt(os.path.join(self.folder, self.distr_file), unpack=True)
            #self.res_lines = [line.rstrip('\n') for line in open(os.path.join(self.folder, self.res_file))]

def plot(
        deerFolder = '',
        filesArr = [],
        titlesArr = [],
        deerColors = [],
        backgroundColors = [],
        offsetArr = [],
        mLineWidthArr = [],
        oLineWidthArr = [],
        deerDistOffset = [],
        simFolder = '',
        simFiles = [],
        simTitles = [],
        simColors = [],
        plotType = '3plots',
        simDistOffset = [],
        distanceXlim = [],
        suptitle = '',
        plotFolder = os.path.realpath(__file__),
        rmFitDistr = [],
        plotExts = ['png'],
        dateInPlot = False,
        showPlot = True,
        timeTraceXlim = [],
        fitXlim = [],
        figSize = (14.4, 9.6),
        figDpi = 250,
        figStyle = 'seaborn-whitegrid',  # seaborn-whitegrid, ggplot, bmh, fivethirtyeight, You can find all in here: http://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
        figGrid = True,
):
    style.use(figStyle)
    #Handling Offset for '3plotsWoffset'
    maxDistrInt = 0
    if plotType == '3plotsWoffset':
        if filesArr:
            for i, val in enumerate(filesArr):
                try:
                    data = fn(val, deerFolder)
                    if i not in rmFitDistr:
                        intMax = max(data.distr_ax[1]/((trapz(data.distr_ax[1], x=data.distr_ax[0])/len(data.distr_ax[1]))))
                        maxDistrInt = intMax if intMax>maxDistrInt else maxDistrInt
                except Exception as e:
                    print "I could not find the file: ",val," ignoring this entry ... ", e
                    continue
        if simFiles:
            for i, val in enumerate(simFiles):
                try:
                    data = fn(val, simFolder, dataType='sim')
                    intMax = max(data.distr_ax[1]/((trapz(data.distr_ax[1], x=data.distr_ax[0])/len(data.distr_ax[1]))))
                    maxDistrInt = intMax if intMax>maxDistrInt else maxDistrInt
                except Exception as e:
                    print "I could not find the file: ",val," ignoring this entry ... ", e
                    continue
    if plotType == '4plots':
        fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)
        fig.set_size_inches(figSize[0], figSize[1], forward=True)
        st = fig.suptitle(suptitle, fontsize="x-large")
    elif plotType == '3plots' or plotType == '3plotsWoffset':
        fig = plt.figure()
        ax0 = plt.subplot2grid((2,2),(0,0))
        ax1 = plt.subplot2grid((2,2),(1,0))
        ax2 = plt.subplot2grid((2,2),(0,1), rowspan=2)
        fig.set_size_inches(figSize[0], figSize[1], forward=True)
        st = fig.suptitle(suptitle, fontsize="x-large")
    if filesArr:
        for i, val in enumerate(filesArr):
            try:
                data = fn(val, deerFolder)
            except:
                print "I could not find the file: ",val," ignoring this entry ..."
                continue
            offset = offsetArr[i] if len(offsetArr)>=len(filesArr) else i*.1
            colMain = deerColors[i] if len(deerColors)==len(filesArr) else next(defCol)
            colOffset = backgroundColors[i] if len(backgroundColors)==len(filesArr) else ('black' if colMain != 'black' else 'gray')
            mLineWidth = mLineWidthArr[i] if len(mLineWidthArr)==len(filesArr) else 4
            oLineWidth = oLineWidthArr[i] if len(oLineWidthArr)==len(filesArr) else 2.5
            title = titlesArr[i] if len(titlesArr)==len(filesArr) else data.title.replace('_',' ')
            distrOff = deerDistOffset[i]*maxDistrInt if len(deerDistOffset)==len(filesArr) else 0
            if len(timeTraceXlim) == 2:
                min_x = min(data.bckg_ax[0][logical_and(data.bckg_ax[0]<timeTraceXlim[1], data.bckg_ax[0]>timeTraceXlim[0])])
                min_y = min(min(data.bckg_ax[1][logical_and(data.bckg_ax[0]<timeTraceXlim[1], data.bckg_ax[0]>timeTraceXlim[0])]-float(offset)),min(data.bckg_ax[2][logical_and(data.bckg_ax[0]<timeTraceXlim[1], data.bckg_ax[0]>timeTraceXlim[0])]-float(offset)))
                max_x = max(data.bckg_ax[0][logical_and(data.bckg_ax[0]<timeTraceXlim[1], data.bckg_ax[0]>timeTraceXlim[0])])
                max_y = max(max(data.bckg_ax[1][logical_and(data.bckg_ax[0]<timeTraceXlim[1], data.bckg_ax[0]>timeTraceXlim[0])]),max(data.bckg_ax[2][logical_and(data.bckg_ax[0]<timeTraceXlim[1], data.bckg_ax[0]>timeTraceXlim[0])]))
            else:
                min_x = min(data.bckg_ax[0])
                min_y = min(min(data.bckg_ax[1]-float(offset)),min(data.bckg_ax[2]-float(offset)))
                max_x = max(data.bckg_ax[0])
                max_y = max(max(data.bckg_ax[1]),max(data.bckg_ax[2]))
            ax0.plot(data.bckg_ax[0],data.bckg_ax[1]-offset, label=title, color="%s" % colMain, linewidth=mLineWidth)
            ax0.plot(data.bckg_ax[0],data.bckg_ax[2]-offset, label=None, color="%s" % colOffset, linewidth=oLineWidth)
            ax0.set_ylabel('V(t)/V(0)', weight='bold')
            ax0.set_xlabel(r'time [$\mu s$]', weight='bold')
            ax0.set_xlim(min_x,max_x)
            ax0.set_ylim(min_y-.02,max_y+.02)
            ax0.set_title('DEER trace + fitted background')
            leg = ax0.legend(loc='upper right', ncol=1, fontsize=8, frameon=True)
            min_y=max_y=0.9
            min_x=0.1
            max_=0.6
            if len(fitXlim) == 2:
                min_x = min(data.fit_ax[0][logical_and(data.fit_ax[0]<fitXlim[1], data.fit_ax[0]>fitXlim[0])])
                min_y = min(min(data.fit_ax[1][logical_and(data.fit_ax[0]<fitXlim[1], data.fit_ax[0]>fitXlim[0])]-float(offset)),min(data.fit_ax[2][logical_and(data.fit_ax[0]<fitXlim[1], data.fit_ax[0]>fitXlim[0])]-float(offset)))
                max_x = max(data.fit_ax[0][logical_and(data.fit_ax[0]<fitXlim[1], data.fit_ax[0]>fitXlim[0])])
                max_y = max(max(data.fit_ax[1][logical_and(data.fit_ax[0]<fitXlim[1], data.fit_ax[0]>fitXlim[0])]),max(data.fit_ax[2][logical_and(data.fit_ax[0]<fitXlim[1], data.fit_ax[0]>fitXlim[0])]))
            min_x = min(min_x,min(data.fit_ax[0]))
            min_y = min(min_y,min(data.fit_ax[1]-offset),min(data.fit_ax[2]-offset))
            max_x = max(max_x,max(data.fit_ax[0]))
            max_y = max(max_y,max(data.fit_ax[1]),max(data.fit_ax[2]))
            ax1.plot(data.fit_ax[0],data.fit_ax[1]-offset, label=title, color="%s" % colMain, linewidth=mLineWidth)
            if i not in rmFitDistr:
                ax1.plot(data.fit_ax[0],data.fit_ax[2]-offset, label=None, color="%s" % colOffset, linewidth=oLineWidth)
            ax1.set_ylabel('F(t)/F(0)', weight='bold')
            ax1.set_xlabel(r'time [$\mu s$]', weight='bold')
            ax1.set_xlim(0,max_x)
            ax1.set_ylim(min_y-.02,max_y+.02)
            ax1.set_title('Form factor + fitted distance function')
            if i not in rmFitDistr:
                if distanceXlim:
                    ax2.plot(data.distr_ax[0][logical_and(data.distr_ax[0]<distanceXlim[1], data.distr_ax[0]>distanceXlim[0])],data.distr_ax[1][logical_and(data.distr_ax[0]<distanceXlim[1], data.distr_ax[0]>distanceXlim[0])]/((trapz(data.distr_ax[1][logical_and(data.distr_ax[0]<distanceXlim[1], data.distr_ax[0]>distanceXlim[0])], x=data.distr_ax[0][logical_and(data.distr_ax[0]<distanceXlim[1], data.distr_ax[0]>distanceXlim[0])])/len(data.distr_ax[1][logical_and(data.distr_ax[0]<distanceXlim[1], data.distr_ax[0]>distanceXlim[0])])))+distrOff, color="%s" % colMain, linewidth=mLineWidth)
                else:
                    ax2.plot(data.distr_ax[0],data.distr_ax[1]/((trapz(data.distr_ax[1], x=data.distr_ax[0])/len(data.distr_ax[1])))+distrOff, color="%s" % colMain, linewidth=mLineWidth)
                ax2.set_ylabel('P(r)', weight='bold')
                ax2.set_xlabel(r'distance [$nm$]', weight='bold')
                ax2.set_title('Distance distribution normalized to area')
                ax2.set_yticks([])
                ax2.set_ylim(0,maxDistrInt*(1+max(deerDistOffset)))
                if distanceXlim: ax2.set_xlim(distanceXlim[0],distanceXlim[1])
                if plotType == '4plots':
                    ax3.plot(data.distr_ax[0],data.distr_ax[1]/max(data.distr_ax[1]), label=title, color="%s" % colMain, linewidth=mLineWidth)
                    ax3.set_ylabel('P(r)', weight='bold')
                    ax3.set_xlabel(r'distance [$nm$]', weight='bold')
                    ax3.set_title('Distance distribution normalized to max.')
                    ax3.set_yticks([])
    if simFiles:
        for i, val in enumerate(simFiles):
            try:
                data = fn(val, simFolder, dataType='sim')
            except:
                print "I could not find the file: ",val," ignoring this entry ..."
                continue
            colMain = simColors[i] if len(simColors)==len(simFiles) else defColorArr[i]
            mLineWidth = mLineWidthArr[i] if len(mLineWidthArr)==len(filesArr) else 4
            title = simTitles[i] if len(simTitles)==len(simFiles) else data.title.replace('_',' ')
            distrOffSim = simDistOffset[i]*maxDistrInt if len(simDistOffset)==len(simFiles) else 0
            ax2.bar(data.distr_ax[0],data.distr_ax[1]/((trapz(data.distr_ax[1], x=data.distr_ax[0])/len(data.distr_ax[1]))), label=title, color="%s" % colMain, linewidth=mLineWidth, alpha=0.2, width=      data.distr_ax[0][1]-data.distr_ax[0][0], bottom=distrOffSim)
            ax2.legend(loc='upper right', ncol=1, fontsize=8, frameon=True)
            if plotType == '4plots':
                ax3.bar(data.distr_ax[0],data.distr_ax[1]/max(data.distr_ax[1]), label=title, color="%s" % colMain, linewidth=mLineWidth, alpha=0.2, width=data.distr_ax[0][1]-data.distr_ax[0][0])
            
    #fig.set_size_inches(30, fig.get_figheight(), forward=True)
    #bbox = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    #width, height, dpi = bbox.width*fig.dpi, bbox.height*fig.dpi, fig.dpi
    if not figGrid:
        for i, ax in enumerate(fig.axes):
            ax.grid(False)
    if plotExts:
        #print plotFolder
        for val in plotExts:
            figName = os.path.join(os.path.dirname(plotFolder),os.path.basename(plotFolder),time.strftime("%Y%m%d-")+suptitle.replace(' ','-')+"-PLOT."+val) if dateInPlot else os.path.join(os.path.dirname(plotFolder),os.path.basename(plotFolder),suptitle.replace(' ','-')+"-PLOT."+val)
            try:
                fig.tight_layout()
                fig.savefig(figName, bbox_inches=0, dpi=figDpi, transparent=True)
                #print "Figure saved: ",figName
            except Exception as e:
                print e
    if showPlot:
        fig.tight_layout()
        plt.show(block=True)
        plt.close("all")
    else:
        plt.close("all")
    return figName[:-4]

