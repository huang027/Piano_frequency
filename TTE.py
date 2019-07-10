import numpy as np
import wave
import pandas as pd
from pydub.audio_segment import AudioSegment
file_path='G:\music\合并文件-08_41_25_182.wav'
f=wave.open(file_path,'rb')
num=file_path[-5]
params=f.getparams()
nchannels,samplewidth,framerate,nframes=params[:4]
str_data=f.readframes(nframes)
f.close()
wave_data=np.fromstring(str_data,dtype=np.short)
wave_data.shape=-1,1
if nchannels==2:
    wave_data.shape=-1,2
else:
    pass
wave_data=wave_data.T
time=np.arange(0,nframes)*(1.0/framerate)
wave_data=abs(wave_data[0])
wave_data=pd.DataFrame(wave_data)
wave_data1=wave_data.rolling(window=5000).mean()
wave_data1=wave_data1.fillna(0)
wave_data1=np.array(wave_data1)
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
vmax1=[vmax[i] for i in range(len(vmax)) if (vmax[i]-vmin[i])>0.02]
vmin1=[vmin[j] for j in range(len(vmin)) if (vmax[j]-vmin[j])>0.02]
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

