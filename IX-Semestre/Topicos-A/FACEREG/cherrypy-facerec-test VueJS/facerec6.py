import face_recognition
import numpy as np
from dataIO import pk as pickle
import time
#import image_decoder as imdec
#https://pythonhosted.org/dataIO/pk.html
def cadastrar(file,name):
    all_face_encodings = {}
    pickle_file = 'dataset_faces.pickle'
    load_image = face_recognition.load_image_file(file)
    image_encoding = face_recognition.face_encodings(load_image)[0]
    try:
        all_face_encodings = pickle.load(pickle_file)
    except:
        print("Arquivo vazio")
        print("Depois : "+str(all_face_encodings))
    try:
        all_face_encodings[name] = image_encoding
        pickle.safe_dump(all_face_encodings, pickle_file)

    except:
        raise
        return "Ocorreu um erro ao salvar os dados"
    
    return "Foto cadastrada com sucesso"
    
def deletar(name):
    all_face_encodings = {}
    pickle_file = 'dataset_faces.pickle'
    try:
        all_face_encodings = pickle.load(pickle_file)
    except:
        print("Arquivo vazio")
    try:
        all_face_encodings.pop(name)
        pickle.safe_dump(all_face_encodings, pickle_file)
        print("Depois : "+str(all_face_encodings))
        
    except:
        return "Ocorreu um erro ao salvar os dados"
    
    return "Usuário removido com sucesso."
    
def atualizar(file,name):
    all_face_encodings = {}
    pickle_file = 'dataset_faces.pickle'
    load_image = face_recognition.load_image_file(file)
    image_encoding = face_recognition.face_encodings(load_image)[0]
    try:
        all_face_encodings = pickle.load(pickle_file)
    except:
        print("Arquivo vazio")
    try:
        all_face_encodings[name] = image_encoding
        pickle.safe_dump(all_face_encodings, pickle_file)

    except:
        raise
        return "Ocorreu um erro ao salvar os dados"
    
    return "Foto atualizada com sucesso"

def procurar(file):

    print("TIPO  :::::: ")
    print(type(file))
    # Load face encodings
    all_face_encodings = {}
    pickle_file = 'dataset_faces.pickle'
    erro = ""
    try:
        all_face_encodings = pickle.load(pickle_file)
        print(all_face_encodings)
        if all_face_encodings:
            print(all_face_encodings.keys())
        else:
            erro = "Ninguem Cadastrado"
    except:
        erro = "Não foi possivel acessar o banco de dados"
        return erro

    # Grab the list of names and the list of encodings
    face_names = list(all_face_encodings.keys())
    print("FACE NAMES")
    print(face_names)
    face_encodings = np.array(list(all_face_encodings.values()))

    # Try comparing an unknown image
    unknown_image = face_recognition.load_image_file(file)
    #unknown_image = file
    unknown_face = face_recognition.face_encodings(unknown_image)
    result = face_recognition.compare_faces(face_encodings, unknown_face)

    # Print the result as a list of names with True/False
    names_with_result = dict(zip(result, face_names))
    if True in names_with_result.keys():
        return names_with_result[True]
    return "Não encontrou ninguém"