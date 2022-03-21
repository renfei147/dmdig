import logging
import os
from gensim.models.word2vec import Word2Vec

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model_file = "../data/model/model.word2vec"
download_path = "../data/download/"


class DocumentsFromFiles:
    def __iter__(self):
        for filename in os.listdir(download_path):
            with open(download_path + filename, "r", encoding="utf-8") as file:
                for line in file:
                    tokens = line.strip().split("\t")
                    yield tokens


model = Word2Vec(DocumentsFromFiles(), vector_size=256, min_count=2, epochs=25)
model.save(model_file)
