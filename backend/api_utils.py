"""
This module contains utility functions specifically for interacting with external APIs.
Functions in this module are meant to be imported and used in other parts of the application
to abstract away the details of making API requests and handling API responses.
"""
import json
import requests
import time

def api_request_llm(prompt, url, headers):
    """Helper function to make an API request."""
    payload = json.dumps(
        {
            "input": {
                "prompt": prompt,
                "max_new_tokens": 500,
                "temperature":0.7,
                "top_k":50,
                "top_p":0.7,
                "repetition_penalty":1.2,
                "batch_size": 8,
                "stop": ["</s>"]}
        })
    return requests.post(url, headers=headers, data=payload)

def get_llm_api_credentials():
    llm_url = "https://api.runpod.ai/v2/2btspg14jnwza1/runsync"
    headers = {
        "Authorization": "Bearer 05IB5U9J6DD7UG8GXO0X1DU2M68JF5AZODD5JC1J",
        "Content-Type": "application/json"}
    return llm_url, headers

def poll_for_llm_task_completion(task_id, headers):
    while True:
        sql_response = requests.get(f"https://api.runpod.ai/v2/2btspg14jnwza1/status/{task_id}", headers=headers)
        if sql_response.json().get('status') == 'COMPLETED':
            break
        time.sleep(1)
    return sql_response