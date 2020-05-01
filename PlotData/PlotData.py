import pandas as pd
import numpy as np
import pylab as plt
class PlotData():#Класс для хранения данных (новое название)
    def __init__(self,x,y,color=None,linestyle=None,linewidth=2,label=None):
        #x,y - данные
        #color - цвет
        #label = метка
        #Те же данные, что передаются в plot(x,y,color,lineidth,label)
        self.x=x
        self.y=y
        self.color=color
        self.linewidth = linewidth
        self.label=label
        self.linestyle=linestyle
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    def get_color(self):
        return self.color
    
    def get_linewidth(self):
        return self.linewidth
    
    def get_label(self):
        return self.label
    def get_linestyle(self):
        return self.linestyle

class SubFig():#Класс отвечающий за один график на канвасе аналог axs[i]
    
    def __init__(self,plots_data=[],#plots_data - Список классов для даты[plot_data_1(),plot_data_2()...]
                 x_lim=[],#[min,max] по x
                 y_lim=[],#[min,max] по y
                 x_label="X",#-меткa по x
                 y_label="Y",#меткa по y
                 title="title",#title
                 fontsize=14,
                 linestyle="-"):#ширина 14
        
        self.plot_data=plots_data
        self.x_label=x_label
        self.y_label=y_label
        self.title=title
        self.fontsize=14
        self.x_lim=x_lim
        self.y_lim=y_lim
        self.linestyle=linestyle
        
    def get_title(self):
        return self.title
           
    def get_fontsize(self):
        return self.fontsize
           
    def get_plot_data(self):
        return self.plot_data
           
    def get_y_label(self):
        return  self.y_label
           
    def get_x_label(self):
        return   self.x_label
    
    def get_y_lim(self):
        return  self.y_lim
           
    def get_x_lim(self):
        return   self.x_lim
    def get_linestyle(self):
        return self.linestyle
    
#Тип линии для каждой data
def paint_subplots(nrows=None,ncols=None,figsize=None,layers=[],wspace=0.7,hspace=0.7):
    if(not nrows or not ncols or (nrows==1 and ncols==1)):
        fig,axs = plt.subplots(figsize=figsize,constrained_layout=True)
        axs.plot(layers[0].get_plot_data()[0].get_x(),layers[0].get_plot_data()[0].get_y(),color=layers[0].get_plot_data()[0].get_color(),
                        linewidth=layers[0].get_plot_data()[0].get_linewidth(),label=layers[0].get_plot_data()[0].get_label(),linestyle=layers[0].get_linestyle())
        if(len(layers[0].get_y_lim())>0):
            axs.set_ylim(layers[0].get_y_lim()[0],layers[0].get_y_lim()[1])
        if(len(layers[0].get_x_lim())>0):
            axs.set_xlim(layers[0].get_x_lim()[0],layers[0].get_x_lim()[1])
        axs.set_ylabel(layers[0].get_y_label())
        axs.set_xlabel(layers[0].get_x_label());
        axs.set_title(layers[0].get_title())
        return
        
        
    fig,axs = plt.subplots(nrows,ncols,figsize=figsize,constrained_layout=True)
    for i in range(len(layers)):
        for j in range(len(layers[i].get_plot_data())):
            if(len(layers[i].get_y_lim())>0):
                axs[i].set_ylim(layers[i].get_y_lim()[0],layers[i].get_y_lim()[1])
            if(len(layers[i].get_x_lim())>0):
                axs[i].set_xlim(layers[i].get_x_lim()[0],layers[i].get_x_lim()[1])

            axs[i].set_ylabel(layers[i].get_y_label())
            axs[i].set_xlabel(layers[i].get_x_label());
            axs[i].plot(layers[i].get_plot_data()[j].get_x(),layers[i].get_plot_data()[j].get_y(),color=layers[i].get_plot_data()[j].get_color(),
                        linewidth=layers[i].get_plot_data()[j].get_linewidth(),label=layers[i].get_plot_data()[j].get_label(),
                        linestyle=layers[i].get_plot_data()[j].get_linestyle())

  
        axs[i].set_title(layers[i].get_title())
        plt.subplots_adjust(wspace=wspace,hspace=hspace)