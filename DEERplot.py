import matplotlib.pyplot as plt
import csv
import os
import easygui
from numpy import *
from collections import namedtuple
import datetime
#import time
import sys
from matplotlib.backends.backend_pdf import PdfPages
from colour import Color

def main():
    while True:
        #get values from Plot_Data()
        plot, plot_legs, plot_figs = Plot_Data()
        #Show the user the plot with subplots for DEER
        plot.show(block=False)
        figManager = plot.get_current_fig_manager()
        figManager.window.showMaximized()
        #Uncomment for delay before asking for plot save
        # plot.pause(1)
        # time.sleep(10.5)
        pdf_con = easygui.buttonbox(msg='Proceed to saving summary PDF file?',
                                    choices=('Yes', 'No, start over', 'No, terminate'))
        if pdf_con == 'No, terminate':
            break
        elif pdf_con == 'No, start over':
            pass

        else:
            #Ask for the PDF file location
            pdf_file = easygui.filesavebox(msg='Please select the PDF file address', title='PDF dialog', default=None)
            #Check if the extension is missing
            if pdf_file[len(pdf_file) - 4:] == '.pdf' or pdf_file[len(pdf_file) - 4:] == '.PDF':
                plt.close("all")
                pass
            else:
                pdf_file = pdf_file + '.pdf'
            #Save each figure in one PDF page
            with PdfPages(pdf_file) as pdf:
                for fig, leg in zip(plot_figs, plot_legs):
                    pdf.savefig(fig, bbox_extra_artists=(leg,),
                                bbox_inches='tight')  # saves the current figure into a pdf page
            plt.close("all")
            break


