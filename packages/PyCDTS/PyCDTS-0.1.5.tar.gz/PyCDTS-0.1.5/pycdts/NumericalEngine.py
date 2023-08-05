
import numpy as np
from .mesh_class import Mesh_class
from .simple_PS import simple_PS
from .linearized_PS import linearized_PS
from .damping_PS import damping_PS
from .simpleLinearized_PS import simpleLinearized_PS
from .DAE_PS import DAE_PS
from .Newton_PS import Newton_PS

from .simul_RS import simul_RS
from .simul_RS2 import simul_RS2

from .simul_DS import simul_DS
from .simul_DS_ber import simul_DS_ber
from .Newton_DS_ber import Newton_DS_ber
from .DAE_DS_ber import DAE_DS_ber

class NumericalEngine:
    """
    All the computations are done in this class
    """
    def __init__(self):
        """
        Initializes the variables
        """
        self.nX=0
        self.nY=0
        self.M=0
        self.K=0
        self.iter_tol=0
        self.Kf=np.empty([])
        self.Kb=np.empty([])
        self.LHS=np.empty([])
        self.RHS=np.empty([])
        self.D=np.empty([])
        self.G=np.empty([])
        self.Ns=np.empty([])
        self.qVec=np.empty([])
        self.Eps=np.empty([])
        self.FC_BC=np.empty([])
        self.BC_BC=np.empty([])
        self.Dop=np.empty([])
        self.U0=np.empty([])
        self.fi0=np.empty([])
        self.kT=0
        self.vT=0
        self.Species=[]
        self.is0D=0
        self.nDims=0
        self.mGrid=Mesh_class()
#        Used in the internals of numerical engine.
#        Do not use them outside numerical engine except in solvers
        self.time=0
        self.timeEnd=0
        self.U=np.empty([])
        self.fi=np.empty([])
        self.fi_sol=np.empty([])
        self.uInit=np.empty([])
        self.uR_sol=np.array([])
        self.uD_sol=np.array([])
        self.uD_solInit=np.array([])
        self.gummelStart=1
        self.gummelRelTolForPotential=1e-3
        self.gummelRelTolForConc=1e-3
        
        self.nPoints=100
        
        self.maxGummelIter=40
        
        self.enableRS=1
        self.enableDS=1
        self.enablePS=1
        
        self.typeDS=0
        self.typePS=0
        self.typeRS=1
        
        self.PS=0
        self.DS=0
        self.RS=0
        
        
        self.PS_list={0:simple_PS,
                      1:linearized_PS,
                      2:damping_PS,
                      3:simpleLinearized_PS,
                      4:DAE_PS,
                      5:Newton_PS}
        
        self.DS_list={0:simul_DS,
                      1:simul_DS_ber,
                      2:Newton_DS_ber,
                      4:DAE_DS_ber}
        
        self.RS_list={0:simul_RS,
                      1:simul_RS2}
        
        self.debugFlgEnableCorrections=0
        self.debugFlgEnableCorrectionsInsideWhileLoop=0
        
    def Run(self,timeStart,timeEnd,dtStart):
#        print("Inside Run with timeStart={0},timeEnd={1}".format(timeStart,timeEnd))
        tVec=np.array([timeStart])
        tVec.shape=(1,1)
        UVec=np.reshape(self.U0,(self.nX*self.nY*self.M,1))
        fiVec=self.fi0
        
        self.time=timeStart
        self.timeEnd=timeEnd
        
        self.U=self.U0
        self.fi=self.fi0
        self.fi_sol=np.reshape(self.fi0,(self.nX,self.nY))
        self.uInit=self.U0
        self.uR_sol=self.uInit
        
        if dtStart < timeEnd-timeStart:
            dt=dtStart
        else:
            dt=timeEnd-timeStart
        
        nIterTloop=0
        
        dtcounter=0
        tStart=0
        ratio=1
        
        while self.time < self.timeEnd and nIterTloop<2000:
