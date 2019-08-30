# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 15:42:39 2019

@author: aakansha.dhawan
"""

import pickle
from PIL import Image
from numpy import asarray
from numpy import expand_dims
from mtcnn.mtcnn import MTCNN
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model

out_encoder = LabelEncoder()
def extract_face(filename, required_size=(160, 160)):
    # load image from file
    image = Image.open(filename)
    # convert to RGB, if needed
    image = image.convert('RGB')
    # convert to array
    pixels = asarray(image)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    # bug fix
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    #image.show()
    return face_array

def get_embedding(model, face_pixels):
    # scale pixel values
    face_pixels = face_pixels.astype('float32')
    # standardize pixel values across channels (global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    print(face_pixels.shape)
    # transform face into one sample
    samples = expand_dims(face_pixels, axis=0)
    print(samples.shape)
    # make prediction to get embedding
    yhat = model.predict(samples)
    return yhat[0]

def predict(image):
    filename = 'C:/Users/anchal.chaudhary/Desktop/hackathon/Love-Peace-Code/facedetector/finalized_model.sav'
    model_svm = pickle.load(open(filename, 'rb'))

    extracted_face=extract_face(image)
    
    model = load_model('C:/Users/anchal.chaudhary/Desktop/hackathon/Love-Peace-Code/facedetector/facenet_keras.h5')
    face_emmbed = get_embedding(model, extracted_face)
    
    face_emmbed = asarray(face_emmbed)
    
    face_emmbed = expand_dims(face_emmbed, axis=0)
    yhat_class = model_svm.predict(face_emmbed)
    yhat_prob = model_svm.predict_proba(face_emmbed)
    
    class_index = yhat_class[0]
    class_probability = yhat_prob[0,class_index] * 100

    if class_probability > 80 :
        if yhat_class[0]==0 :
            name="aakansha"
        if yhat_class[0]==1 :
            name="ben_afflek"
        if yhat_class[0]==2 :
            name="elton_john"
        if yhat_class[0]==3 :
            name="jerry_seinfeld"
        if yhat_class[0]==4 :
            name="madonna"
        if yhat_class[0]==5 :
            name="mindy_kaling"
    else:
        name=""
        
    return name,class_probability