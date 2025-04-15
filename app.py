import gradio as gr
from typing import Protocol, Optional
from google_services import GoogleTTS, GoogleSTT
from telegram_client import TelegramBot
import threading
from dotenv import load_dotenv

load_dotenv()

class TextToSpeech(Protocol):
    """Interface for text-to-speech functionality."""
    def speak(self, text: str) -> None:
        """Convert text to speech and play it."""
        pass

class SpeechToText(Protocol):
    """Interface for speech-to-text functionality."""
    def listen(self) -> Optional[str]:
        """Convert speech to text and return it."""
        pass

class MessageProcessor:
    """Handles message processing and communication between TTS and STT."""
    def __init__(self, tts: TextToSpeech, stt: SpeechToText, telegram_bot: TelegramBot):
        self.tts = tts
        self.stt = stt
        self.telegram_bot = telegram_bot
        self.message_queue = []
        self.last_sent_message = ""
        self.last_received_message = ""
        self.received_message_box = None

    def get_spoken_message(self) -> Optional[str]:
        """Get the last spoken message."""
        return self.stt.listen()

    def handle_telegram_message(self, message: str) -> None:
        """Handle incoming Telegram messages."""
        self.last_received_message = message
        self.tts.speak(message)

    def send_telegram_message(self, message: str) -> None:
        """Send a message to Telegram."""
        self.telegram_bot.send_message(message)
        self.last_sent_message = message

    def get_last_received_message(self) -> str:
        """Get the last received message."""
        return self.last_received_message

def create_interface(message_processor: MessageProcessor) -> gr.Interface:
    """Create the Gradio interface."""
    def receive_message() -> tuple[str, str]:
        """Receive and process a spoken message."""
        message = message_processor.get_spoken_message()
        if message:
            message_processor.send_telegram_message(message)
        return message_processor.last_sent_message, message_processor.last_received_message

    def load_last_message() -> str:
        """Load the last received message."""
        return message_processor.get_last_received_message()

    with gr.Blocks() as interface:
        gr.Markdown("# Voice Communication Interface")
        gr.Markdown("Record voice messages to send to Telegram")
        
        with gr.Row():
            with gr.Column():
                sent_message = gr.Textbox(label="Last sent message", value=message_processor.last_sent_message)
            
            with gr.Column():
                record_btn = gr.Button("Record Message")
                received_message = gr.Textbox(label="Last received message", value=message_processor.last_received_message)
                load_btn = gr.Button("Load Last Message")
        
        record_btn.click(
            fn=receive_message,
            outputs=[sent_message, received_message]
        )

        load_btn.click(
            fn=load_last_message,
            outputs=received_message
        )

    return interface

if __name__ == "__main__":
    # Initialize services
    tts = GoogleTTS()
    stt = GoogleSTT()
    
    # Initialize Telegram bot
    telegram_bot = TelegramBot(lambda msg: None)  # Callback will be set later
    
    # Initialize the message processor
    processor = MessageProcessor(tts, stt, telegram_bot)
    
    # Set up Telegram message handler
    telegram_bot.on_message_callback = processor.handle_telegram_message
    
    # Start Telegram bot
    telegram_bot.start()
    
    # Create and launch the interface
    interface = create_interface(processor)
    interface.launch() 