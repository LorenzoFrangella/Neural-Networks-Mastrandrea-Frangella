from  pytube import YouTube

import os

video_id = "--4gqARaEJE"

video_url = f"https://www.youtube.com/watch?v={video_id}"

selected_video = YouTube(video_url)
audio = selected_video.streams.filter(only_audio = True).first()

destination = "./download"

base , ext = os.path.splitext(destination)
new_file = base + '.mp3'
os.rename(destination,new_file)
print(type(audio))