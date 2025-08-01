from transformers import AutoTokenizer
import onnxruntime as ort
import numpy as np
import soundfile as sf

# 1. Charger le tokenizer
print("Chargement du tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("elloza/mms-tts-mlg-onnx")

# 2. Texte en malgache
text = "Manaôna daholo ,atao eto ny teny malagasy izay tiana ho tenenina"


# 3. Tokenisation du texte
inputs = tokenizer(text, return_tensors="np")  # numpy pour onnxruntime

input_ids = inputs["input_ids"]
attention_mask = inputs["attention_mask"]

# 4. Chargement du modèle ONNX
print("Chargement du modèle ONNX...")
session = ort.InferenceSession("onnx/model.onnx")

# 5. Inference (⚠️ attention_mask est requis)
print("Génération de l'audio...")
onnx_inputs = {
    session.get_inputs()[0].name: input_ids.astype(np.int64),
    session.get_inputs()[1].name: attention_mask.astype(np.int64),
}
audio = session.run(None, onnx_inputs)[0]

# 6. Sauvegarde du fichier audio
sf.write("output_malagasy.wav", audio.squeeze(), 16000)
print("✅ Audio sauvegardé : output_malagasy.wav")
