from pathlib import Path
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(api_key)


client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input="Mezi ANO, SPD a Motoristy se rýsuje spor o Českou televizi a rozhlas",
    instructions="Speak in a cheerful and positive tone.",
) as response:
    response.stream_to_file(speech_file_path)