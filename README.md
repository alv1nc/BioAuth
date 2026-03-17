# BioAuth System

A complete biometric authentication system featuring a FastAPI Python backend with deep learning models (SpeechBrain for voice, DeepFace for facial recognition).

## Prerequisites

Before starting, ensure you have the following installed on your system:
- Python 3.9+
- Node.js 18+ and npm

---

## Setup Instructions

### 1. Database Setup
The backend requires a PostgreSQL database with the `pgvector` extension to store and query biometric embeddings. A pre-configured Docker Compose file is provided to streamline this setup.

1. Ensure you have Docker and Docker Compose installed on your system.
2. Navigate to the `database` directory:
   ```bash
   cd database
   ```
3. Start the `pgvector` PostgreSQL container in the background:
   ```bash
   docker-compose up -d
   ```
   *This spins up a container named `bio_auth_db` running PostgreSQL 16 on `localhost:5432` with credentials `postgres/password123` and a database named `bio_auth`. The vector extension will be created automatically by the program.*

### 2. BioAuth Setup
1. Open a terminal in the root directory.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server (it will automatically build the tables on first boot and download the required ML models):
   ```bash
   python main.py
   ```
   *BioAuth will now be running on `http://localhost:8000`.*

### 3. Frontend Setup
1. Open a new terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install the Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend dashboard will now be running on `http://localhost:5173`.*

---

##  API Documentation

Base URL: `http://localhost:8000/`

The backend provides the following REST API endpoints for managing biometric profiles.

### POST `/register`
Enrolls a new user by generating embeddings from their face and voice.
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `user_id` (string, required): A unique identifier for the user.
  - `metadata` (JSON string, optional): Additional contextual data to store.
  - `photos` (Array of files, required): 1 or more face images (JPG/PNG).
  - `audio` (file, required): A voice clip recording.
- **Returns:** `{ user_id, status, message }`

### POST `/verify`
Verifies a specific user's identity based on an explicit `user_id`.
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `user_id` (string, required): The ID of the user attempting verification.
  - `photos` (Array of files, required): Live face image capture(s).
  - `audio` (file, required): Live voice recording.
- **Returns:** `{ authorized, face_score, voice_score, metadata, message }` (Returns 400 if user does not exist).

### POST `/identify`
Natively matches a live capture against all enrolled users in the database using vector cosine distance without requiring an explicit User ID.
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `photos` (Array of files, required): Live face image capture(s).
  - `audio` (file, required): Live voice recording.
- **Returns:** `{ identified, best_match_userid, face_score, voice_score, metadata, message }`

### GET `/users`
Retrieves a list of all users registered in the system.
- **Returns:** `{ total_users, users: [{ user_id, is_active, metadata, created_at }, ...] }`

### DELETE `/users/{user_id}`
Deletes or deactivates a user.
- **Query Parameters:**
  - `permanent` (boolean, optional, default: false): If true, permanently deletes the row. If false, marks the user as inactive.
- **Returns:** `{ user_id, deleted, mode, message }`

### GET `/logs`
Retrieves a list of recent authentication attempts.
- **Query Parameters:**
  - `limit` (int, optional, default: 100): Number of recent logs to return.
- **Returns:** `{ count, logs: [{ user_id, status, face_score, voice_score, timestamp }, ...] }`

### GET `/health`
Checks the overall system and database health.
- **Returns:** `{ status, service, checks: { database, models } }`

---
# Notes

- Voice verification is genereally not trusted as the detection system heavily depends on the quality of audio from the user end, hence BioAuth explicitly returns the confidence of both..
- The system will likely take a lot of time on the processing of the first image/audio since it has to download the model parameters first, after which the execution will be compeletly offline and will depend on the hardware specification of the hosting device.
- The system uses Cosine Similarity (<=>) to determine matches. The threshold for what constitutes a "pass" or "fail" can be manually adjusted in the backend configuration, allowing you to prioritize either high security (strict threshold) or user convenience (loose threshold).