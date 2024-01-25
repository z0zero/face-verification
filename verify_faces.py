import numpy as np
from sklearn.metrics import pairwise
from deepface import DeepFace

def cosine_similarity_base_search_algorithm(ktp_embedding, face_embedding, cosine_threshold=0.45):
    """
    cosine similarity base search algorithm
    """
    # step-1: take the embeddings
    ktp_embedding = np.asarray(ktp_embedding)
    face_embedding = np.asarray(face_embedding).reshape(1,-1)
    
    # step-2: Cal. cosine similarity
    cosine_score = pairwise.cosine_similarity(ktp_embedding, face_embedding)
    cosine_score = np.array(cosine_score).flatten()[0]

    # step-3: check the cosine score
    verification_result = cosine_score >= cosine_threshold
        
    return verification_result, cosine_score

def verify_faces(ktp_path, face_path, cosine_threshold=0.5, enforce_detection=False):
    try:
        ktp = DeepFace.represent(img_path=ktp_path, model_name='Facenet512', enforce_detection=enforce_detection)
        face = DeepFace.represent(img_path=face_path, model_name='Facenet512', enforce_detection=enforce_detection)

        ktp_embedding = ktp[0]['embedding']
        face_embedding = face[0]['embedding']

        if ktp_embedding is not None and face_embedding is not None:
            if isinstance(ktp_embedding, (np.ndarray, list)) and isinstance(face_embedding, (np.ndarray, list)):
                ktp_embedding = np.atleast_2d(ktp_embedding)
                face_embedding = np.atleast_2d(face_embedding)
                
                verification_result, cosine_score = cosine_similarity_base_search_algorithm(ktp_embedding, face_embedding, cosine_threshold)
                return verification_result, cosine_score
            else:
                raise TypeError("Embeddings should be list or numpy array.")
        else:
            raise ValueError("Could not get embeddings for the images.")
    except Exception as e:
        raise e