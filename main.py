import os
import warnings

# 1. Suppress TensorFlow Logs (C++ Backend)
# '0' = all logs, '1' = filter info, '2' = filter warnings, '3' = filter errors
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Turns off the oneDNN info message

# 2. Suppress Python Warnings (like the torchaudio one)
warnings.filterwarnings("ignore")


import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the router we just defined in routes.py
# (Ensure your routes file is named 'routes.py')
from routes import router as bio_router 

# 1. Initialize the Application
app = FastAPI(
    title="Bio-Authentication Microservice",
    description="API for Face and Voice Verification using DeepFace and SpeechBrain",
    version="1.0.0"
)

# 2. Configure CORS (Crucial for your Frontend)
# Without this, your React/HTML site cannot communicate with this Python backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" allows ALL sites to access this. Safe for dev, risky for prod.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# 3. Include the Router
# This mounts all the endpoints (/register, /verify) onto the main app
app.include_router(bio_router)

# 4. A Simple Root Endpoint
# Good for quickly checking if the server is alive without hitting the heavy logic
@app.get("/")
def root():
    return {
        "message": "Bio-Auth System is Online", 
        "docs_url": "http://localhost:8000/docs"
    }

# 5. The Execution Block
if __name__ == "__main__":
    print("Starting Bio-Authentication Server...")
    # 'reload=True' means the server restarts automatically when you save code changes.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)