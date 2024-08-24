import asyncio
from services.speech_to_text import GoogleSpeechToText
from services.summarizer import GPTUtilizer
from services.speech_summarizer_service import GGSummarizer

DefaultService = GGSummarizer(GoogleSpeechToText(), GPTUtilizer())
