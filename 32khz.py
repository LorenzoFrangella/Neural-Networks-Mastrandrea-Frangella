import librosa

# Load audio file with 32 kHz sampling rate
file_path = './download/-0DLPzsiXXE.mp3'  # Replace with your file path
audio_data, sampling_rate = librosa.load(file_path, sr=32000)
import soundfile as sf

# Assuming you have processed your audio data and want to save it
processed_audio_data = audio_data  # Replace this with your processed audio data

# Saving the processed audio data with the original sampling rate
sf.write(file_path, processed_audio_data, sampling_rate)