from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse
from auth import get_auth_url, acquire_token_by_code
import config

app = FastAPI()

@app.get("/auth/login")
def login():
    auth_url = get_auth_url()
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return JSONResponse({"error": "Authorization code not found"}, status_code=400)
    token_response = acquire_token_by_code(code)
    return JSONResponse(token_response)

@app.get("/protected")
def protected_endpoint(token: str = Depends(acquire_token_by_code)):
    return {"message": "Access granted", "user": token.get("id_token_claims")}