from flask import Flask, render_template, request, send_file
from tts_malagasy import generate_audio
from docx import Document
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text')
    if text:
        generate_audio(text)
        return {'success': True}
    return {'success': False, 'error': 'No text received'}

@app.route('/generate-from-file', methods=['POST'])
def generate_from_file():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return {'success': False, 'error': 'Aucun fichier envoyé'}

    try:
        if uploaded_file.filename.endswith('.txt'):
            text = uploaded_file.read().decode('utf-8')
        elif uploaded_file.filename.endswith('.docx'):
            doc = Document(uploaded_file)
            text = '\n'.join([p.text for p in doc.paragraphs])
        else:
            return {'success': False, 'error': 'Format de fichier non supporté'}

        generate_audio(text)  # Appelle ta fonction TTS
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/audio')
def audio():
    return send_file(
        'static/output_malagasy.wav',
        as_attachment=True,
        download_name='output_malagasy.wav'
    )

if __name__ == '__main__':
    app.run(debug=True)
