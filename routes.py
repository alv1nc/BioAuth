from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional,List
import json

from core.dependencies import get_service
from core.bio_service import BioAuthService
from models.schemas import (
    RegistrationResponse, 
    VerificationResponse, 
    IdentificationResponse,
    UserListResponse,
    DeleteResponse,
    LogListResponse,
    HealthResponse
)
from core.utils import write_temp_files
from core.config import settings

router = APIRouter()


@router.post("/register",response_model=RegistrationResponse) #tells the api to run this funciton when called at this url
async def register_user(
    user_id: str = Form(...), #
    metadata: str = Form("{}"),
    photos: List[UploadFile] = File(...),
    audio: UploadFile = File(...),
    service: BioAuthService = Depends(get_service)
):
    try:
        photo_path , audio_path=write_temp_files(photos,audio)
        # Convert string metadata to real dict
        meta_dict = json.loads(metadata)
        
        # Call the logic layer
        result = service.register_user(user_id, audio_path,photo_path, meta_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify",response_model=VerificationResponse)
async def verify_user(
    user_id: str = Form(...),
    photos: List[UploadFile] = File(...),
    audio: UploadFile = File(...),
    service: BioAuthService = Depends(get_service)
):
    try:
        photo_paths,audio_path = write_temp_files(photos,audio)

        result = service.verify_user(user_id, audio_path,photo_paths)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/identify",response_model=IdentificationResponse)
async def identify_user(
    photos: List[UploadFile] = File(...),
    audio: UploadFile = File(...),
    service: BioAuthService = Depends(get_service)
):
    try:
        photo, audio = write_temp_files(photos,audio)

        result = service.identify_user(audio,photo)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users",response_model=UserListResponse)
async def list_users(
    service: BioAuthService = Depends(get_service)
):
    try:
        result = service.user_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/{user_id}",response_model=DeleteResponse)
async def delete_user(
    user_id: str,
    permanent: Optional[bool] = False,
    service: BioAuthService = Depends(get_service)
):
    try:
        result = service.delete_user(user_id,permanent)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/logs",response_model=LogListResponse)
async def get_logs(
    limit: int = 100,
    service: BioAuthService = Depends(get_service)
):
    try:
        result = service.get_logs(limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/health",response_model=HealthResponse)
async def health_check(
    service: BioAuthService = Depends(get_service)
):
    try:
        result = service.health_check()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))