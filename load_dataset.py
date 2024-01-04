from  pytube import YouTube
import os
from pydub import AudioSegment
import csv
import random

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

    return 
    


def download_all_dataset():
    with open('balanced_train_segments.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            video_id = lines[0]
            start = lines[1]
            end = lines[2]
            try:
                get_audio_clip(video_id,float(start),float(end))
            except:
                continue




# get a random row from the file "new_balanced.csv"
            
def get_random_pair(file_name):

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        
        random_rows = random.sample(data, 2)
        
        #print(random_rows[0])
        #print(random_rows[1])
        return random_rows




def get_training_element():
    # we get a random pair of audios from the file
    audios = get_random_pair("./new_balanced.csv")
    
    audio1_metadata = audios[0]
    audio2_metadata = audios[1]

    audio1 = get_audio_clip(audio1_metadata[0],audio1_metadata[1],audio1_metadata[2])
    audio2 = get_audio_clip(audio2_metadata[0],audio2_metadata[1],audio2_metadata[2])


    

get_training_element()




