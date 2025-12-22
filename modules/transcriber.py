import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_file_path):
    """
    Transcribe audio file using OpenAI Whisper API.
    
    Args:
        audio_file_path (str): Path to the audio file.
        
    Returns:
        str: Transcribed text.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
        return transcript
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
