import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage


def encode_event():
    cred_certificate = credentials.Certificate("Key.json")
    try:
        firebase_admin.initialize_app(cred_certificate, {
        'databaseURL': "https://faceattendacerealtime-66ada-default-rtdb.firebaseio.com/",
        'storageBucket': "faceattendacerealtime-66ada.appspot.com"
        })
    except:
        print("encode error")
    path_folder = 'Images'
    list_path = os.listdir(path_folder)
    list_path.remove(".DS_Store")
    list_img = []
    id_students = []
    for path in list_path:
        list_img.append(cv2.imread(os.path.join(path_folder, path)))
        id_students.append(os.path.splitext(path)[0])
        fileName = f'{path_folder}/{path}'
        bucket = storage.bucket()
        blob = bucket.blob(fileName)
        blob.upload_from_filename(fileName)

    def findEncodings(imagesList):
        encodeList = []
        for img in imagesList:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(img)
            if len(face_encodings) > 0:
                encode = face_encodings[0]
                encodeList.append(encode)
            else:
                print("No faces found in the image.")

        return encodeList

    list_encode_known = findEncodings(list_img)
    list_encode_knownWithIds = [list_encode_known, id_students]

    file = open("EncodeFile.p", 'wb')
    pickle.dump(list_encode_knownWithIds, file)
    file.close()
    print("---Encode Complete---")