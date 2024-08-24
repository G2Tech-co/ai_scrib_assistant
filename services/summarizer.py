import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from openai import AsyncOpenAI, APIConnectionError, RateLimitError, APIStatusError
from utils.log import debug_logger, info_logger, error_logger
from .exceptions import OpenAIError


class TextSummarizer(ABC):
    @abstractmethod
    async def summarize(self, text: str) -> str:
        """
        Abstract method to summarize text.
        """
        pass


class GPTUtilizer(TextSummarizer):
    """
    Class to summarize text using the GPT model.
    """

    def __init__(self):
        super().__init__()
        load_dotenv()
        self.engine = os.getenv("ENGINE")

        try:
            self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            info_logger.info("Connected to OpenAI successfully.")
            debug_logger.debug("GPTUtilizer initialized")

        except APIConnectionError as e:
            error_logger.error(f"Failed to connect to OpenAI {e}")
            raise OpenAIError(f"Failed to connect to OpenAI {e}")

    async def summarize(self, text: str) -> str:
        """
        Summarize the given text.

        Args:
            text (str): The text to be summarized.

        Returns:
            str: The summarized text.
        """
        prompt = os.getenv("DIALOGUE_PROMPT") + " " + text

        try:
            response = await self.openai_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.engine,
            )
            response_text = response.choices[0].message.content

            return response_text

        except (RateLimitError, APIStatusError) as e:
            error_logger.error(f"OpenAI API error: {e}")
            raise OpenAIError("Failed to summarize text due to an error in the OpenAI API.")


if __name__ == "__main__":
    import asyncio


    async def main():
        obj = GPTUtilizer()
        # await obj.openai_connector()
        text = ("Türkiye toprakları üzerindeki ilk yerleşmeler Yontma Taş Devri nde başlar. Doğu Trakya da Traklar olmak üzere, "
                "Hititler, Frigler, Lidyalılar ve Dor istilası sonucu Yunanistan dan kaçan Akalar tarafından kurulan İyon medeniyeti "
                "gibi çeşitli eski Anadolu medeniyetlerinin ardından, Makedonya kralı Büyük İskender in egemenliğiyle ve "
                "fetihleriyle birlikte Helenistik Dönem başladı. Daha sonra, sırasıyla Roma İmparatorluğu ve Anadolu nun "
                "Hristiyanlaştığı Bizans dönemleri yaşandı.")
        output = await obj.summarize(text)
        print(output)


    asyncio.run(main())
