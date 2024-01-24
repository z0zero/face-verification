import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key' # Needed for flash messaging

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ktp_image = request.files['ktpImage']
        face_image = request.files['faceImage']

        if ktp_image and allowed_file(ktp_image.filename):
            filename = secure_filename(ktp_image.filename)
            ktp_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('KTP image successfully uploaded')
        else:
            flash('Invalid file type for KTP image')

        if face_image and allowed_file(face_image.filename):
            filename = secure_filename(face_image.filename)
            face_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Face image successfully uploaded')
        else:
            flash('Invalid file type for Face image')

        return redirect(url_for('home'))

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
