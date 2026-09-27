from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learninig_module import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Gemini Powered Learning Assistant",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


class LearningRequest(BaseModel):
    task: Literal[
        "qa",
        "explain",
        "quiz",
        "summarize",
        "learn"
    ]

    text: str = Field(
        min_length=1,
        max_length=20000
    )


def process_request(task: str, text: str):
    if task == "qa":
        return answer_question(text)

    if task == "explain":
        return explain_topic(text)

    if task == "quiz":
        return generate_quiz(text)

    if task == "summarize":
        return summarize_text(text)

    if task == "learn":
        return get_learning_recommendations(text)

    raise HTTPException(
        status_code=400,
        detail="Invalid task selected."
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/api/learn")
async def learn(payload: LearningRequest):
    text = payload.text.strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="Please enter some text."
        )

    try:
        result = process_request(
            payload.task,
            text
        )

        return {
            "task": payload.task,
            "result": result
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"AI request failed: {error}"
        ) from error


# Individual API endpoints


@app.post("/qa")
async def qa_endpoint(payload: dict):
    return {
        "result": answer_question(
            get_text(payload)
        )
    }


@app.post("/explain")
async def explain_endpoint(payload: dict):
    return {
        "result": explain_topic(
            get_text(payload)
        )
    }


@app.post("/quiz")
async def quiz_endpoint(payload: dict):
    return {
        "result": generate_quiz(
            get_text(payload)
        )
    }


@app.post("/summarize")
async def summarize_endpoint(payload: dict):
    return {
        "result": summarize_text(
            get_text(payload)
        )
    }


@app.post("/learn/recommendations")
async def recommendations_endpoint(payload: dict):
    return {
        "result": get_learning_recommendations(
            get_text(payload)
        )
    }


def get_text(payload: dict) -> str:
    text = str(
        payload.get("text", "")
    ).strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="The JSON body must contain a non-empty 'text' field."
        )

    if len(text) > 20000:
        raise HTTPException(
            status_code=422,
            detail="Maximum input length is 20,000 characters."
        )

    return text