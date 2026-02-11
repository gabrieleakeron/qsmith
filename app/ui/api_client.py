import os

import requests


API_BASE_URL = os.getenv("QSMITH_API_BASE_URL", "http://localhost:9082").rstrip("/")


def api_get(path: str):
    response = requests.get(f"{API_BASE_URL}{path}", timeout=8)
    response.raise_for_status()
    return response.json()


def api_post(path: str, payload: dict):
    response = requests.post(f"{API_BASE_URL}{path}", json=payload, timeout=8)
    response.raise_for_status()
    return response.json()


def api_put(path: str, payload: dict):
    response = requests.put(f"{API_BASE_URL}{path}", json=payload, timeout=8)
    response.raise_for_status()
    return response.json()


def api_delete(path: str):
    response = requests.delete(f"{API_BASE_URL}{path}", timeout=8)
    response.raise_for_status()
    return response.json()
