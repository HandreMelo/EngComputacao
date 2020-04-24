import face_recognition
import numpy as np
import pickle

def cadastrar(file,name):
    all_face_encodings = {}
    load_image = face_recognition.load_image_file(file)
    image_encoding = face_recognition.face_encodings(load_image)[0]
    all_face_encodings[name] = image_encoding
    try:
        with open('dataset_faces.dat', 'wb') as f:
            pickle.dump(all_face_encodings, f)
    except:
        return "Ocorreu um erro ao salvar os dados"
    
    return "Foto cadastrada com sucesso"

def procurar(file):
    # Load face encodings
    try:
        with open('dataset_faces.dat', 'rb') as f:
            all_face_encodings = pickle.load(f)
    except:
        return "Ocorreu um erro ao carregar os dados"

    # Grab the list of names and the list of encodings
    face_names = list(all_face_encodings.keys())
    face_encodings = np.array(list(all_face_encodings.values()))

    # Try comparing an unknown image
    unknown_image = face_recognition.load_image_file(file)
    unknown_face = face_recognition.face_encodings(unknown_image)
    count=-1
    for res in face_recognition.compare_faces(face_encodings, unknown_face):
        count+=1
        if res==True:
            print(face_names[count])
            return face_names[count]
        else:
            print("NADA")
            return "Não cadastrado"
