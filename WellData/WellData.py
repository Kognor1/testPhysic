
from LAS import Converter
import pandas as pd
import numpy as np
class WellData():
    def __init__(self,path,data=None,params=None,del_invalid=False,invalid_columns=None,invalid_value=None):
        c= Converter()
        log = c.set_file(path)
        params_l=log.parameter

        if(params!=None):
            self.heads={}
            for key,value in params.items():
                self.__dict__[value] =params_l[key]['value']
                self.heads[value]= self.__dict__[value]
            print(self.heads)
            self.heads=pd.DataFrame(self.heads,index=[0])
        
        if(data!=None):
            self.data={}
            for key,value in data.items():
                self.__dict__[value] =log.data[key]
                self.data[value]=self.__dict__[value]     
            self.data=pd.DataFrame(self.data)
            
            if(del_invalid):
                self.data=self.data.dropna()
    
    def convert_to_df_head(self):
        return self.heads
    def convert_to_df_data(self):
        return self.data
    def convert_to_df(self,including=None,excluding=None):
        if(including):
                newdict={}
                for i in including:
                    newdict[i]=self.__dict__[i]
                return  pd.DataFrame(newdict)
        if(excluding):
                newdict={}
                for key,value in self.__dict__.items() :
                    if(key in excluding):
                        continue
                    else:
                        newdict[key]=value
                return  pd.DataFrame(newdict)
            
            
        return pd.DataFrame(self.__dict__)
    def merge(self,well,left_on,right_on):
        well_res=self.data.merge(well,left_on=left_on, right_on=right_on)
        self.data=well_res
        return self.data
    def set_reflectivity(self,params):
        self.data['Reflectivity']=0.0

        for ii in range(0,len(self.data['Time'])-1):
            self.data['Reflectivity'][ii]=((1/self.data[params[0]][ii])*self.data[params[1]][ii]-(1/self.data[params[0]][ii+1])*self.data[params[1]][ii+1])/((1/self.data[params[0]][ii])*self.data[params[1]][ii]+(1/self.data[params[0]][ii+1])*self.data[params[1]][ii+1])
    def get_Refl_int(self,T_well):
        self.Refl_int=np.interp(T_well,self.data['Time'],self.data['Reflectivity'])
        return self.Refl_int