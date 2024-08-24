from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from services import DefaultService
from utils.log import debug_logger

app = FastAPI()
service = DefaultService

templates = Jinja2Templates(directory="templates")


class RequestData(BaseModel):
    """Data model for the service"""
    file_name: str
    summarize: bool


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    debug_logger.debug("Request made against index page")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/sum", response_class=HTMLResponse)
async def get_answer():
    """Handle form submission"""
    return RedirectResponse(url="/")


@app.post("/sum", response_class=HTMLResponse)
async def get_answer(request: Request, file_name: Annotated[str, Form()], summarize: Annotated[bool, Form()]):
    """Handle form submission"""
    debug_logger.debug("Request made against /sum endpoint")
    answer = await service.execute(file_name, summarize)
    return templates.TemplateResponse("index.html", {"request": request, "answer": answer})


@app.post("/api/sum", response_class=JSONResponse) 
async def get_answer_rest(data: RequestData):
    """Handle REST API requests for both summarization and transcription"""
    try:
        answer = await service.execute(data.file_name, data.summarize)
        debug_logger.debug(f"Result length: {len(answer)}")
        return JSONResponse(status_code=200, content={"answer": answer})
    except Exception as e:
        debug_logger.error(f"Error in api: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