#            print("time={0},nIterTloop={1}".format(self.time,nIterTloop))
            nIterTloop+=1
            uSol_t=self.uInit
            fiSol_t=self.fi_sol
            try:
                U,fi,nIter,Error=self.SolveTimeStep(dt)
            except Exception as error:
                U,fi,nIter,Error=np.array([]),np.array([]),0,0
            if not U.size==0:
                if not tStart:
                    tStart=1
                    tSave=self.time+dt;
                    ratio= (self.timeEnd/tSave)**(1/self.nPoints)
                
                self.time=self.time+dt
                print('time=%2.5e,\t dt=%2.5e\t dtcounter=%d' % (self.time,dt,dtcounter))
                
                if self.time==tSave or self.time==self.timeEnd:
                    UVec=np.hstack((UVec,U))
                    fiVec=np.hstack((fiVec,fi))
                    tVec=np.hstack((tVec,np.array([[self.time]])))
                    tSave=ratio*tSave
                
                if dtcounter < 15:
                    dtcounter+=1
                    if self.time+dt > tSave:
                        dt=tSave-self.time
                else:
                    dt=dt*2
                    
                    if self.time+dt > self.timeEnd:
                        dt=self.timeEnd-self.time
                    elif self.time+dt > tSave:
                        dt=tSave-self.time
                    
                
            else:
                self.uInit=uSol_t
                self.uD_sol=uSol_t
                self.uR_sol=uSol_t
                self.fi_sol=fiSol_t
                dt=dt/2
                dtcounter=1
            
        return tVec,UVec,fiVec
    
    def SolveTimeStep(self,dt):
#        print("Inside SolveTimeStep dt={0}".format(dt))
        U=np.array([])
        fi=np.array([])
        nIter=0
        Error=np.array([])
        
        if self.enableRS:
            out=self.RS.Solve(dt)
        else:
            out=self.uR_sol
        
#        print("Out={0}".format(out))
        
        if out.size==0:
            raise ValueError('Could not solve reactions for dt='+str(dt))
            print("Could not solve reactions for dt={0}".format(dt))
        
        uR_old=self.uR_sol
        self.uR_sol=out
        
        self.uD_sol=self.uR_sol
        
        if not self.is0D:
            convergence=0
            self.uD_solInit=self.uD_sol
            Error_U=np.zeros((1,self.maxGummelIter))
            Error_Fi=np.zeros((1,self.maxGummelIter))
            
            self.gummelStart=1
            
            while convergence==0 and nIter<self.maxGummelIter:
                nIter=nIter+1
                
                if self.enableDS:
                    out=self.DS.Solve(dt)
                else:
                    out=self.uD_sol
                
                if out.size==0:
                    raise ValueError('Could not solve diffusion for dt='+str(dt))
                
                uD_old=self.uD_sol
                self.uD_sol=out
                
                iCheck=np.where(uD_old !=0)
                if iCheck[0].size==0:
                    Error=np.float64('inf')
                else:
                    Error=np.linalg.norm(out[iCheck]/uD_old[iCheck]-1)/np.sqrt(iCheck[0].size)
                
                conv_U=Error<self.gummelRelTolForConc
                Error_U[nIter-1]=Error
                
                if self.enablePS:
                    out=self.PS.Solve(dt)
                else:
                    out=self.fi_sol
                
                if out.size==0:
                    raise ValueError('Could not solve Poisson for dt'+str(dt))
                
                fi_old=self.fi_sol
                self.fi_sol=out
                
                Error_Fi[nIter-1,1]=np.amax(abs(fi_old-out))
                conv_Fi=Error_Fi[nIter-1,1]<self.gummelRelTolForPotential
                
                if nIter>2 and Error_Fi[nIter-1,1]>Error_Fi[nIter-2,1] and Error_Fi[nIter-2,1]>Error_Fi[nIter-3,1]:
                    break
                convergence = conv_U and conv_Fi
                self.gummelStart=0
        else:
            convergence=1
        
        if convergence:
            self.uInit=self.uD_sol
            self.uR_sol=self.uD_sol
            U=np.reshape(self.uD_sol,(self.nX*self.nY*self.M,1))
            fi=np.reshape(self.fi_sol,(self.nX*self.nY,1))
        else:
            if nIter==self.maxGummelIter:
                raise ValueError('Could not Converge Gummel Loop for dt='+str(dt)+', Error_Conc='+str(Error_U[-1])+', Error_Fi='+str(Error_Fi[-1]))
            else:
                raise ValueError('Divergence Detected. Stopped Gummel Loop for dt='+str(dt))
            
#        print(nIter)
        return U,fi,nIter,Error
    
    def initialize(self):
        self.initializeSolvers()
    
    def initializeSolvers(self):
        if not self.is0D:
            self.PS=self.PS_list[self.typePS](self)
            self.DS=self.DS_list[self.typeDS](self)
        self.RS=self.RS_list[self.typeRS](self)
        
    def reInitialize(self):
        self.RS.updateFields()
        if not self.is0D:
            self.PS.updateFields()
            self.DS.updateFields()
        
    
