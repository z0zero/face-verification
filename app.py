import os
import uuid
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from verify_faces import verify_faces
from crop_face import crop_face  # Import fungsi crop_face

UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'  # Folder untuk menyimpan gambar yang telah diproses
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.secret_key = 'super secret key'

# Pastikan folder untuk upload dan processed ada, jika tidak maka buat
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    verification_result = None
    ktp_filename = None
    face_filename = None
    ktp_face_path = None
    face_face_path = None
    cosine_score = None

    if request.method == 'POST':
        print("Request method adalah POST")  # Debugging statement
        ktp_image = request.files['ktpImage']
        face_image = request.files['faceImage']

        if ktp_image and face_image and allowed_file(ktp_image.filename) and allowed_file(face_image.filename):
            print("File gambar KTP dan wajah valid")  # Debugging statement
            unique_id = uuid.uuid4().hex  # Generate a unique ID
            ktp_filename = secure_filename(f"{unique_id}_{ktp_image.filename}")
            face_filename = secure_filename(f"{unique_id}_{face_image.filename}")
            ktp_path = os.path.join(app.config['UPLOAD_FOLDER'], ktp_filename)
            face_path = os.path.join(app.config['UPLOAD_FOLDER'], face_filename)
            ktp_image.save(ktp_path)
            face_image.save(face_path)

            try:
                print("Mulai pemotongan wajah")  # Debugging
                ktp_faces = crop_face(ktp_path, app.config['PROCESSED_FOLDER'])
                face_faces = crop_face(face_path, app.config['PROCESSED_FOLDER'])

                # Pastikan setidaknya satu wajah terdeteksi di setiap gambar sebelum verifikasi
                if ktp_faces and face_faces:
                    ktp_face_path = ktp_faces[0]
                    face_face_path = face_faces[0]

                    print("Mulai verifikasi wajah")  # Debugging
                    verification_result, cosine_score = verify_faces(ktp_face_path, face_face_path)
                    print(f"Hasil verifikasi: {verification_result}, Skor kosinus: {cosine_score}")  # Debugging statement

                    flash('Verifikasi berhasil: Orang yang sama.' if verification_result else 'Verifikasi gagal: Orang yang berbeda.')
                else:
                    flash('Tidak dapat mendeteksi wajah di salah satu atau kedua gambar.')
                    return redirect(url_for('home'))

            except Exception as e:
                print(f"Terjadi kesalahan: {str(e)}")  # Debugging
                flash(str(e))
                return redirect(url_for('home'))
        else:
            print("Tipe file gambar tidak valid")  # Debugging statement
            flash('Tipe file gambar tidak valid')

    ktp_face_path_rel = None
    face_face_path_rel = None
    if ktp_face_path:
        ktp_face_path_rel = os.path.join('processed', os.path.basename(ktp_face_path)).replace('\\', '/')
    if face_face_path:
        face_face_path_rel = os.path.join('processed', os.path.basename(face_face_path)).replace('\\', '/')

    return render_template('home.html', verification_result=verification_result, ktp_filename=ktp_filename, face_filename=face_filename, ktp_face_path=ktp_face_path_rel, face_face_path=face_face_path_rel, cosine_score=cosine_score)

if __name__ == '__main__':
    app.run(debug=True)