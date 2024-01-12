# Separate anything you describe
This repository contains an implementation of the official paper of [Separate anything you describe](https://github.com/Audio-AGI/AudioSep)

#### Description
___

The scope of this project is to isolate a specific sound related to a text query (in natural language) from an audio made of a mixture of multiple audio sources. This task is called Language Query Audio Separation (LASS).

#### The Architecture
---

![alt text](./architecture.png)
The above architecture proposed in the original paper of AudioSep is made by a Language Query encoder and a separation model, also called QueryNet and SeparationNet.
For the former we used the text-encoder and audio-encoder of [CLAP](https://github.com/LAION-AI/CLAP) also used in the original version, while for the latter we have built from scratch the whole architecture. 

#### SeparationNet
---

The separationNet takes as input the audio to process and the output of CLAP. At the beginning the audio is preprocessed with a Short time fourier transform in order to extract the magnitude and the phase of the waveform.
At this point the magnitude spectrogram goes through a ResUnet(encoder-decoder architecture).

This network is composed by 7 encoder blocks and 6 decoder blocks.

Every encoder block contains 2 batch normalization layers, 2 CNN layers and 2 Leaky Relu layers and if the number of channels in input is different from the ones in output there is another convolution on the initial input that is summed with the previous result giving raise to a Residual block. 

In every decoder block instead first we have a ConvTranspose2D that allows to upsample the input, then a skip connection is established between the encoder and the decoder that works on the same sampling rate and then we have the same architecture of the encoder, resulting in this kind of block.

In order to correlate the QueryNet and the SeparationNet, to each feature map of the Separation model is applied another layer called Feature Wise Linearly modulated layer, that essentially is a MLP with 2 fully connected layers that takes as input the embedding of CLAP and the size of the feature map. It returns a value for each channel of the feature map that has to be summed with it.

---
### PLOTS
 These are simplified plots of the ResUnet, of the encoder and and of the decoder. 
 
![image](./resunet.png) 
![image](./encoder.jpg)
![image](./decoder.png)


