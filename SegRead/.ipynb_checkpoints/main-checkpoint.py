from SegRead import Seg

from time import time
a = Seg.SegReader()
b=  Seg.SegReader()

#Открываем фаил
# a.open("ki.sgy")
b.open("Dzhelo-pop-60m.sgy")


#Получить количество трасс
#trace = a.read_bin_trace_specefic(["SourceX","SourceY"])
start=time()

#Как считывать часть трасс
# d2 = b.get_data(0,4)
# print(d2[0])
# print(b.get_count_traces())

#Считать всё
data,bn_head,trace_head = b.read_all()
#Для записи нужно использовать функцию, что вернёт объект описывающий bin head. То что возвраает read_all это словарь, для удобства
bin_head=b.get_bin_head()

#Ошибка была в SegyTraceHeaders, исправил
#Запись
#Обязательное имя файла,  и для data  нужно указать
#sampleformat, а то считыввать потом не то будет
Seg.write("ki.sgy",Data =data,SampleFormat=3,SegyHeader=bin_head,SegyTraceHeaders=trace_head)
# print(time()-start)
# a.open("ki.sgy")
# ar =a.get_data(0,2)
# for i in ar:
#     print(i)
#
