"""
Path: src/infrastructure/httpx/app.py
"""

import httpx

DEFAULT_TIMEOUT = 30.0


def get_http_client() -> httpx.Client:
    return httpx.Client(timeout=DEFAULT_TIMEOUT, follow_redirects=True)


def get_async_http_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=DEFAULT_TIMEOUT, follow_redirects=True)
