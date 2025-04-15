# Voice Communication Interface

A Gradio-based application that provides text-to-speech and speech-to-text communication capabilities using Google Cloud services and Telegram integration.

## Features

- Send text messages to be spoken out loud using Google Cloud Text-to-Speech
- Receive spoken messages and convert them to text using Google Cloud Speech-to-Text
- Read messages from Telegram chat and speak them out loud
- Send recorded messages to Telegram chat
- Clean interface design with Gradio
- Modular architecture with interfaces for TTS and STT implementations

## Prerequisites

1. Google Cloud Platform account
2. Google Cloud project with the following APIs enabled:
   - Cloud Text-to-Speech API
   - Cloud Speech-to-Text API
3. Google Cloud credentials file (JSON)
4. FFmpeg installed on your system
5. Telegram account and API credentials

## Setup

1. Install FFmpeg:
   - Windows: Download from https://ffmpeg.org/download.html and add to PATH
   - Linux: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`

2. Get Telegram API credentials:
   - Go to https://my.telegram.org/auth
   - Log in with your phone number
   - Go to "API development tools"
   - Create a new application
   - Note down the `api_id` and `api_hash`

3. Create a `.env` file with the following variables:
```env
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=your_phone_number
TELEGRAM_CHAT_ID=target_chat_id
```

4. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python app.py
```

## Project Structure

- `app.py`: Main application file containing the Gradio interface and core functionality
- `google_services.py`: Google Cloud TTS and STT implementations
- `telegram_client.py`: Telegram integration
- `requirements.txt`: Project dependencies

## Implementation Notes

The application uses:
- Google Cloud services for TTS and STT
- Telegram for message exchange
- Gradio for the user interface

## Configuration

The current implementation uses the following default settings:
- Language: English (en-US)
- TTS Voice: en-US-Neural2-F (Female)
- Audio Format: LINEAR16 (WAV)
- Recording Duration: 5 seconds
- Sample Rate: 16kHz

## Usage

1. Start the application
2. The application will automatically connect to Telegram
3. Messages received in the configured Telegram chat will be spoken out loud
4. Use the interface to:
   - Type and send messages to be spoken
   - Record voice messages to be sent to Telegram

## Troubleshooting

If you encounter the warning about ffprobe/avprobe:
1. Make sure FFmpeg is installed on your system
2. Verify that FFmpeg is in your system's PATH
3. Restart your terminal/command prompt after installation

If Telegram connection fails:
1. Verify your API credentials
2. Check your phone number format (include country code)
3. Make sure you have access to the target chat

## Future Improvements

- Add language selection
- Add voice selection
- Implement message history
- Add audio visualization
- Add configuration options
- Implement error handling and logging
- Add support for streaming recognition
- Add support for multiple Telegram chats 