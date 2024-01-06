from  pytube import YouTube
import os
from pydub import AudioSegment
import csv
import random
import math
import torch
import torchaudio

def cut_audio(input_file, output_file, start_time, end_time):
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(32000)
    cut_audio = audio[start_time:end_time]
    cut_audio.export(output_file, format="mp3")


def get_mixture_audio(audio1,audio2):

    waveform_s1, sample_rate_s1 = torchaudio.load(audio1)
    waveform_s2,sample_rate_s2 = torchaudio.load(audio2)

    E1 = torch.square(torch.norm(waveform_s1,p=2))
    E2 = torch.square(torch.norm(waveform_s2,p=2))

    alpha = torch.sqrt(E1/E2)

    x = waveform_s1 + alpha * waveform_s2
    return x

def get_audio_clip(video_id, start, end, download=True):

    if download:

        if f"{video_id}.mp3" not in os.listdir("./download"):

            video_url = f"https://www.youtube.com/watch?v={video_id}"
            selected_video = YouTube(video_url)
            audio = selected_video.streams.filter(only_audio = True).first()
            path_dest = audio.download("./download", filename=f"{video_id}.mp3")
            cut_audio(path_dest, path_dest, start*1000, end*1000)

        path_dest = f"./download/{video_id}.mp3"

    else:

        if f"{video_id}.mp3" not in os.listdir("./download"):
            return ""    
        
        else:
            path_dest = f"./download/{video_id}.mp3"

    return path_dest
    


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
    
    # divide the two audo metadata
    audio1_metadata = audios[0]
    audio2_metadata = audios[1]

    #cast the initial audio time of each track
    start1 = float(audio1_metadata[1])
    start2 = float(audio2_metadata[1])

    #cast the final audio time of each track
    end1 = float(audio1_metadata[2])
    end2 = float(audio2_metadata[2])
    
    #download the two audio clips, cut them in the defined interval and save

    audio1 = get_audio_clip(audio1_metadata[0],start1,end1)
    audio2 = get_audio_clip(audio2_metadata[0],start2,end2)

    path_clip1 = audio1
    path_clip2 = audio2
    #load the downloaded files

    audio1 = AudioSegment.from_file(audio1)
    audio2 = AudioSegment.from_file(audio2)


    duration1 = audio1.duration_seconds
    duration2 = audio2.duration_seconds

    # now we have to sample 5 random seconds from each clip


    start_time1 = random.uniform(0,(duration1-5))
    start_time2 = random.uniform(0,(duration2-5))

    # we cut the two audios in a random sample of 5 second 

    clipped_audio1 = audio1[start_time1*1000:(start_time1+5)*1000]
    clipped_audio2 = audio2[start_time2*1000:(start_time2+5)*1000]

    clipped_audio1.export(path_clip1, format="mp3")
    clipped_audio2.export(path_clip2, format="mp3")

    # we save the two clips and then we combine them

    mixed = get_mixture_audio(path_clip1,path_clip2)

    torchaudio.save("./download/mixed.mp3",mixed,32000)

    out = torch.stft(mixed,n_fft=1024,hop_length=320,return_complex=True)

    #return the text to enter into CLAP
    
    

    query = audio1_metadata[-1]

    print(query)

    query = query.replace("[","")
    query = query.replace("]","")
    query = query.replace(",","")
    query = query.replace("'","")
    
    
    print(query)
    

    magnitude_spectrogram = torch.abs(out)
    phase_spectrogram = torch.angle(out)

    query = [query]

    return [magnitude_spectrogram,phase_spectrogram,query]
    



def sure_training_item():

    while True:
        try:
            element = get_training_element()
        except:
            continue
        break

    return element




