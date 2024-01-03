import torch
import torchaudio
import matplotlib.pyplot as plt

waveform, sample_rate = torchaudio.load("./download/0Bl8dDFsAQU.mp3")
print("Shape of the audio tensor:", waveform)

print("This is the shape of the waveform: {}".format(waveform.size()))

print("This is the output for Sample rate of the waveform: {}".format(sample_rate))

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

plot_waveform(waveform, sample_rate)