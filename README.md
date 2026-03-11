# BioAuth System

A complete biometric authentication system featuring a FastAPI Python backend with deep learning models (SpeechBrain for voice, DeepFace for facial recognition) and a sleek React/Vite frontend dashboard.

## Prerequisites

Before starting, ensure you have the following installed on your system:
- Python 3.9+
- Node.js 18+ and npm
- PostgreSQL 15+
- `pgvector` extension installed on your PostgreSQL server

---

## 🚀 Setup Instructions

### 1. Database Setup
1. Create a PostgreSQL database named `bio_auth`
2. Ensure you have the `pgvector` extension installed. You can install it globally on Linux using:
   ```bash
   sudo apt install postgresql-15-pgvector
   ```
3. Connect to your database and enable the extension (the backend setup will also attempt this automatically if your user has permissions):
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
4. If your Postgres credentials differ from `postgres/password123` on `localhost:5432`, update them in `models/database.py`.

### 2. Backend Setup
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
   *The backend will now be running on `http://localhost:8000`.*

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

## 📡 API Documentation

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