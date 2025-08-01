---
base_model: facebook/mms-tts-mlg
library_name: transformers.js
pipeline_tag: text-to-speech
tags:
- text-to-audio
---

https://huggingface.co/facebook/mms-tts-mlg with ONNX weights to be compatible with Transformers.js.

## Usage (Transformers.js)

If you haven't already, you can install the [Transformers.js](https://huggingface.co/docs/transformers.js) JavaScript library from [NPM](https://www.npmjs.com/package/@xenova/transformers) using:
```bash
npm i @xenova/transformers
```

**Example:** Generate Malagasy speech with `elloza/mms-tts-mlg`.
```js
import { pipeline } from '@xenova/transformers';

// Create a text-to-speech pipeline
const synthesizer = await pipeline('text-to-speech', 'elloza/mms-tts-mlg', {
    quantized: false, // Remove this line to use the quantized version (default)
});

// Generate speech
const output = await synthesizer('manao ahoana');
console.log(output);
// {
//   audio: Float32Array(10752) [ ... ],
//   sampling_rate: 16000
// }
```

Optionally, save the audio to a wav file (Node.js):
```js
import wavefile from 'wavefile';
import fs from 'fs';

const wav = new wavefile.WaveFile();
wav.fromScratch(1, output.sampling_rate, '32f', output.audio);
fs.writeFileSync('out.wav', wav.toBuffer());
```

---

Note: Having a separate repo for ONNX weights is intended to be a temporary solution until WebML gains more traction. If you would like to make your models web-ready, we recommend converting to ONNX using [🤗 Optimum](https://huggingface.co/docs/optimum/index) and structuring your repo like this one (with ONNX weights located in a subfolder named `onnx`).