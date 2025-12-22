import numpy as np
import torchaudio
import os

from speechbrain import EncoderClassifier
from deepface import DeepFace

from core.database import DatabaseManager



class BioAuthService:
    def __init__(self):
        self.db=DatabaseManager()


        #temp folder here

        self.speaker_model = EncoderClassifier.from_hparams(
        source="./pretrained_model",
        hparams_file='hyperparams.yaml' 
        )


    def _get_average_face_vect(self,photo_paths = list):
        valid_vectors=[]
        for path in photo_paths:
            try:
                obj = DeepFace.represent(
                    img_path=path,
                    model_nam= "VGG-Face",
                    detector_backend="retinaface",
                    enforce_detection = False
                )
                if obj:
                    vector=obj[0]["embedding"]
                    valid_vectors.append(vector)
            except Exception as e:
                print(f"Skipping bad frame {path}: {e}")
        if not valid_vectors:
            raise Exception("No valid faces found in the burst photos")
        avg_vector = np.mean(valid_vectors, axis=0)
        return avg_vector.tolist()
    

    def _get_vectors(self,audio_path,photo_paths = list):

        try:
            signal, fs = torchaudio.load(audio_path)
            voice_embedding = self.speaker_model.encode_batch(signal)
            emb= voice_embedding.squeeze().tolist()
        except Exception as e:
            raise Exception(f"Voice embedding extraction failed: {e}")
        
        try:
            face_vector = self._get_average_face_vect(photo_paths)
        except Exception as e:
            raise Exception(f"Face embedding extraction failed: {e}")
        return face_vector, emb
    

    def _calculate_similarity(self, vector1, vector2):
        v1,v2=np.array(vector1),np.array(vector2)
        return np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    

    def cleanup(self,paths = list):
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
    
    def register_user(self,user_id,audio_path,photo_paths = list,metadata=None):
        try:
            face_vector, voice_vector = self.get_vectors(audio_path,photo_paths)
            success = self.db.add_user(user_id,face_vector,voice_vector,metadata)
            return success
        finally:
            self.cleanup(photo_paths + [audio_path])

    def verify_user(self,user_id,audio_path,photo_paths = list, metadata=None):
        try:
            face_vector, voice_vector = self.get_vectors(audio_path,photo_paths)
            stored_face, stored_voice, _ = self.db.get_user_vectors(user_id)
            if stored_face is None or stored_voice is None:
                raise ValueError("User ID not found or missing biometric data")
            face_similarity = self._calculate_similarity(face_vector, stored_face)
            voice_similarity = self._calculate_similarity(voice_vector, stored_voice)

            authorized = face_similarity > 0.7 and voice_similarity > 0.7

            self.db.log_attempt(user_id,face_similarity,voice_similarity,"Authorized" if authorized else "Denied")

            return {
                "authorized": authorized,
                "face_score": face_similarity,
                "voice_score": voice_similarity,
                "metadata": metadata,
                "message": "Verification completed"
            }
        finally:
            self.cleanup(photo_paths + [audio_path])
    def identify_user(self,audio_path,photo_paths = list):
        try:
            face_vector,voice_vector = self._get_vectors(photo_paths=photo_paths)

            user_id,metadata,face_near,voice_near = self.db.identify_user(face_vector)

            if user_id is not None:
                face_similarity = self._calculate_similarity(face_vector,face_near)
                voice_similarity = self._calculate_similarity(voice_vector,voice_near)

                authorized = face_similarity > 0.7 and voice_similarity > 0.7

                if face_similarity > 0.7 and voice_similarity > 0.7:
                    message = "Identified"
                elif face_similarity > 0.7:
                    message = "Voice does not match"
                elif voice_similarity > 0.7:
                    message = "Face does not match"
                else:
                    message = "Both face and voice does not match"

                self.db.log_attempt(user_id,face_similarity,voice_similarity,"Authorized" if authorized else "Denied")

                return {
                        "identified": authorized,
                        "best_match_userid": user_id,
                        "face_score": face_similarity,
                        "voice_score": voice_similarity,
                        "metadata": metadata,
                        "message": message
                    }
            else:
                raise ValueError("No userid found")
        finally:
            self.cleanup(photo_paths + [audio_path])
        
    def summarize_user(self,user_id):
        try:
            out = self.db.summarize_user(user_id)

            if out is not None:
                return out
            else:
                raise ValueError("No user_id found")
        finally:
            pass
    def user_list(self):
        try:
            out = self.db.get_users_list()

            if out is not []:
                return out
            else:
                raise ValueError("No users Found")
        finally:
            pass
    def delete_user(self,user_id,permanent=False):
        try:
            cnf = self.db.delete_user(user_id,permanent)
            if cnf==0:
                raise ValueError("No user found")
        finally:
            pass
    def get_logs(self,limit):
        try:
            cnf = self.db.log_attempt_list(limit)

            if cnf == []:
                raise ValueError("No log attempts found")
            else:
                return cnf
        finally:
            pass

            
    



    