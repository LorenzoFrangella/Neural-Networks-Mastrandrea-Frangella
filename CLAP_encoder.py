import laion_clap
import torch
model = laion_clap.CLAP_Module(enable_fusion=False, amodel= 'HTSAT-base')
model.load_ckpt('C:/Users/pgb_2/OneDrive/Desktop/music_speech_audioset_epoch_15_esc_89.98.pt')
def _get_text_embed( batch):
        double_batch = False
        if len(batch) == 1:
            batch = batch * 2
            double_batch = True
            text_data = model.tokenizer(batch)
            embed = model.model.get_text_embedding(text_data)
        if double_batch:
            embed = embed[0].unsqueeze(0)
        
        return embed.detach()

text_data = ['pigeons are cooing in the background']
text_input = _get_text_embed(text_data)
print(text_input)