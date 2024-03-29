import torch
import torchaudio
import matplotlib.pyplot as plt
from pydub import AudioSegment
import random
import numpy as np
from torchlibrosa.stft import STFT, ISTFT, magphase
def plot_waveform(waveform, sample_rate):

    waveform = waveform.numpy()
    num_channels, num_frames = waveform.shape
    time_axis = torch.arange(0, num_frames) / sample_rate
    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].plot(time_axis, waveform[c], linewidth=1)
        axes[c].grid(True)
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c+1}")
    figure.suptitle("waveform")
    plt.show()



def get_mixture_audio(audio1,audio2):

    waveform_s1, sample_rate_s1 = torchaudio.load(f"./tmp/{audio1}.mp3")
    waveform_s2,sample_rate_s2 = torchaudio.load(f"./tmp/{audio2}.mp3")

    E1 = torch.square(torch.norm(waveform_s1,p=2))
    E2 = torch.square(torch.norm(waveform_s2,p=2))

    alpha = torch.sqrt(E1/E2)

    x = waveform_s1 + alpha * waveform_s2
    return x
audio1 = AudioSegment.from_file(f'./download/5331QhBtfh4.mp3')
audio1 = audio1.set_frame_rate(32000)
audio2 = AudioSegment.from_file(f'./download/3204TAJ9USI.mp3')
audio2 = audio2.set_frame_rate(32000)
duration1 = audio1.duration_seconds
duration2 = audio2.duration_seconds

start_time1 = random.uniform(0,(duration1-5))
start_time2 = random.uniform(0,(duration2-5))


#audio = get_mixture_audio("-0DLPzsiXXE","--aaILOrkII")
#input = torch.stft(audio,n_fft=1024,hop_length=512,return_complex=True)

clipped_audio1 = audio1[start_time1*1000:(start_time1+5)*1000]
clipped_audio2 = audio2[start_time2*1000:(start_time2+5)*1000]

clipped_audio1.export('./tmp/audio1.mp3', format="mp3")
clipped_audio2.export('./tmp/audio2.mp3', format="mp3")
audio = get_mixture_audio("audio1","audio2")
torchaudio.save("./tmp/audio.mp3",audio,32000)
audio1,wave = torchaudio.load("./tmp/audio.mp3")
audios = torch.stack((audio1,audio),dim=0)
print(audios.shape)
stft = STFT(n_fft=1024,
            hop_length=320,
            win_length=1024,
            window='hann',
            center=True,
            pad_mode='reflect',
            freeze_parameters=True)
sp_list = []
cos_list = []
sin_list = []

for i in range(audios.shape[1]):

    (real,img) = stft(audios[:,i,:])
    mag = torch.clamp(real ** 2 + img ** 2, 1e-10, np.inf) ** 0.5
    cos = real / mag
    sin = img / mag
    sp_list.append(real)
    cos_list.append(cos)
    sin_list.append(sin)
mag = torch.cat(sp_list, dim=1)
coss = torch.cat(cos_list, dim=1)
sins = torch.cat(sin_list, dim=1)
#real = real.transpose(0,1)
x = mag.transpose(1,3)


