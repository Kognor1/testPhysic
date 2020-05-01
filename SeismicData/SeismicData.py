import SegRead as s
import pandas as pd
import numpy as np

class SeismicData():
    def __init__(self,path):
        self.ss = s.Seg.SegReader()
        self.ss.open(path)
        
        data,head=self.ss.get_data_and_trace_heads()
        self.data=data.T
        self.head=head
        self.dt = self.ss.get_dt()/1000# Дискретизация (считывать из хэдеров?)!!!!2 или 2000!!!
        self.Tdata =np.arange(0,np.shape(self.data)[0]*self.dt,self.dt)/1000
        
    def get_spchere(self,CDP_X,CDP_Y,radius):
        idx = self.head[(self.head["CDP_X"] ==CDP_X )& (self.head["CDP_Y"] ==CDP_Y)]
        
        i_line=    (idx["ILINE_NO"].values[0])
        x_line = (idx["XLINE_NO"].values[0])
        
        i_line_filter=[i_line + i for i in range(-radius,radius+1)]
        x_line_filter=[x_line + i for i in range(-radius,radius+1)]

        res = self.head.query(" @i_line_filter in ILINE_NO and @x_line_filter in XLINE_NO")    
        return res
    
        
    def get_offset(self,lasData):
        self.offsets=np.zeros(len(self.head['CDP_X']))
        for ii in range(0, len(self.head['CDP_X'])):
            self. offsets[ii]=np.sqrt((lasData.well_X-self.head['CDP_X'][ii])*(lasData.well_X-self.head['CDP_X'][ii])+(lasData.well_Y-self.head['CDP_Y'][ii])*(lasData.well_Y-self.head['CDP_Y'][ii]))
        return self.offsets
    
    def get_Seism_sig(self,T_well,a):
        Seism_sig=np.interp(T_well,self.Tdata,np.squeeze(self.data[:,a[0]]))
        return Seism_sig