# install visual studio, then desktop development with c++
# pip install cmake
# pip install dlib==19.18.0
# pip install face-recognition
# pip install opencv-contrib-python
# pip install caer

import os
from time import sleep
import cv2
import numpy as np
import face_recognition

known_faces_dir = "face_identity"    # stored face images folder location
tolerance = 0.5    # accurecy of face recognition (lower is more secure)
model = "hog"    # face maping (hog for cpu, cnn for cuda) 

# checking if there is any user images stored
def checkFolder():
    files_list = len(os.listdir(known_faces_dir))
    if files_list == 0:
        return "empty"
    else:
        return "notempty"
    
def imageIdentification(frame):
    known_faces_encoding = []
    
    # encoding images
    for filename in os.listdir(known_faces_dir):
        image = face_recognition.load_image_file(f"{known_faces_dir}/{filename}")
        faces = face_recognition.face_locations(image, model=model)
        image_encoding = face_recognition.face_encodings(image, faces)[0]
        known_faces_encoding.append(image_encoding)
        
    img = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    
    faces_in_frame = face_recognition.face_locations(img, model=model)
    encoded_face = face_recognition.face_encodings(img, faces_in_frame)
    
    for encodeFace, faceLoc in zip(encoded_face, faces_in_frame):
        matches = face_recognition.compare_faces(known_faces_encoding, encodeFace, tolerance)
        face_distance = face_recognition.face_distance(known_faces_encoding, encodeFace)
        matchIndex = np.argmin(face_distance)
        
        if matches[matchIndex]:
            return "matched"
        else:
            return "unmatched"     