def Plot_Data():
    class fn():
        def __init__(self, bckg_file):
            self.bckg_file = os.path.basename(bckg_file)
            self.folder = os.path.dirname(bckg_file)
            self.default_file = os.path.join(self.folder, self.bckg_file)
            self.raw_file = self.bckg_file[:len(self.bckg_file) - 8]
            self.fit_file = self.raw_file + 'fit.dat'
            self.distr_file = self.raw_file + 'distr.dat'
            #self.res_file = self.raw_file + 'res.txt'
        def BckgIsValid(self):
            if not self.bckg_file:
                return "User has canceled file selection"
            elif f.bckg_file[len(f.bckg_file) - 8:len(f.bckg_file) - 4] != 'bckg':
                return False
            else:
                return True
        def GetLabels(self):
            try:
                int(self.bckg_file[:8])
                date = self.bckg_file[:8]
                self.date = datetime.date(int(date[:4]), int(date[4:6]), int(date[6:8]))
                title = self.bckg_file[9:len(self.bckg_file) - 9]
            except ValueError:
                try:
                    self.date = datetime.date.fromtimestamp(os.path.getmtime(os.path.join(self.folder, self.bckg_file)))
                except:
                    self.date = datetime.date(2016,01,01)
                title = self.bckg_file[:len(self.bckg_file) - 9]

            self.title = title
        def GetValuesFromUser(self):
            self.values = easygui.multenterbox(msg = "Enter your information",
                        title = "Plot variables",
                        fields = ["Date of experiment (YYYY-MM-DD)","Title of the plot","Background and fit offset"
                                          ,"Data line color (e.g. red, #234567, etc.)", "Background color"
                                          , "Data linewidth", "Background linewidth"],
                        values = [self.date, self.title, off, col_arr[col_arr_ind], bg_col_arr[col_arr_ind], 2, 1])
            print int(self.values[0][:4]), int(self.values[0][5:7]), int(self.values[0][8:10])
            self.date = datetime.date(int(self.values[0][:4]), int(self.values[0][5:7]), int(self.values[0][8:10]))
            self.title = self.values[1]
            self.offset = self.values [2]
            self.col = self.values [3]
            self.bg_col = self.values [4]
            self.lw = self.values [5]
            self.bg_lw = self.values [6]
        def GetData(self):
            self.bckg_ax = []
            self.fit_ax = []
            self.distr_ax = []
            self.bckg_ax = loadtxt(os.path.join(self.folder, self.bckg_file), unpack=True)
            self.fit_ax = loadtxt(os.path.join(self.folder, self.fit_file), unpack=True)
            self.distr_ax = loadtxt(os.path.join(self.folder, self.distr_file), unpack=True)
            #self.res_lines = [line.rstrip('\n') for line in open(os.path.join(self.folder, self.res_file))]

    a = []
    off = 0
    col_arr = ['blue','red','green','magenta','cyan','black','purple','orange','brown']
    bg_col_arr = ['black','black','black','black','black','grey','black','black','black']
    col_arr_ind = 0
    f = easygui.fileopenbox(msg='Please select bckg file', filetypes=["*.dat"])
    if not f:
        sys.exit("Canceled by user")
    else:
        f = fn(f)
    if not f.BckgIsValid():
        f = fn(easygui.fileopenbox('Wrong file selected. Please select bckg file !'
                                   , default=f.default_file if f.default_file else ""))
    elif f.BckgIsValid() == True:
        f.GetLabels()
        f.GetValuesFromUser()
    elif "User" in f.BckgIsValid():
        print f.BckgIsValid()
        sys.exit("Canceled by user")

    a.append (f)


    while True:
        next_file = easygui.ccbox('Select another file for comparison?', title='Add data to plot', choices=('Yes', 'No'))
        if next_file == True:
            f = easygui.fileopenbox(msg='Please select bckg file', default=f.default_file if f.default_file else ""
                                       , filetypes=["*.dat"])
            if not f:
                break
            f = fn(f)
            off += .1
            col_arr_ind += 1
            next_file == False
            if not f.BckgIsValid():
                f = fn(easygui.fileopenbox('Wrong file selected. Please select bckg file !',
                                           default=f.bckg_file if f.bckg_file else ""))
            elif f.BckgIsValid() == True:
                f.GetLabels()
                f.GetValuesFromUser()
            elif "User" in f.BckgIsValid():
                print f.BckgIsValid()
                break
            a.append(f)
        else:
            break

    plot_figs = []
    plot_legs = []
    min_y=max_y=0.9
    min_x=0.1
    max_x=0.6
    fig_DEER = plt.figure(1)
    for i in a:
        i.GetData()
        min_x = min(min_x,min(i.bckg_ax[0]))
        min_y = min(min_y,min(i.bckg_ax[1]-float(i.offset)),min(i.bckg_ax[2]-float(i.offset)))
        max_x = max(max_x,max(i.bckg_ax[0]))
        max_y = max(max_y,max(i.bckg_ax[1]),max(i.bckg_ax[2]))
        plt.plot(i.bckg_ax[0],i.bckg_ax[1]-float(i.offset), label=i.title, color="%s" % Color(i.col)#, linewidth=i.lw
                 )
        plt.plot(i.bckg_ax[0],i.bckg_ax[2]-float(i.offset), label=None, color="%s" % Color(i.bg_col)#, linewidth=i.bg_lw
                 )
        plt.ylabel('V(t)/V(0)')
        plt.xlabel(r'time [$\mu s$]')
        plt.xlim(min_x,max_x)
        plt.ylim(min_y-.02,max_y+.02)
        plt.title('DEER trace + fitted background')
        leg = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
              fancybox=True, shadow=True, ncol=1)
    plot_figs.append(fig_DEER)
    plot_legs.append(leg)
    plt.close()
    plt.figure(5)
    plt.subplot(2,2,1)
    for i in a:
        i.GetData()
        min_x = min(min_x,min(i.bckg_ax[0]))
        min_y = min(min_y,min(i.bckg_ax[1]-float(i.offset)),min(i.bckg_ax[2]-float(i.offset)))
        max_x = max(max_x,max(i.bckg_ax[0]))
        max_y = max(max_y,max(i.bckg_ax[1]),max(i.bckg_ax[2]))
        plt.plot(i.bckg_ax[0],i.bckg_ax[1]-float(i.offset), label=i.title, color="%s" % Color(i.col)#, linewidth=i.lw
                 )
        plt.plot(i.bckg_ax[0],i.bckg_ax[2]-float(i.offset), label=None, color="%s" % Color(i.bg_col)#, linewidth=i.bg_lw
                 )
        plt.ylabel('V(t)/V(0)')
        plt.xlabel(r'time [$\mu s$]')
        plt.xlim(min_x,max_x)
        plt.ylim(min_y-.02,max_y+.02)
        plt.title('DEER trace + fitted background')
        leg = plt.legend(loc='upper center',
              fancybox=True, shadow=True, ncol=1)
    min_y=max_y=0.9
    min_x=0.1
    max_x=0.6
    fig_fit = plt.figure(2)
    for i in a:
        min_x = min(min_x,min(i.bckg_ax[0]))
        min_y = min(min_y,min(i.bckg_ax[1]-float(i.offset)),min(i.bckg_ax[2]-float(i.offset)))
        max_x = max(max_x,max(i.bckg_ax[0]))
        max_y = max(max_y,max(i.bckg_ax[1]),max(i.bckg_ax[2]))
        plt.plot(i.fit_ax[0],i.fit_ax[1]-float(i.offset), label=i.title, color="%s" % Color(i.col)#, linewidth=i.lw
                 )
        plt.plot(i.fit_ax[0],i.fit_ax[2]-float(i.offset), label=None, color="%s" % Color(i.bg_col)#, linewidth=i.bg_lw
                 )
        plt.ylabel('F(t)/F(0)')
        plt.xlabel(r'time [$\mu s$]')
        plt.xlim(0,max_x)
        plt.ylim(min_y-.02,max_y+.02)
        plt.title('Form factor + fitted distance function')
        leg = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
              fancybox=True, shadow=True, ncol=1)
    plot_figs.append(fig_fit)
    plot_legs.append(leg)
    plt.close()
    plt.figure(5)
    plt.subplot(2,2,2)
    for i in a:
        min_x = min(min_x,min(i.bckg_ax[0]))
        min_y = min(min_y,min(i.bckg_ax[1]-float(i.offset)),min(i.bckg_ax[2]-float(i.offset)))
        max_x = max(max_x,max(i.bckg_ax[0]))
        max_y = max(max_y,max(i.bckg_ax[1]),max(i.bckg_ax[2]))
        plt.plot(i.fit_ax[0],i.fit_ax[1]-float(i.offset), label=i.title, color="%s" % Color(i.col)#, linewidth=i.lw
                 )
        plt.plot(i.fit_ax[0],i.fit_ax[2]-float(i.offset), label=None, color="%s" % Color(i.bg_col)#, linewidth=i.bg_lw
                 )
        plt.ylabel('F(t)/F(0)')
        plt.xlabel(r'time [$\mu s$]')
        plt.xlim(0,max_x)
        plt.ylim(min_y-.02,max_y+.02)
        plt.title('Form factor + fitted distance function')

    fig_dist_int = plt.figure(3)
    for i in a:
        plt.plot(i.distr_ax[0],i.distr_ax[1]/(sum(i.distr_ax[1])*len(i.distr_ax[1])), label=i.title, color="%s" % Color(i.col)#, linewidth=i.lw
                 )
        plt.ylabel('P(r)')
        plt.xlabel(r'distance [$nm$]')
        plt.tick_params(left='on', top='on', right='on', bottom='on',
                        labelleft='off', labeltop='off', labelright='off', labelbottom='on')
        plt.title('Distance distribution normalized to area')
        leg = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
              fancybox=True, shadow=True, ncol=1)
    plot_figs.append(fig_dist_int)
    plot_legs.append(leg)
    plt.close()
    plt.figure(5)
    plt.subplot(2,2,3)
    for i in a:
        plt.plot(i.distr_ax[0],i.distr_ax[1]/(sum(i.distr_ax[1])*len(i.distr_ax[1])), label=i.title, color="%s" % Color(i.col)#, linewidth=i.lw
                 )
        plt.ylabel('P(r)')
        plt.xlabel(r'distance [$nm$]')
        plt.tick_params(left='on',  top='on', right='on', bottom='on',
                       labelleft='off', labeltop='off', labelright='off', labelbottom='on')
        plt.title('Distance distribution normalized to area')

    fig_dist_max = plt.figure(4)
    for i in a:
        plt.plot(i.distr_ax[0],i.distr_ax[1]/max(i.distr_ax[1]), label=i.title, color="%s" % Color(i.col)#, linewidth=i.lw
                 )
        plt.ylabel('P(r)')
        plt.xlabel(r'distance [$nm$]')
        plt.title('Distance distribution normalized to max.')
        leg = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
              fancybox=True, shadow=True, ncol=1)
    plot_figs.append(fig_dist_max)
    plot_legs.append(leg)
    plt.close()
    plt.figure(5)
    plt.subplot(2,2,4)
    for i in a:
        plt.plot(i.distr_ax[0],i.distr_ax[1]/max(i.distr_ax[1]), label=i.title, color="%s" % Color(i.col)#, linewidth=i.lw
                 )
        plt.ylabel('P(r)')
        plt.xlabel(r'distance [$nm$]')
        plt.title('Distance distribution normalized to max.')
    plt.subplots_adjust(
        left = 0.025,  # the left side of the subplots of the figure
        right = 0.99,  # the right side of the subplots of the figure
        bottom = 0.05,  # the bottom of the subplots of the figure
        top = 0.97,  # the top of the subplots of the figure
        wspace = 0.09,  # the amount of width reserved for blank space between subplots
        hspace = 0.25  # the amount of height reserved for white space between subplots
        )# the amount of height reserved for white space between subplots
    return plt, plot_legs, plot_figs

main()

