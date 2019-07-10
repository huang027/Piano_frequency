import librosa
import numpy as np
import pandas as pd
import soundfile as sf
from pydub.audio_segment import AudioSegment
y, sr =sf.read('G:\music\C大调.wav')
y_new=[i.mean() for i in y]
y_new=np.array(y_new)
#y, sr = librosa.load('G:\music\C大调.wav')
time=librosa.get_duration(filename='G:\music\C大调.wav',sr=sr)
onsets_frames = librosa.onset.onset_detect(y=y_new,sr=sr)
onsets_frames=np.array(onsets_frames)
o_env = librosa.onset.onset_strength(y_new, sr=sr)
onsets_frames=(onsets_frames/len(o_env))*(time)
onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)
onsets_frame=np.array(onsets_frames)
#D = np.abs(librosa.stft(y))**2
time_new=np.linspace(0,time,len(o_env))
time=[]
for i in range(len(o_env)):
    if o_env[i]>=0.2:
        time.append(time_new[i])
    else:
        time.append(0)
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
t_start=[]
t_end=[]
for k in df:
    t_start.append(min(k))
    t_end.append(max(k))
def get_second_part_wav(main_wav_path,start_time,end_time,part_wav_path):
    start_time=start_time*1000
    end_time=end_time*1000
    sound = AudioSegment.from_mp3(main_wav_path)
    word = sound[start_time:end_time]
    word.export(part_wav_path, format="wav")
main_wav_path ='G:\music\C大调.wav'


for j in range(len(t_end)):
    start_time=t_start[j]
    end_time=t_end[j]
    part_wav_path = 'G:\music\cut\ ms_part_voice'+str(j)+'.wav'
    get_second_part_wav(main_wav_path,start_time,end_time,part_wav_path)
