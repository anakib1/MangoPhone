from google.cloud import texttospeech
from google.cloud import speech
import tempfile
import os
import sounddevice as sd
import numpy as np
from typing import Optional
import wave
import io
import warnings

class GoogleTTS:
    """Google Cloud Text-to-Speech implementation."""
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-F",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

    def speak(self, text: str) -> None:
        """Convert text to speech and play it."""
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=self.voice,
                audio_config=self.audio_config
            )

            # Convert audio content to numpy array
            audio_data = np.frombuffer(response.audio_content, dtype=np.int16)
            
            # Play audio directly using sounddevice
            sd.play(audio_data, samplerate=24000)
            sd.wait()  # Wait until audio is finished playing

        except Exception as e:
            warnings.warn(f"Error in text-to-speech: {str(e)}")
            print(f"Error in text-to-speech: {str(e)}")

class GoogleSTT:
    """Google Cloud Speech-to-Text implementation."""
    def __init__(self):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )

    def listen(self) -> Optional[str]:
        """Record audio and convert it to text."""
        try:
            # Record audio
            duration = 5  # seconds
            sample_rate = 16000
            print("Recording...")
            audio_data = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype=np.int16
            )
            sd.wait()
            print("Recording finished")

            # Convert to bytes
            audio_bytes = audio_data.tobytes()

            # Create audio object
            audio = speech.RecognitionAudio(content=audio_bytes)

            # Perform the speech recognition
            response = self.client.recognize(config=self.config, audio=audio)

            # Process the response
            if response.results:
                return response.results[0].alternatives[0].transcript
            return None

        except Exception as e:
            warnings.warn(f"Error in speech recognition: {str(e)}")
            print(f"Error in speech recognition: {str(e)}")
            return None 