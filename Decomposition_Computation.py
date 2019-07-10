import numpy as np
import wave
import pandas as pd
from pydub.audio_segment import AudioSegment
file_path='G:\music\合并文件-08_41_25_182.wav' #音频文件路径
f=wave.open(file_path,'rb') #读取音频文件
#获取音频文件参数：nchannels：声道数；sampwidth:量化位数（byte）；framerate:采样频率；nframes:采样点数
params=f.getparams()
nchannels,samplewidth,framerate,nframes=params[:4]
str_data=f.readframes(nframes) #读取音频，字符串格式
f.close()
wave_data=np.fromstring(str_data,dtype=np.short) #将字符串转化为int
#将wave_data数组改为1列，行数自动匹配。当声道数为2的时候，将wave_data数组改为2列，行数自动匹配。在修改shape的属性时，需使得数组的总长度不变。
wave_data.shape=-1,1
if nchannels==2:
    wave_data.shape=-1,2
else:
    pass
wave_data=wave_data.T #将数组转置
time=np.arange(0,nframes)*(1.0/framerate) #音频文件采样点的时间
#音频数据进行平滑用于音符切割
wave_data=abs(wave_data[0])
wave_data=pd.DataFrame(wave_data)
wave_data1=wave_data.rolling(window=5000).mean()
wave_data1=wave_data1.fillna(0)
wave_data1=np.array(wave_data1)
#音符切割，切割成单个音符
for i in range(len(wave_data1)):
    if wave_data1[i]<200:
        time[i]=0
lists = [[]]
index = 0
for i in time:
    if i == 0:
        index+=1
        lists.append([])
    else:
        lists[index].append(i)
df=[]
for j in range(len(lists)-1):
    if lists[j]!=[]:
        df.append(lists[j])
vmin=[]
vmax=[]
for k in df:
    vmin.append(min(k))
    vmax.append(max(k))
vmax1=[vmax[i] for i in range(len(vmax)) if (vmax[i]-vmin[i])>0.02] #剔除切割后时长20毫秒以下的音频
vmin1=[vmin[j] for j in range(len(vmin)) if (vmax[j]-vmin[j])>0.02]
#定义切割保存的路径，单个音符切割的起始时间和终止时间
def get_second_part_wav(main_wav_path,start_time,end_time,part_wav_path):
    start_time=start_time*1000
    end_time=end_time*1000
    sound = AudioSegment.from_mp3(main_wav_path)
    word = sound[start_time:end_time]
    word.export(part_wav_path, format="wav")
main_wav_path =file_path
for j in range(len(vmax)):
    start_time=vmin1[j]
    end_time=vmax1[j]
    part_wav_path = 'G:\music\cut\ ms_part_voice'+str(j)+'.wav'
    get_second_part_wav(main_wav_path,start_time,end_time,part_wav_path)
