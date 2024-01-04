from  pytube import YouTube
import os
from pydub import AudioSegment

def cut_audio(input_file, output_file, start_time, end_time):
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(32000)
    cut_audio = audio[start_time:end_time]
    cut_audio.export(output_file, format="mp3")


def get_audio_clip(video_id, start, end):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    selected_video = YouTube(video_url)
    audio = selected_video.streams.filter(only_audio = True).first()
    path_dest = audio.download("./download", filename=f"{video_id}.mp3")

    cut_audio(path_dest, path_dest, start*1000, end*1000)
    print(video_id+" downloaded...")
    



import csv
with open('new_balanced.csv', mode ='r')as file:
  csvFile = csv.reader(file)
  for lines in csvFile:
     video_id = lines[0]
     start = lines[1]
     end = lines[2]
     text_to_be_embedded = lines[4]
     text_to_be_embedded = text_to_be_embedded[1:-1]
     try:
        get_audio_clip(video_id,float(start),float(end))
     except:
        continue

     