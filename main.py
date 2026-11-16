
import os
import requests

API_URL = (
    "https://router.huggingface.co/"
    "hf-inference/models/facebook/bart-large-cnn"
)


def text_summary(text: str) -> str:

    if not text or not text.strip():
        raise ValueError("Please enter some text to summarize.")

    # Read token securely from environment
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        raise RuntimeError("Hugging Face API token is not configured.")

    headers = {
        "Authorization": f"Bearer {hf_token}"
    }

    payload = {
        "inputs": text.strip(),
        "parameters": {
            "do_sample": False
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=90
        )

        result = response.json()

        if not response.ok:
            error_message = (
                result.get("error", "Unknown Hugging Face API error")
                if isinstance(result, dict)
                else "Unknown Hugging Face API error"
            )

            raise RuntimeError(
                f"Hugging Face API error ({response.status_code}): "
                f"{error_message}"
            )

        if isinstance(result, list) and result:
            return result[0]["summary_text"]

        raise RuntimeError("Unexpected response from Hugging Face API.")

    except requests.Timeout as exc:
        raise RuntimeError(
            "Hugging Face request timed out. Please try again."
        ) from exc

    except requests.RequestException as exc:
        raise RuntimeError(
            "Unable to connect to Hugging Face."
        ) from exc


# Do not call text_summary() at module import time.
# The API endpoint will call it when a user submits text.
