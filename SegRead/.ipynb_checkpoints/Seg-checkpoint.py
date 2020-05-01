#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mmap import mmap
import ibm2ieee
import numpy as np

from pandas import DataFrame

from SegRead import Heads
import os

import pandas
import struct
from time import time
trace_head_names=['TRACE_SEQUENCE_LINE', 'TRACE_SEQUENCE_FILE', 'FieldRecord', 'TraceNumber', 'EnergySourcePoint', 'CDP', 'CDP_TRACE', 'TraceIdentificationCode', 'NSummedTraces', 'NStackedTraces', 'DataUse', 'offset', 'ReceiverGroupElevation', 'SourceSurfaceElevation', 'SourceDepth', 'ReceiverDatumElevation', 'SourceDatumElevation', 'SourceWaterDepth', 'GroupWaterDepth', 'ElevationScalar', 'SourceGroupScalar', 'SourceX', 'SourceY', 'GroupX', 'GroupY', 'CoordinateUnits', 'WeatheringVelocity', 'SubWeatheringVelocity', 'SourceUpholeTime', 'GroupUpholeTime', 'SourceStaticCorrection', 'GroupStaticCorrection', 'TotalStaticApplied', 'LagTimeA', 'LagTimeB', 'DelayRecordingTime', 'MuteTimeStart', 'MuteTimeEND', 'TRACE_SAMPLE_COUNT', 'TRACE_SAMPLE_INTERVAL', 'GainType', 'InstrumentGainConstant', 'InstrumentInitialGain', 'Correlated', 'SweepFrequencyStart', 'SweepFrequencyEnd', 'SweepLength', 'SweepType', 'SweepTraceTaperLengthStart', 'SweepTraceTaperLengthEnd', 'TaperType', 'AliasFilterFrequency', 'AliasFilterSlope', 'NotchFilterFrequency', 'NotchFilterSlope', 'LowCutFrequency', 'HighCutFrequency', 'LowCutSlope', 'HighCutSlope', 'YearDataRecorded', 'DayOfYear', 'HourOfDay', 'MinuteOfHour', 'SecondOfMinute', 'TimeBaseCode', 'TraceWeightingFactor', 'GeophoneGroupNumberRoll1', 'GeophoneGroupNumberFirstTraceOrigField', 'GeophoneGroupNumberLastTraceOrigField', 'GapSize', 'OverTravel', 'spare']


