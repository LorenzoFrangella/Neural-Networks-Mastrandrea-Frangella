import librosa
import laion_clap

model = laion_clap.CLAP_Module(enable_fusion=True)
model.load_ckpt()
text_data = ["I love the contrastive learning", "I love the pretrain model"] 
text_embed = model.get_text_embedding(text_data, use_tensor=True)
print(text_embed)
print(text_embed.shape)