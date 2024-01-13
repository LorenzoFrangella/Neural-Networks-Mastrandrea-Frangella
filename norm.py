import torch
import torchaudio

audio1, sr = torchaudio.load("/Users/pigiby/Desktop/Neural-Networks-Mastrandrea-Frangella/download/-_dElQcyJnA.mp3")
audio2, sr = torchaudio.load("/Users/pigiby/Desktop/Neural-Networks-Mastrandrea-Frangella/download/V65IPXejqj4.mp3")
E1 = torch.square(torch.norm(audio1 ,p = 2))
E2 = torch.square(torch.norm(audio2 ,p = 2))
alpha = (E1/E2)**0.5
mix = audio1 + alpha * audio2

print(alpha)
print(torch.min(audio1))
print(torch.max(audio1))
print(torch.min(audio2))
print(torch.max(audio2))
print(torch.min(mix))
print(torch.max(mix))
