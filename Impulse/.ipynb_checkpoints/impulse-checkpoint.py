import numpy as np
class Impulse():
    def __init__(self,path,start,stop,dt):
        with open(path,"r") as file:
            i=0
            flag=False
            for line in file:
                if(line[0]=='*'):
                    continue
                else:break
            self.info=line
            self.start_time_or_depth=float(file.readline())
            self.sample_interval=float(file.readline())
            self.N = int(file.readline())
            self.data=np.array( [float(i) for i in list(file)])
            self.T=np.arange(self.start_time_or_depth,self.start_time_or_depth+(self.N)*self.sample_interval,self.sample_interval)
            # вектор времен с дискретизацией по скважине и дополнение нулями для норм спектров
            self.T_int2=np.arange(start,stop,dt) 
            self.Sig=np.interp(self.T_int2,self.T,self.data)
    def get_params():
        return self.T_int2,self.Sig
