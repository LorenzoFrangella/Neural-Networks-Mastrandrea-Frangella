import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt

# Load the MP3 file
def plot_signal(path,video_id):
    mp3_file_path = path+"/"+video_id+".mp3"
    audio = AudioSegment.from_mp3(mp3_file_path)
    # get the audio of the left channel
    channel_left = audio.split_to_mono()[0]
    # Convert audio to NumPy array
    samples = np.array(channel_left.get_array_of_samples())
    # Get the sample rate
    sample_rate = audio.frame_rate
    #get the len of the samples
    n_samples = len(samples)
    #length of the audio
    t_audio = n_samples/sample_rate

    plt.figure(figsize=(15, 5))
    plt.specgram(samples, Fs=sample_rate, vmin=-20, vmax=50)
    plt.title('Left Channel')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.xlim(0, t_audio)
    plt.colorbar()
    #plt.savefig(f"./waveform_plots/{video_id}")
    plt.show()

plot_signal("./download","V65IPXejqj4")