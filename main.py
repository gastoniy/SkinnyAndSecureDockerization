import os
import logging
import bcrypt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone

APP_ENV = os.getenv("APP_ENV", "development")
LOG_DIR = os.getenv("LOG_DIR", "./logs")

app = FastAPI(title="Skinny & Secure API", version="1.1.0")

os.makedirs(LOG_DIR, exist_ok=True)

class PasswordRequest(BaseModel):
    password: str

class AuditEventRequest(BaseModel):
    event: str

@app.get("/")
def root():
    return {
        "message": "Hello from FastAPI!", 
        "status": "ok",
        "environment": APP_ENV,
        "status": "ok"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/hash")
def hash_password(req: PasswordRequest):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(req.password.encode('utf-8'), salt)
    return {"hashed_password": hashed.decode('utf-8')}

@app.post("/audit-log")
def create_audit_log(req: AuditEventRequest):
    log_file_path = os.path.join(LOG_DIR, "audit.log")
    try:
        with open(log_file_path, "a") as f:
            timestamp = datetime.now(timezone.utc).isoformat()
            f.write(f"[{timestamp}] EVENT: {req.event}\n")
        return {"status": "success", "message": "Log saved."}
    except PermissionError:
        raise HTTPException(
            status_code=500, 
            detail="Permission Denied. Is the app running as root or missing directory permissions?"
        )