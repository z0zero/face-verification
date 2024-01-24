from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ktp_image = request.files['ktpImage']
        face_image = request.files['faceImage']
        if ktp_image:
            print(f"KTP Image Filename: {ktp_image.filename}")
            # Save or process the KTP image file
        if face_image:
            print(f"Face Image Filename: {face_image.filename}")
            # Save or process the face image file
        # Redirect or inform the user of successful upload
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
