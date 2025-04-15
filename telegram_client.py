from telethon import TelegramClient, events
from telethon.tl.types import Message
from typing import Callable, Optional
import asyncio
import os
from dotenv import load_dotenv
import threading
from queue import Queue
import time

load_dotenv()

class TelegramBot:
    """Handles Telegram integration."""
    def __init__(self, on_message_callback: Callable[[str], None]):
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone = os.getenv('TELEGRAM_PHONE')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.on_message_callback = on_message_callback
        self.client = None
        self.loop = None
        self.message_queue = Queue()
        self.running = False
        self.thread = None

    async def _start(self):
        """Start the Telegram client."""
        if not all([self.api_id, self.api_hash, self.phone, self.chat_id]):
            raise ValueError("Missing required Telegram credentials in .env file")

        self.client = TelegramClient('voice_assistant_session', self.api_id, self.api_hash)
        await self.client.start(phone=self.phone)
        
        # Set up message handler
        @self.client.on(events.NewMessage(chats=self.chat_id))
        async def handle_message(event: Message):
            if event.message.text:
                self.on_message_callback(event.message.text)

    async def _send_message(self, text: str) -> None:
        """Send a message to the configured chat."""
        if self.client and self.client.is_connected():
            await self.client.send_message(self.chat_id, text)

    def _run(self):
        """Run the Telegram client in a separate event loop."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            self.loop.run_until_complete(self._start())
            self.running = True
            
            while self.running:
                try:
                    # Check for messages to send
                    if not self.message_queue.empty():
                        message = self.message_queue.get_nowait()
                        self.loop.run_until_complete(self._send_message(message))
                    
                    # Process other tasks
                    self.loop.run_until_complete(asyncio.sleep(0.1))
                except Exception as e:
                    print(f"Error in Telegram loop: {e}")
                    time.sleep(1)  # Prevent tight loop on error
        finally:
            if self.client:
                self.loop.run_until_complete(self.client.disconnect())
            self.loop.close()

    def start(self):
        """Start the Telegram client in a separate thread."""
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            # Wait for client to be ready
            time.sleep(2)

    def stop(self):
        """Stop the Telegram client."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        if self.loop and self.loop.is_running():
            self.loop.stop()

    def send_message(self, text: str) -> None:
        """Thread-safe method to send a message."""
        if self.running:
            self.message_queue.put(text) 