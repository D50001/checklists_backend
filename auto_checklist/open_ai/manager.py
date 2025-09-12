import os
import logging

import openai
from auto_checklist.settings import OPEN_AI_API_KEY, WHISPER_MODEL
from pydub import AudioSegment


class OpenAIManager:

    def __init__(
            self,
            whisper_model: str =WHISPER_MODEL,
            api_key: str =OPEN_AI_API_KEY
    ):
        self.whisper_model = whisper_model
        self.api_key = api_key

    def transcribe(self, file_path: str, prompt: str = "") -> str | None:
        if file_path.endswith('.ogg'):
            file_path = self._convert_ogg_to_mp3(file_path)
        elif file_path.endswith('.m4a'):
            file_path = self._convert_m4a_to_mp3(file_path)

        client = openai.OpenAI(api_key=self.api_key)
        try:
            with open(file_path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    model=self.whisper_model,
                    file=f,
                    prompt=prompt,
                    language="ru",
                    response_format="text"
                )
        except Exception as e:
            logging.warning(e)
            return None
        finally:
            os.remove(file_path)
        return transcript

    def _convert_ogg_to_mp3(self, ogg_path: str) -> str:
        mp3_path = ogg_path.replace('.ogg', '.mp3')

        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(mp3_path, format="mp3")

        os.remove(ogg_path)
        return mp3_path

    def _convert_m4a_to_mp3(self, m4a_path: str) -> str:
        m4a_path = os.path.normpath(m4a_path)
        mp3_path = m4a_path.replace('.m4a', '.mp3')

        audio = AudioSegment.from_file(m4a_path)
        audio.export(mp3_path, format="mp3")

        os.remove(m4a_path)
        return mp3_path