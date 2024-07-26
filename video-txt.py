import os
import io
import speech_recognition as sr
from pydub import AudioSegment
from pydub.effects import normalize
from moviepy.editor import VideoFileClip

def remove_extra_spaces(text):
    """Remove extra spaces from the given text."""
    return ' '.join(text.split())

def extract_audio_from_video(video_path):
    """Extract audio from a video file."""
    video = VideoFileClip(video_path)
    audio_path = "extracted_audio.wav"
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path

def convert_audio_to_text(audio_path):
    """Convert audio file to text using speech recognition."""
    recognizer = sr.Recognizer()
    chunk_size = 30000  # size of each chunk in milliseconds

    try:
        # Load the audio file
        audio = AudioSegment.from_file(audio_path)
        
        # Normalize and reduce noise in the audio
        audio = normalize(audio)
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        # Split the audio into chunks
        chunks = [audio[i:i + chunk_size] for i in range(0, len(audio), chunk_size)]
        
        full_text = ""

        for i, chunk in enumerate(chunks):
            audio_bytes = io.BytesIO()
            chunk.export(audio_bytes, format="wav")
            audio_bytes.seek(0)
            
            # Load the audio into recognizer
            with sr.AudioFile(audio_bytes) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="hi-IN")
                    full_text += text + " "
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    raise RuntimeError(f"Could not request results from Google Speech Recognition service; {e}")

        return remove_extra_spaces(full_text.strip())
    
    except Exception as e:
        raise RuntimeError(f"Error recognizing speech: {e}")

if __name__ == "__main__":
    # Path to the media file
    media_path = "C:/Users/Anshuman Ankur/OneDrive/Desktop/dd/video2.mp4"

    try:
        # Check if the file is a video or audio
        if media_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
            # Extract audio from the video file
            audio_path = extract_audio_from_video(media_path)
        else:
            # Use the media path directly for audio files
            audio_path = media_path
        
        # Convert audio to text
        text = convert_audio_to_text(audio_path)
        print("Transcription:")
        print(text)
    except Exception as e:
        print(f"Error: {e}")
