import pandas as pd
import numpy as np
from mido import MidiFile
score= MidiFile('G:\music\波罗涅兹舞曲-17-巴赫初级钢琴曲集.mid') #mid文件读取
M=[]
#获取mid文件track信息
for i,track in enumerate(score.tracks):
    M.append(track)
#获取每个track的数字信息
for m in range(len(M)-1):
    Msg = []
    for msg in M[m+1]:
        Msg.append(msg)
    Msg=Msg[2:-1]
    Msg=pd.DataFrame(Msg)
    Msg.to_csv('G:\music\\tracks\\track'+str(m+1)+'.csv',index=None) #中间数据保存路径
    data=pd.read_csv('G:\music\\tracks\\track'+str(m+1)+'.csv') #读取中间缓存数据
    #track 数据信息数据处理，包括去空、提取数字、分列等
    data.columns=['meg']
    data = data['meg'].str.split(' ', expand=True)
    data_c=data[2].str.split('note=', expand=True)
    dataset=pd.concat([data_c,data],axis=1)
    dataset=dataset.iloc[:,1:3]
    dataset=dataset[dataset[1].notnull()]
    on_off=np.array(dataset[0])
    note=np.array(dataset[1]).astype(int)
    for n in range(len(on_off)):
        if on_off[n]=='note_off':
            note[n]=0
    c = np.array(note).flatten()
    c = list(c)
    #将整段切分单个音符
    lists = [[]]
    index = 0
    for i in c:
        if i == 0:
            index += 1
            lists.append([])
        else:
            lists[index].append(i)
    dfset = []
    for j in range(len(lists) - 1):
        if lists[j] != []:
            dfset.append(lists[j])
    dfset = pd.DataFrame(dfset)
    dfset=dfset-20 #mid数据信息的键号比实际键号高20，因此需要减20
    dfset.to_excel('G:\music\\tracks\\track'+str(m+1)+'.xlsx') #分别保存每个track的键号