class SegReader():


    def __init__(self):
        self.f =None
        self.path=""
        self.bin_head=None
        self.line_header = None
        self.trace_bin_head=None
        self.count_trace = 0
        self.order = "big"
        self.sample_format=4
        self.type_float = None
    def get_lineHeader(self):
        return self.line_header
    def get_bin_head(self):
        return self.bin_head
    def open(self,path ):
        self.path=path
        self.f = open(self.path, "rb")
        self.f.seek(0, 0)
        self.line_header = self.f.read(3200)
        b_h = self.f.read(400)
        format = struct.unpack(b'>h',b_h[24:26:] )[0]
        # Check if valid.
        if format in [1,2,3,4,5,8]:
            self.order = "big"
        # Else test little endian.
        else:
            format = struct.unpack(b'<h',b_h[24:26:] )[0]
            if format in [1, 2, 3, 4, 5, 8]:
                self.order = "little"
            else:
                msg = 'Unable to determine the endianness of the file. ' + \
                      'Please specify it.'
                raise Exception(msg)
        # if (int.from_bytes(b_h[97:101:], "big") > 255):
        #     self.order = "little"
        # else:
        #     self.order = "big"
        # self.order="little"
        self.bin_head = Heads.BinHead(b_h, self.order)
        size_file = os.path.getsize(self.path)
        coef = self.check_coef()
        self.count_trace = (size_file - 3600) / (self.bin_head.Samples * coef + 240)
        self.count_trace = int(self.count_trace)
    def read_all(self):
        data , trace_head=self.get_data_and_trace_heads()
        self.f.close()
        return data, self.bin_head.__dict__,trace_head
    def get_step_count(self):
        self.f.seek(3600, 0)
        trace_head = Heads.TraceBinHead()
        b = trace_head.get_all_trace(self.f.read(240), self.order)
        step_count = b["TRACE_SAMPLE_COUNT"]
        self.f.seek(3600, 0)
        return step_count
    def __get_step_count(self):

        trace_head = Heads.TraceBinHead()
        b = trace_head.get_all_trace(self.f.read(240), self.order)
        step_count = b["TRACE_SAMPLE_COUNT"]
        return step_count
    def get_data(self,start=0,end=None):
        self.f.seek(3600, 0)
        step_count = self.__get_step_count()
        coef = self.check_coef()
        offset =coef* step_count
        data = []
        if end == None : end =self.count_trace
        new_end=end-start
        self.f.seek(-240, 1)
        if(start!=0):
            self.f.seek((offset+240) * start,1)
            start =0
        if end ==None :
            end = self.count_trace
        if( end>self.count_trace):
            raise Exception
        for i in range(start, new_end):
            step_count=self.__get_step_count()
            datas = (self.f.read(coef*step_count))
            sample=self.__get_sample(coef,datas)
            data.append(sample)
        return (np.array(data))
    def get_data_and_trace_heads(self):
        if( self.f == None):
            raise Exception("File not open. Use open('path')")
        self.f.seek(3600,0)
        coef = self.check_coef()
        self.trace_bin_headers=None
        offset =self.bin_head.Samples*coef
        #print(offset)
        all={}#pandas.DataFrame(index=np.arange(0,len(Heads.TraceBinHead().__dict__.keys())),columns=Heads.TraceBinHead().__dict__.keys())
        data=[]
        trace_head = Heads.TraceBinHead()
        start_tp=time()
        for i in range(0,self.count_trace):
            start=time()
            b=trace_head.get_all_trace(self.f.read(240), self.order)
            step_count = b["TRACE_SAMPLE_COUNT"]
            all[i]=b.values()
            step_count=self.bin_head.Samples
            datas = (self.f.read(coef*step_count))
            sample= self.__get_sample(coef,datas)
            data.append(sample)

        #print(time()-start_tp)
        self.data= np.array(data)
       # strat = time()
        self.trace_bin_headers = pandas.DataFrame.from_dict(data=all,columns=Heads.TraceBinHead().__dict__.keys(),orient='index')
        self.trace_bin_headers["IDX"]=np.arange(len(self.trace_bin_headers))
       # print(time() -strat)
        self.trace_bin_headers= self.delete_rows_cols(self.trace_bin_headers)
        self.trace_bin_headers=self.trace_bin_headers.drop(["spare"],axis=1)
       
        return self.data ,self.trace_bin_headers
    def check_coef(self):
        if (self.bin_head.Format == 3):
            coef = 2
        elif (self.bin_head.Format == 6 or self.bin_head.Format == 8):
            coef = 1
        elif (self.bin_head.Format == 5):
            coef = 4
            self.type_float="IEEE"
        elif (self.bin_head.Format == 1):
            coef = 4
            self.type_float = "IBM"
        else:
            coef = 4
        return coef
    
    def delete_rows_cols(self,df):
        a = df.values
        mask = a!= 0
        m0 = mask.any(0)
        m1 = mask.any(1)
        return pandas.DataFrame(a[np.ix_(m1,m0)], df.index[m1], df.columns[m0])
    
    
    def get_line_header(self):
        try:
              if self.line_header.decode("cp500")[0]=="C":
                  return self.line_header.decode("cp500"),1
              else:
                  return self.line_header.decode("cp1251"),0
        except Exception as e:
              res= self.line_header
    def print_line_header(self):
        Line_header_decode,id=self.get_line_header()
        if(id==0):
            print(Line_header_decode)
            return
        res = "1"
        for num in range(0, len(Line_header_decode)):

            if res[len(res) - 1] == " " and Line_header_decode[num] == " ":
                continue
            if (Line_header_decode[num] == "C" and Line_header_decode[num + 1].isdigit()):
                res += Line_header_decode[num]
                res += " "
                continue
            if (num == 0):
                res += " "
            res += Line_header_decode[num]
        res = res[1::]
        list_C = res.split(" C ")
        list_C.remove("")
        for i in (list_C):
            print("C" + i)
    def read_bin_trace_specefic(self, param):
        self.f.seek(3600, 0)
        all=[]
        trace_head = Heads.TraceBinHead()
        for i in range(0, self.count_trace):
              cur  = self.f.tell()
              all.append(trace_head.get_specific_trace(self.f,self.order,cur,param))
              self.f.seek(cur+240,0)
              step_count = self.bin_head.Samples
              self.f.seek(step_count*self.check_coef(),1)
        return  pandas.DataFrame(all)
    def load_all_file(self,path):
        with open(path ,"r+b") as f:
            self.f = mmap(f.fileno(), 0)
            self.f.seek(0, 0)
            self.line_header = self.f.read(3200)
            b_h = self.f.read(400)
            if (int.from_bytes(b_h[24:26:], "big") > 255):
                self.order = "little"
            else:
                self.order = "big"
            self.bin_head = Heads.BinHead(b_h, self.order)
            print(self.bin_head.__sizeof__())
            size_file = os.path.getsize(path)
            coef = self.check_coef()
            self.count_trace = (size_file - 3600) / (self.bin_head.Samples * coef + 240)
            self.count_trace = int(self.count_trace)
           # self.f.close()
    def __get_sample(self,coef,datas):
        sample=[]
        if (coef == 2):
            sample = np.frombuffer(datas, dtype=np.int16)
        elif (coef == 4):
            if (self.order == "big"):
                if (self.type_float == "IBM"):
                    dt = np.dtype(np.uint32)
                    dt = dt.newbyteorder(">")
                    sample = np.frombuffer(datas, dtype=dt)
                    sample = ibm2ieee.ibm2float32(sample)
                else:
                    dt = np.dtype(np.float32)
                    dt = dt.newbyteorder(">")
                    sample = np.frombuffer(datas, dtype=dt)
            else:

                if (self.type_float == "IBM"):
                    dt = np.dtype(np.uint32)
                    dt = dt.newbyteorder("<")
                    sample = np.frombuffer(datas, dtype=dt)
                    sample = ibm2ieee.ibm2float32(sample)
                else:
                    dt = np.dtype(np.float32)
                    dt = dt.newbyteorder("<")
                    sample = np.frombuffer(datas, dtype=dt)
        elif (coef == 1):
            sample = np.frombuffer(datas, dtype=np.int8)
        return sample
    def get_dt(self):
        return self.bin_head.Interval


