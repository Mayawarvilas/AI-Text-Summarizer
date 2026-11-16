
import os
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import main

app = FastAPI(
    title="AI Text Summarizer",
    description="Text summarization API using BART and Hugging Face",
    version="1.0.0"
)

# Configure frontend origin
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")

allowed_origins = [
    origin.strip()
    for origin in frontend_origin.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


class TextRequest(BaseModel):
    text: str = Field(min_length=1)


@app.get("/")
def home():
    return {
        "message": "AI Text Summarizer API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/summarize")
def summarize_text(text_request: TextRequest):

    text = text_request.text.strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="Please enter text to summarize."
        )

    try:
        summary = main.text_summary(text)

        return {
            "summary": summary
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000"))
    )
