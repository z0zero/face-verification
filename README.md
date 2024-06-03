
# Face Verification Application

Aplikasi ini melakukan verifikasi wajah dengan membandingkan wajah dari dua gambar yang diunggah pengguna. Aplikasi ini menggunakan Flask sebagai framework web dan menggunakan `dlib` serta `DeepFace` untuk mendeteksi dan memverifikasi wajah.

## Persyaratan

Pastikan Anda telah menginstal semua dependensi yang tercantum dalam `requirements.txt`. Anda dapat menginstalnya dengan menggunakan pip:

```bash
pip install -r requirements.txt
```

### Daftar Dependensi

- Flask
- Werkzeug
- dlib
- opencv-python
- scikit-learn
- deepface
- numpy

## Struktur Proyek

```
.
├── app.py
├── crop_face.py
├── verify_faces.py
├── requirements.txt
├── static
│   ├── uploads
│   └── processed
├── templates
│   └── home.html
└── README.md
```

## Penjelasan File

- **app.py**: File utama yang mengandung logika aplikasi web. Ini mengatur rute aplikasi dan menangani proses unggah dan verifikasi gambar.
- **crop_face.py**: Modul ini berfungsi untuk mendeteksi dan memotong wajah dari gambar yang diunggah.
- **verify_faces.py**: Modul ini melakukan verifikasi wajah dengan menghitung kesamaan kosinus antara dua embedding wajah yang diberikan oleh `DeepFace`.
- **requirements.txt**: File yang mencantumkan semua dependensi yang diperlukan oleh aplikasi ini.

## Cara Menjalankan Aplikasi

1. Pastikan semua dependensi telah terinstal.
2. Jalankan aplikasi dengan perintah berikut:

```bash
python app.py
```

Aplikasi akan berjalan dalam mode debug pada `http://127.0.0.1:5000/`.

## Cara Menggunakan Aplikasi

1. Buka browser dan akses `http://127.0.0.1:5000/`.
2. Unggah gambar KTP dan gambar wajah yang ingin diverifikasi.
3. Klik tombol 'Submit'.
4. Aplikasi akan menampilkan hasil verifikasi apakah kedua wajah tersebut merupakan orang yang sama atau tidak.

## Penjelasan Fungsi Utama

### app.py

- **home()**: Rute utama aplikasi yang menangani unggahan gambar, pemotongan wajah, dan verifikasi wajah. Hasil verifikasi dan skor kosinus akan ditampilkan kepada pengguna.

### crop_face.py

- **crop_face(image_path, output_folder)**: Fungsi untuk mendeteksi dan memotong wajah dari gambar. Wajah yang dipotong kemudian disimpan di folder yang ditentukan.

### verify_faces.py

- **cosine_similarity_base_search_algorithm(ktp_embedding, face_embedding, cosine_threshold=0.45)**: Fungsi untuk menghitung kesamaan kosinus antara dua embedding wajah.
- **verify_faces(ktp_path, face_path, cosine_threshold=0.5, enforce_detection=False)**: Fungsi untuk mendapatkan embedding dari dua gambar dan memverifikasi apakah kedua wajah tersebut merupakan orang yang sama berdasarkan kesamaan kosinus.

## Catatan Tambahan

- Pastikan `CMake` telah terinstal di sistem Anda untuk membangun `dlib`.
- Folder `static/uploads` dan `static/processed` harus ada atau akan dibuat secara otomatis oleh aplikasi.

