import pickle
from PIL import Image
from numpy import asarray
from numpy import expand_dims
from mtcnn.mtcnn import MTCNN
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
import flask
from keras import backend as K

out_encoder = LabelEncoder()
# Create Flask application and initialize Keras model
app = flask.Flask(__name__)
model = None


def extract_face(filename, required_size=(160, 160)):
    print("Here")
    image = Image.open(filename)
    image = image.convert('RGB')
    pixels = asarray(image)
    detector = MTCNN()
    results = detector.detect_faces(pixels)
    x1, y1, width, height = results[0]['box']
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = pixels[y1:y2, x1:x2]
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array


def get_embedding(model, face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    print(face_pixels.shape)
    samples = expand_dims(face_pixels, axis=0)
    print(samples.shape)
    yhat = model.predict(samples)
    return yhat[0]


# Function to Load the model
def load_model1():
    global model_svm
    model_svm = pickle.load(open('finalized_model.sav', 'rb'))


def prepare_image(image):
    extracted_face = extract_face(image)
    print("here2")
    model = load_model('facenet_keras.h5')
    face_emmbed = get_embedding(model, extracted_face)
    face_emmbed = asarray(face_emmbed)
    face_emmbed = expand_dims(face_emmbed, axis=0)
    return face_emmbed


# Now, we can predict the results.
@app.route("/predict", methods=["POST"])
def predict():
    # data = {} # dictionary to store result
    # data["success"] = False

    # Check if image was properly sent to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            print(flask.request.files["image"].filename)
            image = flask.request.files["image"].filename
            print("123")
            print(image)
            K.clear_session()
            emmbed = prepare_image(image)

            K.clear_session()
            yhat_class = model_svm.predict(emmbed)
            yhat_prob = model_svm.predict_proba(emmbed)

            K.clear_session()
            class_index = yhat_class[0]
            class_probability = yhat_prob[0, class_index] * 100

            if yhat_class[0] == 0:
                name = "aakansha"
            if yhat_class[0] == 1:
                name = "ben_afflek"
            if yhat_class[0] == 2:
                name = "elton_john"
            if yhat_class[0] == 3:
                name = "jerry_seinfeld"
            if yhat_class[0] == 4:
                name = "madonna"
            if yhat_class[0] == 5:
                name = "mindy_kaling"

            r = {"label": name, "probability": float(class_probability)}
            # data["predictions"].append(r)

            # data["success"] = True

    # return JSON response
    return flask.jsonify(r)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_model1()
    app.run()
