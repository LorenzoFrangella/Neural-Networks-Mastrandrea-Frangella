import torch
import torchaudio
import matplotlib.pyplot as plt


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

    waveform_s1, sample_rate_s1 = torchaudio.load(f"./download/{audio1}.mp3")
    waveform_s2,sample_rate_s2 = torchaudio.load(f"./download/{audio2}.mp3")

    E1 = torch.square(torch.norm(waveform_s1,p=2))
    E2 = torch.square(torch.norm(waveform_s2,p=2))

    alpha = torch.sqrt(E1/E2)

    x = waveform_s1 + alpha * waveform_s2
    return x


audio = get_mixture_audio("-0DLPzsiXXE","--aaILOrkII")
input = torch.stft(audio,n_fft=1024,hop_length=512,return_complex=True)
print(input)
