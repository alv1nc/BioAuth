from deepface import DeepFace
from core.config import settings


obj = DeepFace.represent(
    img_path='white.jpeg',
    model_name="Facenet",          # Faster, lighter model
    detector_backend="opencv",     # Lightweight C++ based detector
    enforce_detection=True
)

print(obj)