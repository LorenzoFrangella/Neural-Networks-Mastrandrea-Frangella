def get_input(modality):
    batch_audio = get_batch()
    s1 = random.sample(batch_audio[0:50],20)
    s2 = random.sample(batch_audio[51:],20)
    values = [text_dict[key[:-4]] for key in s1 if key[:-4] in text_dict]
    mixed = []
    for i in range(20):
        audio1,_1 = torchaudio.load(f'./download/{s1[i]}')
        audio2,_2 = torchaudio.load(f'./download/{s2[i]}')
        start1 = random.randint(0,160000)
        start2 = random.randint(0,160000)
        audio1 = audio1[:,start1:start1+160000]
        audio2 = audio2[:,start2:start2+160000]
        mixed_audio = get_mixture_audio(audio1,audio2)
        mixed.append(mixed_audio)
    mix = torch.stack(mixed,dim=0)
    if modality == 'text':
        return(mix,values)
    else:
        if random.random() > 0.5:
            return mix,values
        else:
            return mix,["./download/"+elem for elem in s1]
    
    



def get_random_files(directory, count=100):
    files = os.listdir(directory)
    random_files = random.sample(files, count)
    return random_files

def get_batch():
    directory_path = './download'
    random_files = get_random_files(directory_path, 100)
    return random_files
print(get_input('hybrid'))