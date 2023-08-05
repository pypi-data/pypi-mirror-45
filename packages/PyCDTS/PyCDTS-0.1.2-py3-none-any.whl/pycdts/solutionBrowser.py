#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 23:04:35 2018

@author: abdul
"""
#from Project import Project
import matplotlib.pyplot as plt
plt.switch_backend('Qt5Agg')
import matplotlib as mpl
import numpy as np
from cycler import cycler
#import PyQt5 as qt

class SolutionBrowser():
    def __init__(self,project):
        self.proj=project
        self.numEng=project.numEng
#        qApp = qt.QtWidgets.QApplication(sys.argv)
        
    def startInteractive(self):
        print("Starting Interactive Plotting\n")
        plt.rc('axes', prop_cycle=(cycler('linestyle', ['-', '--', ':', '-.']))*cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']))
        fig,ax=plt.subplots()
        for jj in range(0,self.numEng.M):
            ax.loglog(self.proj.tOut[0,:],self.proj.uOut[jj,:]+np.spacing(1),label=self.numEng.Species[jj],linewidth=3.0)
        plt.legend(loc='upper right',bbox_to_anchor=(1.04,1)).draggable()
        plt.grid(True)
        plt.show()