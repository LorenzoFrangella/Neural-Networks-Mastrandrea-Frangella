from pydub import AudioSegment
import os
os.remove("./download/.DS_Store")
list_files = os.listdir("./download")
for elem in list_files:
  sound = AudioSegment.from_file(f"./download/{elem}")
  sound = sound.set_channels(1)
  sound.export(f"./download_mono/{elem}", format="mp3")