
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

import main

# Project directory
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="AI Text Summarizer",
    description="Text summarization using BART and Hugging Face",
    version="1.0.0"
)


# ----------------------------
# Frontend routes
# ----------------------------

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/style.css", include_in_schema=False)
def get_css():
    return FileResponse(
        BASE_DIR / "style.css",
        media_type="text/css"
    )


@app.get("/script.js", include_in_schema=False)
def get_js():
    return FileResponse(
        BASE_DIR / "script.js",
        media_type="application/javascript"
    )


# ----------------------------
# Health check
# ----------------------------

@app.get("/health")
def health():
    return {"status": "healthy"}


# ----------------------------
# API request model
# ----------------------------

class TextRequest(BaseModel):
    text: str = Field(min_length=1)
    length: int = Field(default=3, ge=1, le=5)


# ----------------------------
# Summarization API
# ----------------------------

@app.post("/summarize")
def summarize_text(request: TextRequest):

    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="Please enter some text."
        )

    try:
        summary = main.text_summary(
            text,
            request.length
        )

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


# ----------------------------
# Local development
# ----------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000"))
    )
