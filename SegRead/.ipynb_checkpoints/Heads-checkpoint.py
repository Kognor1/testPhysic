import numpy as np
class BinHead():

    def __init__(self, list_header_bin,order):
        self.JobId = int.from_bytes(list_header_bin[0:4:], order,signed=True)
        self.LineNumber = int.from_bytes(list_header_bin[4:8:], order,signed=True)
        self.ReelNumber = int.from_bytes(list_header_bin[8:12:], order,signed=True)
        self.Traces = int.from_bytes(list_header_bin[12:14:], order,signed=True)
        self.AuxTraces = int.from_bytes(list_header_bin[14:16:], order,signed=True)
        self.Interval = int.from_bytes(list_header_bin[16:18:], order,signed=True)
        self.IntervalOriginal = int.from_bytes(list_header_bin[18:20:], order,signed=True)
        self.Samples = int.from_bytes(list_header_bin[20:22:], order)
        self.SamplesOriginal = int.from_bytes(list_header_bin[22:24:], order,signed=True)
        self.Format = int.from_bytes(list_header_bin[24:26:], order,signed=True)
        self.EnsembleFold = int.from_bytes(list_header_bin[26:28:], order,signed=True)  # ?
        self.SortingCode = int.from_bytes(list_header_bin[28:30:], order,signed=True)
        self.VerticalSum = int.from_bytes(list_header_bin[30:32:], order,signed=True)
        self.SweepFrequencyStart = int.from_bytes(list_header_bin[32:34:], order,signed=True)
        self.SweepFrequencyEnd = int.from_bytes(list_header_bin[34:36:], order,signed=True)
        self.SweepLength = int.from_bytes(list_header_bin[36:38:], order,signed=True)
        self.Sweep = int.from_bytes(list_header_bin[38:40:], order,signed=True)
        self.SweepChannel = int.from_bytes(list_header_bin[40:42:], order,signed=True)
        self.SweepTaperStart = int.from_bytes(list_header_bin[42:44:], order,signed=True)
        self.SweepTaperEnd = int.from_bytes(list_header_bin[44:46:], order,signed=True)
        self.Taper = int.from_bytes(list_header_bin[46:48:], order,signed=True)
        self.CorrelatedTraces = int.from_bytes(list_header_bin[48:50:], order,signed=True)
        self.BinaryGainRecovery = int.from_bytes(list_header_bin[50:52:], order,signed=True)
        self.AmplitudeRecovery = int.from_bytes(list_header_bin[52:54:], order,signed=True)
        self.MeasurementSystem = int.from_bytes(list_header_bin[54:56:], order,signed=True)
        self.ImpulseSignalPolarity = int.from_bytes(list_header_bin[56:58:], order,signed=True)
        self.VibratoryPolarity = int.from_bytes(list_header_bin[58:60:], order,signed=True)
        self.order =  int.from_bytes(list_header_bin[96:100:], "big",signed=True)
        self.Spare = int.from_bytes(list_header_bin[60:401:], order,signed=True)


