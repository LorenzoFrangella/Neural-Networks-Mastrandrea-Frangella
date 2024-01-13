from pydub import AudioSegment
import os
list_files = os.listdir("./validation")
for elem in list_files:
  sound = AudioSegment.from_file(f"./validation/{elem}")
  sound = sound.set_channels(1)
  sound.export(f"./validation_mono/{elem}", format="mp3")