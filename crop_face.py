import dlib
import cv2
import os

def crop_face(image_path, output_folder):
    # Pastikan output_folder ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} cannot be loaded.")

    # Convert the image to grayscale (Dlib works with grayscale images)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initializing the Face Detector
    detector = dlib.get_frontal_face_detector()

    # Detecting Faces
    faces = detector(gray)
    if len(faces) == 0:
        raise ValueError("No faces detected in the image.")

    cropped_faces = []

    for i, face in enumerate(faces):
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())

        # Crop the face from the image
        cropped_face = image[y:y+h, x:x+w]

        # Resize the cropped face to 160x160
        resized_face = cv2.resize(cropped_face, (160, 160))

        # Save the resized face
        base_filename = os.path.basename(image_path)
        filename, ext = os.path.splitext(base_filename)
        processed_image_path = os.path.join(output_folder, f'{filename}_face_{i}{ext}')
        cv2.imwrite(processed_image_path, resized_face)
        cropped_faces.append(processed_image_path)

    return cropped_faces