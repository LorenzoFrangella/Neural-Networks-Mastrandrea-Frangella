from  pytube import YouTube
import os
from pydub import AudioSegment
import csv
import random
import math
import torch
import torchaudio
import numpy as np


text_dict = {}
with open('new_balanced.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            label = lines[4][1:-1]
            label = label.replace("[","")
            label = label.replace("]","")
            label = label.replace(",","")
            label = label.replace("'","")
            text_dict[lines[0]]=[label]
def cut_audio(input_file, output_file, start_time, end_time):
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(32000)
    cut_audio = audio[start_time:end_time]
    cut_audio.export(output_file, format="mp3")


def get_mixture_audio(audio1,audio2):

    E1 = torch.square(torch.norm(audio1,p=2))
    E2 = torch.square(torch.norm(audio2,p=2))

    alpha = torch.sqrt(E1/E2)

    x = audio1 + alpha * audio2
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
    


def download_all_dataset(cognome):
    if cognome == 0:
        with open('mastrandrea.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                video_id = lines[0]
                start = lines[1]
                end = lines[2]
                try:
                    get_audio_clip(video_id,float(start),float(end))
                except:
                    continue
    else:
        with open('frangella.csv', mode ='r')as file:
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
    
    
    #print(query)
    

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


def get_input(modality):
    directory_path = './download'
    batch_audio =  get_random_files(directory_path, 20)

    s1 = batch_audio[0:10]
    print(s1)
    s2 = batch_audio[10:20]
    print(s2)
    values = [text_dict[key[:-4]] for key in s1 if key[:-4] in text_dict]
    mixed = []
    for i in range(10):
        audio1 = AudioSegment.from_file(f'./download/{s1[i]}')
        audio1 = audio1.set_frame_rate(32000)
        audio2 = AudioSegment.from_file(f'./download/{s2[i]}')
        audio2 = audio2.set_frame_rate(32000)
        duration1 = audio1.duration_seconds
        duration2 = audio2.duration_seconds

        # now we have to sample 5 random seconds from each clip


        start_time1 = random.uniform(0,(duration1-5))
        start_time2 = random.uniform(0,(duration2-5))

        # we cut the two audios in a random sample of 5 second 

        clipped_audio1 = audio1[start_time1*1000:(start_time1+5)*1000]
        clipped_audio2 = audio2[start_time2*1000:(start_time2+5)*1000]
        path_clip1 = "./tmp/audio1.mp3"
        path_clip2 = "./tmp/audio2.mp3"
        clipped_audio1.export(path_clip1, format="mp3")
        clipped_audio2.export(path_clip2, format="mp3")

    # we save the two clips and then we combine them

        mixed.append(get_mixture_audio(path_clip1,path_clip2))
    if modality == 'text':
        print(mixed,values)
        return(mixed,values)
    else:
        if random.random() > 0.5:
            return mixed,values
        else:
            print(mixed,["./download/"+elem for elem in s1])
            return mixed,["./download/"+elem for elem in s1]
    
    



def get_random_files(directory, count=20):
    files = os.listdir(directory)
    random_files = random.sample(files, count)
    return random_files



#download_all_dataset(0)


def get_batch(batch_size,dataset_path,labels_file,modality):
    batch_size=batch_size*2
    random_samples = get_random_files(dataset_path,batch_size)
    half = int(batch_size/2)
    
    first_subset = random_samples[0:half]
    second_subset = random_samples[half:batch_size]    

    labels_dict = {}

    with open(labels_file, mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            label = lines[4][1:-1]
            label = label.replace("[","")
            label = label.replace("]","")
            label = label.replace(",","")
            label = label.replace("'","")
            labels_dict[lines[0]]=[label]

    batch = []
    labels = []

    for i in range(half):
        audio1,sample_rate1 = torchaudio.load(f"./download/{first_subset[i]}")
        audio2,sample_rate2 = torchaudio.load(f"./download/{second_subset[i]}")

        # computing starting and ending frame for audio1 
        start1 = random.randint(0,160000)
        end1 = start1 + 160000
        # computing starting and ending frame for audio2
        start2 = random.randint(0,160000)
        end2 = start2 + 160000

        audio1 = audio1[:,start1:end1]
        audio2 = audio2[:,start2:end2]

        mixed = get_mixture_audio(audio1,audio2)
        
        batch.append(mixed)
        labels.append(labels_dict[first_subset[i][:-4]])

    batch = torch.stack(batch,dim=0)
    
    if modality=="text":
        return (batch,labels,False)
    
    else:
        if random.uniform(0,1) > 0.5:
            labels = ["./download/"+elem for elem in first_subset]
            return (batch,labels,True)
        
    return (batch,labels,False)



batch,labels,isAudio = get_batch(100,"./download","new_balanced.csv","hybtrune")

print(batch.shape)


