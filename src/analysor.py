from gensim.models.word2vec import Word2Vec
import joblib
import numpy as np

model_file = "../data/model/model.word2vec"
class_file = "../data/model/class.pkl"

model = None
class_model = None


def get_emotion(tokens):
    global model, class_model
    if model is None:
        model = Word2Vec.load(model_file)
    if class_model is None:
        class_model = joblib.load(class_file)
    # vec = model.infer_vector(tokens)
    tokens = [token for token in tokens if token in model.wv.key_to_index.keys()]
    vector = np.mean(model.wv[tokens], axis=0) if len(tokens) > 0 else np.zeros(model.vector_size)
    e = class_model.predict([vector])[0]
    return e
