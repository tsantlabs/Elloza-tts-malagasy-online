from transformers import AutoTokenizer
import onnxruntime as ort
import numpy as np
import soundfile as sf

def generate_audio(text):
    tokenizer = AutoTokenizer.from_pretrained("elloza/mms-tts-mlg-onnx")
    inputs = tokenizer(text, return_tensors="np")

    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    session = ort.InferenceSession("onnx/model.onnx")

    onnx_inputs = {
        session.get_inputs()[0].name: input_ids.astype(np.int64),
        session.get_inputs()[1].name: attention_mask.astype(np.int64),
    }

    audio = session.run(None, onnx_inputs)[0]
    sf.write("static/output_malagasy.wav", audio.squeeze(), 16000)
