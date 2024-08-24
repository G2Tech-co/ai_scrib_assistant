# AI Scribe Assistant

This code demonstrates the implementation of an AI Scribe Assistant. The system is designed to take the dialogue between two people or a monologue and transcribe it. This system also has an option to summarize this transcript and extract important information from the text for later use.
In this version of the system, the name of the audio file stored in Google Cloud is obtained by our API. Then, the Google speech-to-text service transcribes the dialogue or the monologue in the mentioned audio file. After getting the transcribed text, GPT API is asked to summarize the transcription and extract specific information from the text with a specific prompt. <br>
This system's API contains two routes:
api/summarize: Gets the stored audio file and gives a summarized transcription and important information of a dialogue or monologue. 
api/transcribe: Gets the stored audio file and gives transcription of a dialogue or monologue. 


please read `README.md` carefully to understand.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
1. Install requirements.

```sh
python -m venv .venv
.\.venv\Scripts\activate
pip install -m requirements.txt
```
3. Run the following code script.
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

## How to Deploy

Change config in .env

```
cd your directory
.\.venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8003
```

## Rest API

```bash 
uvicorn main:app
```

```bash 
curl -i -X POST -H "Content-Type:application/json" \
   -d \ '{
  "file_name": "something" 
}' 'http://localhost:8000/api/summarize'
```
```bash 
curl -i -X POST -H "Content-Type:application/json" \
   -d \ '{
  "file_name": "something" 
}' 'http://localhost:8000/api/transcribe'
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