class TraceBinHead():
    def __init__(self):
            self.TRACE_SEQUENCE_LINE =[0,4]
            self.TRACE_SEQUENCE_FILE=[4,4]
            self.FieldRecord=[8,4]
            self.TraceNumber=[12,4]
            self.EnergySourcePoint=[16,4]
            self.CDP=[20,4]
            self.CDP_TRACE=[24,4]
            self.TraceIdentificationCode=[26,2]
            self.NSummedTraces=[28,2]
            self.NStackedTraces=[30,2]
            self.DataUse=[32,2]
            self.offset=[36,4]
            self.ReceiverGroupElevation=[40,4]
            self.SourceSurfaceElevation=[44,4]
            self.SourceDepth=[48,4]
            self.ReceiverDatumElevation=[52,4]
            self.SourceDatumElevation =[56,4]
            self.SourceWaterDepth=[60,4]
            self.GroupWaterDepth=[64,4]
            self.ElevationScalar =[68,2]
            self.SourceGroupScalar=[70,2]
            self.SourceX=[72,4]
            self.SourceY=[76,4]
            self.GroupX=[80,4]
            self.GroupY=[84,4]
            self.CoordinateUnits=[88,2]
            self.WeatheringVelocity=[90,2]
            self.SubWeatheringVelocity=[92,2]
            self.SourceUpholeTime=[94,2]
            self.GroupUpholeTime=[96,2]
            self.SourceStaticCorrection=[98,2]
            self.GroupStaticCorrection=[100,2]
            self.TotalStaticApplied=[102,2]
            self.LagTimeA =[104,2]
            self.LagTimeB =[106,2]
            self.DelayRecordingTime=[108,2]
            self.MuteTimeStart=[110,2]
            self.MuteTimeEND=[112,2]
            self.TRACE_SAMPLE_COUNT=[114,2]
            self.TRACE_SAMPLE_INTERVAL=[116,2]
            self.GainType=[118,2]
            self.InstrumentGainConstant=[120,2]
            self.InstrumentInitialGain=[122,2]
            self.Correlated=[124,2]
            self.SweepFrequencyStart=[126,2]
            self.SweepFrequencyEnd=[128,2]
            self.SweepLength=[130,2]
            self.SweepType=[132,2]
            self.SweepTraceTaperLengthStart=[134,2]
            self.SweepTraceTaperLengthEnd =[136,2]
            self.TaperType=[138,2]
            self.AliasFilterFrequency=[140,2]
            self.AliasFilterSlope=[142,2]
            self.NotchFilterFrequency =[144,2]
            self.NotchFilterSlope =[146,2]
            self.LowCutFrequency =[148,2]
            self.HighCutFrequency =[150,2]
            self.LowCutSlope =[152,2]
            self.HighCutSlope =[154,2]
            self.YearDataRecorded =[156,2]
            self.DayOfYear =[158,2]
            self.HourOfDay=[160,2]
            self.MinuteOfHour=[162,2]
            self.SecondOfMinute =[164,2]
            self.TimeBaseCode=[166,2]
            self.TraceWeightingFactor=[168,2]
            self.GeophoneGroupNumberRoll1=[170,2]
            self.GeophoneGroupNumberFirstTraceOrigField=[172,2]
            self.GeophoneGroupNumberLastTraceOrigField=[174,2]
            self.GapSize=[176,2]
            self.OverTravel=[178,2]
            self.spare =[180,60]


    def get_all_trace(self,list_trace_head_bin,order):
        trace={}
        iter=0
        flag=True
        for i,k in self.__dict__.items():
            if(i=="CoordinateUnits" or not flag and iter<46):
                if(flag):
                    arr = np.frombuffer(list_trace_head_bin[88:180],dtype=">i2")
                    flag=False
                trace[i]=arr[iter]
                iter+=1
                continue
            trace[i]=int.from_bytes(list_trace_head_bin[k[0]:k[0]+k[1]],byteorder=order,signed=True)#order,signed=True)#(np.frombuffer(buffer=list_trace_head_bin[k[0]:k[0]+k[1]],dtype=dt)[0])#int.from_bytes(list_trace_head_bin[k[0]:k[0]+k[1]],byteorder=order,signed=True)#order,signed=True)

        trace["spare"] = int.from_bytes(list_trace_head_bin[180:180 + 60], byteorder=order, signed=True)
        return trace
    def get_specific_trace(self,f,order,cur,a:list=None):
        data={}
        fields = self.__dict__
        if(a==None or (len(a)<=0)):
            return
        else:
            for i in a:
                f.seek(cur+fields[i][0],0)
                data[i]=int.from_bytes(f.read(fields[i][1]),order,signed=True)
        return data

four_bytes={"JobId","LineNumber","ReelNumber","order",
            "TRACE_SEQUENCE_LINE","TRACE_SEQUENCE_FILE","FieldRecord","TraceNumber",
            "EnergySourcePoint","CDP","CDP_TRACE","offset",
            "ReceiverGroupElevation","SourceSurfaceElevation","SourceDepth","ReceiverDatumElevation",
            "SourceDatumElevation","SourceWaterDepth","GroupWaterDepth",
            "SourceX","SourceY","GroupX","GroupY"}

def writeBinHead(f,Headers,order):
    bytes=0
    for i,k in Headers.__dict__.items():
        if (i == "order"):
            continue
        if(i=="Spare"):
            f.write(k.to_bytes(340,order))
            bytes+=340
            continue
        if(i in four_bytes):
            f.write(k.to_bytes(4,order))
            bytes+=4
        else:
            f.write(k.to_bytes(2,order))
            bytes+=2
def writeTraceHeadEmpty(f,Headers,order):
    a = bytearray(240)
    print(type(Headers))
    for i,k in Headers.__dict__.items():

        if(i=="spare"):
            a.extend(int(k).to_bytes(60, order, signed=True))
            continue
        if(i in four_bytes):
            a.extend(int(k).to_bytes(4, order, signed=True))
        else:
            a.extend(int(k).to_bytes(2, order, signed=True))

    return  a
def writeTraceHead(f,Headers,order):
    order_ = ">"
    a=bytes()
    if order=="big":
        order_=">"
    else:
        order_="<"
  #  print(Headers.items())
    for i,k in Headers.items():
     #   print(type(k))
        if (i == "CoordinateUnits"):
            break
        if(i=="spare"):
            a+=(int(k).to_bytes(60, order, signed=True))
            continue
        if(i in four_bytes):
           a+=(np.array(k,dtype=order_+"i4").tobytes())
           #       sample.append(np.frombuffer(k,dtype=np.int32))#
        else:
            a += (np.array(k, dtype=order_ + "i2").tobytes())
    #print(Headers.values[26:-2:])

    a += np.array(list(Headers.values()))[25:-1:].astype(order_+"i2").tobytes()
    a += list(Headers.values())[-1].to_bytes(60, order, signed=True)
    return  a

def writeData(f,Data,coef,order):
    res =None
    if ("int" in str(type(Data[0]))):
       return(Data.astype(int).tobytes())
    elif ("float" in str(type(Data[0]))):
        if(order=="big"):
            res= Data.astype(">f").tobytes()
        else:
            res = Data.astype("<f").tobytes()
    return res