def get_names():
        return trace_head_names
def create_head_traces(dict):
        heads = DataFrame(dict, columns=get_names())
        heads = heads.fillna(0)
        return heads
def write(filename, Data,SegyTraceHeaders=pandas.DataFrame(), SegyHeader=None, text_head=None,order="big",dt=1000,SampleFormat=3):
            if(isinstance(SegyTraceHeaders,dict )):
                SegyTraceHeaders=create_head_traces(SegyTraceHeaders)
            elif(isinstance(SegyTraceHeaders,pandas.DataFrame)):
                pass
            else:
                raise Exception("Not definde type")
            file = open(filename,"wb")
            if(SegyHeader==None):
                bin_head= Heads.BinHead(bytearray(400), order)
            else:
                bin_head=SegyHeader
            coef = retCoef(SampleFormat)
            bin_head.Interval=dt
            bin_head.Samples = len(Data[0])
            bin_head.Format= SampleFormat
            if(text_head!=None):
                file.write(text_head)
            else :
                file.write(bytearray(3200))

            if(SegyTraceHeaders.empty):
                segyTraceHeaders = get_null_trace()
            else:
                segyTraceHeaders=SegyTraceHeaders

            segyTraceHeaders.TRACE_SAMPLE_COUNT = len(Data[0])
            Heads.writeBinHead(file, bin_head, order)
            all_c=bytearray()
            start = time()
            df_dict = segyTraceHeaders.to_dict(orient='index')
            for i in range(0,len(Data)):
                if(SegyTraceHeaders.empty):
                   b = Heads.writeTraceHeadEmpty(file, segyTraceHeaders, order)
                else:
                   b = Heads.writeTraceHead(file, df_dict[i], order)
                a= Heads.writeData(file,Data[i],coef,order)
                try:
                    all_c+=b+a
                except Exception as e:
                    print(e)

            file.write(all_c)
            print(time()-start)


def retCoef(SampleFormat):
    if (SampleFormat == 3):
        coef = 2
    elif (SampleFormat == 6 or SampleFormat == 8):
        coef = 1
    elif (SampleFormat == 5):
        coef = 4
        type_float = "IEEE"
    elif (SampleFormat == 1):
        coef = 4
        type_float = "IBM"
    else:
        coef = 4
    return coef


def get_null_trace():
    ar = Heads.TraceBinHead()
    for i,k in ar.__dict__.items():
        ar.__dict__[i]=0
    return ar
