from gensim.models.word2vec import Word2Vec
import jieba
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import joblib
import numpy as np

jieba.dt.tmp_dir = "../data/jieba"

model = Word2Vec.load("../data/model/model.word2vec")

in_files = ["../data/class/main.txt", "../data/class/sad.txt", "../data/class/more.txt", "../data/class/dict.txt"]
out_file = "../data/model/class.pkl"

x_train = []
y_train = []
for in_file in in_files:
    with open(in_file, "r", encoding="utf-8") as file:
        for line in file:
            type, text = line.strip().split("\t")
            tokens = list(jieba.cut(text))
            tokens = [token for token in tokens if token in model.wv.key_to_index.keys()]
            vector = np.mean(model.wv[tokens], axis=0) if len(tokens) > 0 else np.zeros(model.vector_size)
            x_train.append(vector)
            y_train.append(int(type))

logreg = LogisticRegression(n_jobs=-1, C=1e5, max_iter=30000)
logreg.fit(x_train, y_train)

y_pred = logreg.predict(x_train)
print('Testing accuracy %s' % accuracy_score(y_train, y_pred))
print('Testing F1 score: %s' % f1_score(y_train, y_pred, average='weighted'))

joblib.dump(logreg, out_file)
