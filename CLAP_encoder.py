import laion_clap
import torch
from huggingface_hub import hf_hub_download


model = laion_clap.CLAP_Module(enable_fusion=False, amodel= 'HTSAT-base')
dataset_path = hf_hub_download(repo_id="lukewys/laion_clap", filename="music_speech_audioset_epoch_15_esc_89.98.pt")
model.load_ckpt(dataset_path)


def get_text_embed(batch):
        double_batch = False
        if len(batch) == 1:
            batch = batch * 2
            double_batch = True
            text_data = model.tokenizer(batch)
            embed = model.model.get_text_embedding(text_data)
        if double_batch:
            embed = embed[0].unsqueeze(0)
        
        return embed.detach()

from load_dataset import sure_training_item

training_triple = sure_training_item()



text_data = training_triple[-1]
text_input = get_text_embed(text_data)
print(text_input)