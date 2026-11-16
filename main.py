
import os
import requests

API_URL = (
    "https://router.huggingface.co/"
    "hf-inference/models/facebook/bart-large-cnn"
)

# Summary length settings: slider values 1 to 5
SUMMARY_LENGTHS = {
    1: (8, 40),
    2: (15, 65),
    3: (25, 100),
    4: (35, 125),
    5: (45, 140)
}


def text_summary(text: str, length: int = 3) -> str:

    if not text or not text.strip():
        raise ValueError("Please enter some text.")

    if length not in SUMMARY_LENGTHS:
        raise ValueError("Summary length must be between 1 and 5.")

    # Retrieve token from environment
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        raise RuntimeError("Hugging Face API token is missing.")

    min_length, max_length = SUMMARY_LENGTHS[length]

    headers = {
        "Authorization": f"Bearer {hf_token}"
    }

    payload = {
        "inputs": text.strip(),
        "parameters": {
            "truncation": "longest_first",
            "generate_parameters": {
                "min_length": min_length,
                "max_length": max_length,
                "do_sample": False
            }
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=90
        )

        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Hugging Face returned an invalid response."
            ) from exc

        if not response.ok:
            message = (
                result.get("error", "Unknown inference error")
                if isinstance(result, dict)
                else str(result)
            )

            raise RuntimeError(
                f"Hugging Face error {response.status_code}: {message}"
            )

        if isinstance(result, list) and result:
            return result[0]["summary_text"]

        raise RuntimeError("No summary was returned by the model.")

    except requests.Timeout as exc:
        raise RuntimeError(
            "The model request timed out. Please try again."
        ) from exc

    except requests.RequestException as exc:
        raise RuntimeError(
            "Unable to connect to Hugging Face."
        ) from exc
