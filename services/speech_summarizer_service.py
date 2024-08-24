import asyncio
from abc import ABC, abstractmethod
from utils.log import error_logger, debug_logger
from .speech_to_text import SpeechToText
from .summarizer import TextSummarizer
from .exceptions import StTConnectionError, StTOperationError, OpenAIError


class SpeechSummarizeService(ABC):
    @abstractmethod
    async def execute(self, audio_file_name: str, summarize: bool) -> str:
        """
        Abstract method to execute speech summarization.
        """
        pass


class GGSummarizer(SpeechSummarizeService):
    """
    Class to transcribe and summarize speech.
    """

    def __init__(self, speech_to_text: SpeechToText, summarizer: TextSummarizer):
        """
        prams:
            speech_to_text: Transcribes the recorded voice 
            summarizer: A class that summarizes the generated transcript
        """
        super().__init__()

        self.speech_to_text = speech_to_text
        self.summarizer = summarizer

    async def execute(self, audio_file_name: str, summarize: bool) -> str:
        """
        Execute speech summarization.

        Args:
            audio_file_name (str): The name of the audio file in the Google Cloud bucket.
            summarize (bool): If true the transcribed text will be summarized.

        Returns:
            str: Transcribed text if summarize = False else the summarized text.
        """
        try:
            output = await self.speech_to_text.convert(audio_file_name)
            debug_logger.debug("Speech converted to text successfully in execute")
            if summarize:
                output = await self.summarizer.summarize(output)
                debug_logger.debug("Speech summarized successfully in execute")
            return output

        except (StTConnectionError, StTOperationError, OpenAIError) as e:
            error_logger.error(str(e))
            return str(e)


if __name__ == "__main__":
    from speech_to_text import GoogleSpeechToText
    from summarizer import GPTUtilizer


    async def test():
        obj = GGSummarizer(GoogleSpeechToText(), GPTUtilizer())
        await obj.transcriber_setup()
        text = await obj.execute(audio_file_name='test', summarize=True)
        print(text)


    asyncio.run(test())
