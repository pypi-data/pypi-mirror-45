#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:08:32 2018

@author: abdul
"""

from .diffusionSolver import DiffusionSolver
from .Berfun import Berfun
import numpy as np
import scipy.constants
import scipy.sparse as sps
import scipy.sparse.linalg as spsl

class simul_DS_ber(DiffusionSolver):
    def Solve(self,dt):
        out=np.array([])
        fi=self.numEng.fi_sol
        mG=self.numEng.mGrid
        Hx=mG.Hx
        Hy=mG.Hy
        hx=mG.hx
        hy=mG.hy
        
        u0=self.numEng.uD_solInit
        
        uSol=np.zeros((mG.nX*mG.nY,self.numEng.M))
        
        for ii in range(0,self.numEng.M):
            if max(self.numEng.D[:,ii])==0:
                uSol[:,ii]=u0[:,ii]
                continue
            uT=np.reshape(u0[:,ii],(mG.nX,mG.nY))
            sF=Hx*Hy*uT/dt
            
            Bottom=np.reshape(self.numEng.BC_BC[:,ii],(mG.nX,3),order='F')
            Top=np.reshape(self.numEng.FC_BC[:,ii],(mG.nX,3),order='F')
            
            D_2D=np.reshape(self.numEng.D[:,ii],(mG.nX,mG.nY))
            
            Dh_x=1/hx*2/(1/D_2D[1:,:]+1/D_2D[0:-1,:])
            Dh_y=1/hy*2/(1/D_2D[:,1:]+1/D_2D[:,0:-1])
            
            G_2D=np.reshape(self.numEng.G[:,ii]/self.numEng.Vt,(mG.nX,mG.nY))
            Ns_2D=np.reshape(self.numEng.Ns[:,ii],(mG.nX,mG.nY))
            
            QFL_2D=G_2D-np.log(Ns_2D)+self.numEng.qVec[ii]*fi
            
            dPhi_x=QFL_2D[1:,:]-QFL_2D[0:-1,:]
            dPhi_y=QFL_2D[:,1:]-QFL_2D[:,0:-1]
            
            berVal_plus_dPhi_x,berVal_minus_dPhi_x=Berfun(dPhi_x)
            berVal_plus_dPhi_y,berVal_minus_dPhi_y=Berfun(dPhi_y)
            
            sN=-np.reshape(Hx[:,0:-1]*Dh_y*berVal_minus_dPhi_y,(1,-1))
            sS=-np.reshape(Hx[:,1:]*Dh_y*berVal_plus_dPhi_y,(1,-1))
            
            sE=-np.reshape(Hy[0:-1,:]*Dh_x*berVal_minus_dPhi_x,(1,-1))
            sW=-np.reshape(Hy[1:,:]*Dh_x*berVal_plus_dPhi_x,(1,-1))
            
            sC=Hx*Hy/dt
            
            sC[:,0:-1]=sC[:,0:-1]+Hx[:,0:-1]*Dh_y*berVal_plus_dPhi_y
            sC[:,1:]=sC[:,1:]+Hx[:,1:]*Dh_y*berVal_minus_dPhi_y
            sC[0:-1,:]=sC[0:-1,:]+Hy[0:-1,:]*Dh_x*berVal_plus_dPhi_x
            sC[1:,:]=sC[1:,:]+Hy[1:,:]*Dh_x*berVal_minus_dPhi_x
            
            sC[:,0]=sC[:,0]+Hx[:,0]*Bottom[:,0]/Bottom[:,1]
            sC[:,-1]=sC[:,-1]-Hx[:,-1]*Top[:,0]/Top[:,1]
            
            sCent=np.reshape(sC,(1,-1))
            
            sF[:,0]=sF[:,0]+Hx[:,0]*Bottom[:,2]/Bottom[:,1]
            sF[:,-1]=sF[:,-1]-Hx[:,-1]*Top[:,2]/Top[:,1]
            
            sF=np.reshape(sF,(-1,1))
            
            # center(0), South(-1),North(1),West[-(mG.nX-1)],East(mG.nX-1)
            diagLoc = [0,-1,1,-mG.nY,mG.nY]
            diags = [sCent,sS,sN,sW,sE]
#            if not sW.size==0:
            temp_Ap=sps.diags(diags,diagLoc,shape=(mG.nX*mG.nY,mG.nX*mG.nY))
#            else:
#                temp_Ap = sps.diags([sCent,sS,sN],[0,-1,1],shape=(mG.nX*mG.nY,mG.nX*mG.nY))
            
            uSol[:,ii]=spsl.spsolve(temp_Ap,sF)
        
        # Should check for nan, inf's and negative concentrations.
        out=uSol 
        return out
    def updateFields(self):
        numEng=self.numEng
