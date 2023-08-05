#!/usr/bin/env python3
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.
#
# The authors acknowledge that this material is based upon work supported 
# by the U.S. Department of Energy’s Office of Energy Efficiency and Renewable
# Energy (EERE) under Solar Energy Technologies Office (SETO) Agreement 
# Number DE-EE0007536.
#
# This work is the combined efforts of ASU, First Solar, SJSU and Purdue 
# University. People involved in this project are
# Abdul Rawoof Shaik (ASU)
# Christian Ringhofer (ASU)
# Dragica Vasileska (ASU)
# Daniel Brinkman (SJSU)
# Igor Sankin (FSLR)
# Dmitry Krasikov (FSLR)
# Hao Kang (Purdue)
# Benes Bedrich (Purdue)
#
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 23:37:28 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

from PyQt5.QtWidgets import (
        QAction,QMessageBox
        )

from PyQt5.QtGui import (
        QIcon
        )

from PyQt5.QtCore import (
        Qt
        )

fac=100

prec=6

colorList=[Qt.red,Qt.green,Qt.blue,Qt.cyan,
           Qt.magenta,Qt.yellow]
bStyleList=[Qt.SolidPattern,Qt.Dense7Pattern,Qt.HorPattern,Qt.VerPattern,
            Qt.CrossPattern,Qt.BDiagPattern,Qt.FDiagPattern,Qt.DiagCrossPattern]

def parseString(inputStr):
    if inputStr is not None:
        str1=inputStr.replace("(","")
        str2=str1.replace(")","")
        return str2.split(",")
    else:
        return None

def restoreString(listVal):
    if listVal is not None:
        tempStr=','.join(listVal)
        return "("+tempStr+")"
    else:
        return None
    
def tupleString(tupleVal):
    out=""
    if tupleVal is not None:
        out="("
        for ii in range(len(tupleVal)):
            if ii==0:
                out=out+"{0},".format(tupleVal[ii])
            else:
                out=out+"({0},{1})".format(tupleVal[ii][0],tupleVal[ii][1])
        out=out+")"
    return out
    
def isElectron(inputStr):
    eList=['e_{c}^{-}'
            ]
    return inputStr in eList

def isHole(inputStr):
    eList=['h_{v}^{+}'
            ]
    return inputStr in eList

def createTBAction(iconImageName,tbName,statusTip,
                                     toolTip,isEnabled,slotName,parent):
    
#        QMessageBox.about("Warning","Inside Mode 1 GeoMode 0 Widget")
#    print("Test")
    qa=QAction(QIcon(iconImageName),tbName,parent)
    if statusTip is not None:
        qa.setStatusTip(statusTip)
    if toolTip is not None:
        qa.setToolTip(toolTip)
    qa.setEnabled(isEnabled)
    if slotName is not None:
        qa.triggered.connect(slotName)
    return qa

def getTimeInSeconds(inVal,inUnits):
    outVal=inVal
    found=False
    
    if inUnits.lower() == "s".lower():
        outVal=inVal
        found=True
        
    if inUnits.lower() == "min".lower():
        outVal=inVal*60
        found=True
        
    if inUnits.lower() == "hrs".lower():
        outVal=inVal*60*60
        found=True
        
    if inUnits.lower() == "days".lower():
        outVal=inVal*60*60*24
        found=True
        
    if inUnits.lower() == "weeks".lower():
        outVal=inVal*60*60*24*7
        found=True
        
    if inUnits.lower() == "months".lower():
        outVal=inVal*60*60*24*30
        found=True
        
    if inUnits.lower() == "Years".lower():
        outVal=inVal*60*60*24*365
        found=True
        
    if inUnits.lower() == "Years".lower():
        outVal=inVal*60*60*24*3650
        found=True
        
    if not found:
        print("unknown units for time:{0}".format(inUnits))
    
    return outVal
        
        
def getTempInKelvin(inVal,inUnits):
    outVal=inVal
    found=False
    
    if inUnits.lower() == "K".lower():
        outVal=inVal
        found=True
        
    if inUnits.lower() == "C".lower():
        outVal=inVal+273
        found=True
        
    if not found:
        print("unknown units for time:{0}".format(inUnits))
        
    return outVal

def getInterpolatedVal(dataList,xVal,yVal):
    if len(dataList[0])==1:
        return dataList[2][0]
    
def getBCInterpolatedVal(dataList,xVal,yVal):
    if len(dataList[0])==1:
        return dataList[2][0],dataList[3][0]
        