import requests

def call_hugging_face_api(file_content):
    hugging_face_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf"
    headers = {"Authorization": "Bearer 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"}

    response = requests.post(
        hugging_face_url,
        headers=headers,
        files={"file": file_content}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        return None