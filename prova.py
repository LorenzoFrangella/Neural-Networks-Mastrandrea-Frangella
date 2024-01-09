from pydub import AudioSegment
import os
list = os.listdir("./download")
print(len(list))
for elem in list:
    try:
        sound = AudioSegment.from_file(f"./download/{elem}","mp3")
        sound = sound.set_channels(1)
        sound.export(f"./download_mono/{elem}", format="mp3")
    except:
        continue