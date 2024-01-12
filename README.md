# Separate anything you describe
This repository contains an implementation of the official paper of [Separate anything you describe](https://github.com/Audio-AGI/AudioSep)

#### Description
___

The scope to this project is to isolate a specific sound using a text query (in natural language) from an audio made of a mixture of multiple audio sources. This task is called Language Query Audio Separation (LASS).

#### The Architecture
---

![alt text](./architecture.png)
The above architecture proposed in the original paper of AudioSep is made by a Language Query encoder and a separation model, also called QueryNet and SeparationNet.
For the former we used the text-encoder and audio-encoder of [CLAP](https://github.com/LAION-AI/CLAP) also used in the original version, while for the latter we have built from scratch the whole architecture. 

#### SeparationNet
---

The separationNet takes in input the audio to process, and the output of CLAP. At the beginning the audio is preprocessed and the Short time fourier transform is applied to extract magnitude and phase of the waveform. 