#计算单个音符的钢琴键号
def Computation(file_name,nor_num):
    file_path = file_name #音符的路径
    test = nor_num #该单个音符正确的键号
    f = wave.open(file_path, 'rb') #读取音频文件
    params = f.getparams()
    nchannels, samplewidth, framerate, nframes = params[:4]
    str_data = f.readframes(nframes)
    f.close()
    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, 1
    if nchannels == 2:
        wave_data.shape = -1, 2
    else:
        pass
    wave_data = wave_data.T
    df = framerate / (nframes - 1) # 波形的分辨率
    freq = [df * n for n in range(0, nframes)] #计算出返回值中每个下标对应的真正的频率
    transformed = np.fft.fft(wave_data[0])  #音频数据傅里叶变换
    d = int(len(transformed) / 2) #常规显示采样频率一半的频谱
    # 仅显示频率在4000以下的频谱，钢琴键最高频率为4186.009
    while freq[d] > 4200:
        d -= 10
    freqs = freq[:d]
    transformed = transformed[:d]
    # 我们的最终目标是提取功率信号，因此需要先将信号的傅里叶变换的模即绝对值
    for i, data in enumerate(transformed):
        transformed[i] = abs(data)
    k = transformed
    w = k
    freqst = []
    m = []
    # 求取波形的所有波峰以及对应得频率
    for i in range(len(freqs) - 2):
        if w[i + 1] > w[i] and w[i + 1] > w[i + 2]:
            freqst.append(freqs[i + 1])
            m.append(w[i + 1])
    freqst = pd.DataFrame(freqst)
    m = pd.DataFrame(m)
    # 将波峰以及对应的频率对应起来，形成Dataframe形式，表格型的数据结构
    data = pd.concat([m, freqst], axis=1)
    data.columns = ['n', 'hz']
    data['hz'] = data['hz']
    data = data.sort_index(axis=0, ascending=False, by='n') #按波峰的信号强弱排序
    data = data.reset_index(drop=True) #重置index
    f = data.head(20) #取前20位
    r = np.array(f['hz'])
    list = pd.read_excel('G:\music\list.xlsx')  #钢琴88个键号以及对应的频谱值
    hz = np.array(list['频率'])
    HZ = []
    MI = []
    MA = []
    # 将低频和高频分别计算，低频由于信号较低，但其谐波信号较强，因此取其3倍的谐波作作为该键号的频率进行匹配；高频信号无需处理
    for k in hz:
        if k < 150: #频率低于150定义为低频
            k = k * 2
            HZ.append(k)
            MI.append(k * (1 - 0.015)) #低频信号误差取±1.5%
            MA.append(k * (1 + 0.015))
        else:
            HZ.append(k)
            MI.append(k * (1 - 0.01)) #高频信号误差取±1%
            MA.append(k * (1 + 0.01))
    HZ = pd.DataFrame(HZ)
    MA = pd.DataFrame(MA)
    MI = pd.DataFrame(MI)
    list['频率'] = HZ
    list['min'] = MI
    list['max'] = MA
    # 按上述误差求取88个键号频率的上限与下限的区间
    fd = np.array(list['频率'])
    Min = np.array(list['min'])
    Max = np.array(list['max'])
    A = []
    # 将前面求得的信号最强的20个频率，分别计算是否落在某个键号的频率区间，如果是则保留，如果不是则剔除
    for i in range(len(Max)):
        for j in range(len(f)):
            if r[j] > Min[i] and r[j] < Max[i]:
                A.append(fd[i])
    A = pd.DataFrame(A)
    A.columns = ['频率']
    result = pd.merge(A, list, how='left', on='频率')
    result = result.ix[:, 0:3]
    result = result.drop_duplicates(['键号']) #删除保留下来的重复键号
    PPP = np.array(result['键号'])
    R = []
    # 跟正确的键号相比，如果正确的键号，在保留下来的键号当中，则演奏正确，并输出该键号
    for i in range(len(test)):
        for j in range(len(PPP)):
            if test[i] == PPP[j]:
                R.append(int(test[i]))
    M=[]
    for i in test:
        if i not in R:
            M.append(int(i))
    return R,M
R_data=pd.read_excel('G:\music\正确键号.xlsx',index_col='序号')  #该曲的正确键号表
R_data=np.array(R_data)
T=[]
L=[]
for i in range(len(vmax)):
    file_name= 'G:\music\cut\ ms_part_voice'+str(i)+'.wav' #单个音符保存的路径
    test=R_data[i]
    test1=[]
    for y in test:
        if y==y:
            test1.append(y)
        else:
            test1.append(0)
    test1=list(filter(lambda x: x != 0, test1))
    P,F=Computation(file_name,test1)  #读取切割后的单个音符，并计算键号
    T.append(len(P))
    L.append(len(F))
    print("音符%d" % (i + 1) + "演奏正确(键号：%s)" % (P)+",漏检(键号：%s)"%(F)) #输出正确的键号
m=sum(L)
n=sum(T)/(sum(T)+sum(L)) #单个音符检测的正确率
print("整曲漏检音符：%d个"%(m))
print("准确率："+str('%.2f%%'%(n*100)))



