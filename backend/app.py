"""
Note Taker AI - Transcription API
Flask backend for recording, transcribing, and summarizing audio notes
"""

import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from services.assemblyai_service import AssemblyAIService
from services.openai_service import OpenAIService

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webm', 'mp3', 'wav', 'm4a', 'ogg'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize services
assemblyai_service = AssemblyAIService()
openai_service = OpenAIService()

# In-memory storage (for demo purposes)
transcriptions = {}
summaries = {}


def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    """
    Upload audio file for transcription
    Accepts: multipart/form-data with 'audio' file
    Returns: { id, status, text? }
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    file = request.files['audio']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({
            'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400

    try:
        # Generate unique ID
        transcription_id = str(uuid.uuid4())
        
        # Save file
        filename = secure_filename(f"{transcription_id}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Start transcription
        result = assemblyai_service.transcribe_audio(filepath)
        
        # Store in memory
        transcriptions[transcription_id] = {
            'id': transcription_id,
            'status': result['status'],
            'text': result.get('text'),
            'error': result.get('error'),
            'filepath': filepath,
            'created_at': datetime.utcnow().isoformat()
        }

        return jsonify({
            'id': transcription_id,
            'status': result['status'],
            'text': result.get('text'),
            'error': result.get('error')
        }), 200

    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/transcription/<transcription_id>', methods=['GET'])
def get_transcription(transcription_id):
    """
    Get transcription status and result
    Returns: { id, status, text? }
    """
    if transcription_id not in transcriptions:
        return jsonify({'error': 'Transcription not found'}), 404

    transcription = transcriptions[transcription_id]
    
    return jsonify({
        'id': transcription['id'],
        'status': transcription['status'],
        'text': transcription.get('text'),
        'error': transcription.get('error')
    }), 200


@app.route('/api/summarize/<transcription_id>', methods=['POST'])
def summarize(transcription_id):
    """
    Generate summary from transcription
    Returns: { summary }
    """
    if transcription_id not in transcriptions:
        return jsonify({'error': 'Transcription not found'}), 404

    transcription = transcriptions[transcription_id]
    
    if transcription['status'] != 'completed':
        return jsonify({'error': 'Transcription not yet completed'}), 400

    if not transcription.get('text'):
        return jsonify({'error': 'No transcription text available'}), 400

    try:
        # Generate summary
        summary = openai_service.summarize_transcription(transcription['text'])
        
        # Store summary
        summaries[transcription_id] = {
            'transcription_id': transcription_id,
            'summary': summary,
            'created_at': datetime.utcnow().isoformat()
        }

        return jsonify({'summary': summary}), 200

    except Exception as e:
        print(f"Summarization error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/notes/<transcription_id>', methods=['GET'])
def get_notes(transcription_id):
    """
    Get complete meeting notes (transcription + summary)
    Returns: { id, transcription, summary, createdAt }
    """
    if transcription_id not in transcriptions:
        return jsonify({'error': 'Transcription not found'}), 404

    transcription = transcriptions[transcription_id]
    summary_data = summaries.get(transcription_id, {})

    return jsonify({
        'id': transcription_id,
        'transcription': transcription.get('text', ''),
        'summary': summary_data.get('summary', ''),
        'createdAt': transcription['created_at']
    }), 200


if __name__ == '__main__':
    # Validate environment variables
    if not os.getenv('ASSEMBLYAI_API_KEY'):
        print("Warning: ASSEMBLYAI_API_KEY not set")
    if not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY not set")
    
    app.run(host='0.0.0.0', port=3100, debug=True)

