import os
import shutil
import uuid
from typing import List,Tuple
from fastapi import UploadFile

TEMP_PHOTO_DIR = os.path.join(os.getcwd(),"temp","photos")
TEMP_AUDIO_DIR = os.path.join(os.getcwd(),"temp","audio")

def write_temp_files(photos: List[UploadFile], audio: UploadFile) -> Tuple[List[str],str]:
    os.makedirs(TEMP_PHOTO_DIR,exist_ok=True)
    os.makedirs(TEMP_AUDIO_DIR,exist_ok=True)

    photo_paths=[]
    for p in photos:
        unique_filename = f"{uuid.uuid4()}.jpg"
        file_path = os.path.join(TEMP_PHOTO_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            p.file.seek(0)
            shutil.copyfileobj(p.file, buffer)
        
        photo_paths.append(file_path)


    unique_audio_name = f"{uuid.uuid4()}.wav"
    audio_path = os.path.join(TEMP_AUDIO_DIR, unique_audio_name)
    
    with open(audio_path, "wb") as buffer:
        audio.file.seek(0)
        shutil.copyfileobj(audio.file, buffer)

    return photo_paths,audio_path