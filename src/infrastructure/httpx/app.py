import httpx

# Cliente centralizado para peticiones salientes
# Permite configurar timeout, headers, etc. en un solo lugar
def get_http_client():
    return httpx.Client(timeout=30.0, follow_redirects=True)
