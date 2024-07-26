# Video to Text Transcription

This project provides a simple and efficient way to extract and transcribe audio from video files using Python. It leverages libraries such as `moviepy`, `pydub`, and `speech_recognition` to process the media and convert spoken words into text.

## Features

- **Extract Audio from Video**: Supports common video formats like MP4, MKV, AVI, and MOV.
- **Audio Normalization**: Enhances audio quality to improve transcription accuracy.
- **Speech Recognition**: Transcribes Hindi audio to text using Google’s speech recognition service.
- **Error Handling**: Robust error management to handle various exceptions during processing.

## Getting Started

### Prerequisites

Ensure you have the following libraries installed:

- `moviepy`
- `pydub`
- `speechrecognition`

You can install these dependencies using pip:

```bash
pip install moviepy pydub speechrecognition
```

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/video-to-text-transcription.git
    cd video-to-text-transcription
    ```

2. Run the script with your media file path:
    ```bash
    python transcribe.py
    ```

## Usage

Place your video file in the desired directory and update the `media_path` variable in `transcribe.py`:

```python
media_path = "path/to/your/video.mp4"
```

Run the script to extract and transcribe the audio:

```bash
python transcribe.py
```

### Example

For a video file located at `C:/Users/Anshuman Ankur/OneDrive/Desktop/dd/video2.mp4`, the output will be:

```
Transcription:
[Transcribed text will be displayed here]
```

## Code Overview

### `remove_extra_spaces`

Removes extra spaces from the given text.

```python
def remove_extra_spaces(text):
    return ' '.join(text.split())
```

### `extract_audio_from_video`

Extracts audio from a video file and saves it as a WAV file.

```python
def extract_audio_from_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = "extracted_audio.wav"
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path
```

### `convert_audio_to_text`

Converts an audio file to text using Google’s speech recognition API.

```python
def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    chunk_size = 30000  # size of each chunk in milliseconds

    try:
        audio = AudioSegment.from_file(audio_path)
        audio = normalize(audio)
        audio = audio.set_frame_rate(16000).set_channels(1)
        chunks = [audio[i:i + chunk_size] for i in range(0, len(audio), chunk_size)]
        
        full_text = ""
        for i, chunk in enumerate(chunks):
            audio_bytes = io.BytesIO()
            chunk.export(audio_bytes, format="wav")
            audio_bytes.seek(0)
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
```

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [moviepy](https://github.com/Zulko/moviepy)
- [pydub](https://github.com/jiaaro/pydub)
- [speech_recognition](https://github.com/Uberi/speech_recognition)

---

This structure provides a clear and concise overview of the project, setup instructions, and code explanation.
