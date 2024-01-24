import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np
from scipy import spatial
from deepface import DeepFace
import cv2  # Import OpenCV

UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'  # Folder for saving processed images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.secret_key = 'super secret key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    verification_result = None
    ktp_filename = None
    face_filename = None
    ktp_face_path = None
    face_face_path = None
    cosine_threshold = 0.45
    cosine_score = None

    if request.method == 'POST':
        ktp_image = request.files['ktpImage']
        face_image = request.files['faceImage']

        if ktp_image and face_image and allowed_file(ktp_image.filename) and allowed_file(face_image.filename):
            ktp_filename = secure_filename(ktp_image.filename)
            face_filename = secure_filename(face_image.filename)
            ktp_path = os.path.join(app.config['UPLOAD_FOLDER'], ktp_filename)
            face_path = os.path.join(app.config['UPLOAD_FOLDER'], face_filename)
            ktp_image.save(ktp_path)
            face_image.save(face_path)

            try:
                ktp_embedding = DeepFace.represent(img_path=ktp_path, model_name='Facenet512')[0]["embedding"]
                face_embedding = DeepFace.represent(img_path=face_path, model_name='Facenet512')[0]["embedding"]

                # print("KTP Embedding:", ktp_embedding)  # Debug: Cetak embedding KTP
                # print("Face Embedding:", face_embedding)  # Debug: Cetak embedding Wajah

                if ktp_embedding is not None and face_embedding is not None:
                    if isinstance(ktp_embedding, (np.ndarray, list)) and isinstance(face_embedding, (np.ndarray, list)):
                        cosine_score = 1 - spatial.distance.cosine(ktp_embedding, face_embedding)
                        verification_result = cosine_score >= cosine_threshold
                    else:
                        raise TypeError("Embeddings should be list or numpy array.")
                else:
                    raise ValueError("Could not get embeddings for the images.")

                # Process KTP image and save
                ktp_faces = DeepFace.extract_faces(img_path=ktp_path, detector_backend='opencv')
                if ktp_faces:
                    ktp_face_img = ktp_faces[0]
                    if isinstance(ktp_face_img, np.ndarray):  # Pastikan ini adalah array NumPy
                        ktp_face_path = os.path.join(app.config['PROCESSED_FOLDER'], 'processed_' + ktp_filename)
                        cv2.imwrite(ktp_face_path, ktp_face_img)  # Save the processed face image

                # Process face image and save
                face_faces = DeepFace.extract_faces(img_path=face_path, detector_backend='opencv')
                if face_faces:
                    face_face_img = face_faces[0]
                    if isinstance(face_face_img, np.ndarray):  # Pastikan ini adalah array NumPy
                        face_face_path = os.path.join(app.config['PROCESSED_FOLDER'], 'processed_' + face_filename)
                        cv2.imwrite(face_face_path, face_face_img)  # Save the processed face image

                flash('Verification successful: Same person.' if verification_result else 'Verification failed: Different person.')
            except Exception as e:
                flash(str(e))
                return redirect(url_for('home'))
        else:
            flash('Invalid file type for images')

    # Make sure to send the relative path from the 'static' folder to the template
    ktp_face_path_rel = os.path.join('processed', 'processed_' + ktp_filename) if ktp_face_path else None
    face_face_path_rel = os.path.join('processed', 'processed_' + face_filename) if face_face_path else None

    return render_template('home.html', verification_result=verification_result, ktp_filename=ktp_filename, face_filename=face_filename, ktp_face_path=ktp_face_path_rel, face_face_path=face_face_path_rel, cosine_score=cosine_score)

if __name__ == '__main__':
    app.run(debug=True)