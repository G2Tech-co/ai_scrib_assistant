import os
from abc import ABC, abstractmethod
from google.oauth2 import service_account
from google.cloud import speech
from dotenv import load_dotenv

from utils.log import debug_logger, info_logger, error_logger
from .exceptions import StTConnectionError, StTOperationError


class SpeechToText(ABC):
    @abstractmethod
    async def convert(self, audio_file: str) -> str:
        """
        Abstract method to convert audio to text.
        """
        pass


class GoogleSpeechToText(SpeechToText):
    """
    Transcribes a specified file in a Google Cloud bucket.
    """

    def __init__(self) -> None:
        super().__init__()
        load_dotenv()

        client_file = 'your_file.json'
        client_file = os.getenv("GOOGLE_SERVICE_ACCOUNT")
        credentials = service_account.Credentials.from_service_account_file(client_file)
        try:
            self.client = speech.SpeechAsyncClient(credentials=credentials)
            info_logger.info("Connected to Google Speech_to_Text API")
            debug_logger.debug("Connected to Google Speech_to_Text API")

        except Exception as e:
            error_logger.error(f"Error while making Google client: {e}")
            raise StTConnectionError(str(e))

        audio_format = os.getenv("AUDIO_FORMAT").lower()
        encoder_map = {
            "wav": speech.RecognitionConfig.AudioEncoding.LINEAR16,
            "mp3": speech.RecognitionConfig.AudioEncoding.MP3,
            "ogg": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        }
        self.encoder = encoder_map.get(audio_format)
        if not self.encoder:
            raise ValueError("Invalid audio format specified")

        self.config = speech.RecognitionConfig(
            encoding=self.encoder,
            sample_rate_hertz=int(os.getenv("SAMPLE_RATE_HERTZ")),
            audio_channel_count=int(os.getenv("AUDIO_CHANNEL_COUNT")),
            language_code=os.getenv("LANGUAGE_CODE"),
            model=os.getenv("STT_MODEL"),
        )

    async def convert(self, file_name: str) -> str:
        """
        Converts audio file to text using Google Cloud Speech-to-Text API.

        Args:
            file_name (str): Name of the file in the Google Cloud bucket to transcribe.

        Returns:
            str: Transcribed text.
        """
        uri = f"gs://{os.getenv('BUCKET_NAME')}/{file_name}"
        audio = speech.RecognitionAudio(uri=uri)

        try:
            operation = await self.client.long_running_recognize(
                config=self.config, audio=audio
            )
            response = await operation.result(timeout=600)

            # debug_logger.debug("Text obtained from Google API successfully.")

            transcripts = [result.alternatives[0].transcript for result in response.results]
            confidences = [result.alternatives[0].confidence for result in response.results]

            trans_cof = sum(confidences) / len(confidences)
            info_logger.info(f"{file_name} transcriber_confidence: {trans_cof}")

            return ''.join(transcripts)

        except Exception as e:
            error_logger.error(f"Error in conversion: {str(e)}")
            raise StTOperationError(str(e))


if __name__ == "__main__":
    import asyncio

    async def main():
        obj = GoogleSpeechToText()
        text = await obj.convert("")
        print(text)

    asyncio.run(main())
