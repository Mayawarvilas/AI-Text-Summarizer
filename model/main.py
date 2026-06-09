import requests

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxx",  # replace with your hugging face api token
           "Content-Type": "application/json"}

data = {
    "inputs":None
}

def text_summary(text):
    data['inputs'] = text
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    return result[0]['summary_text']


print(text_summary("The Hugging Face Transformers library provides a wide range of pre-trained models for natural language processing tasks. These models can be used for various applications such as text classification, question answering, and text generation. The library is built on top of PyTorch and TensorFlow, making it easy to integrate into existing workflows. With the growing community and continuous updates, Hugging Face Transformers has become a popular choice for NLP practitioners and researchers."))
