'''
from gensim.models.doc2vec import Doc2Vec

model = Doc2Vec.load("../data/model/model.doc2vec")
print("loaded")
print(model.wv.most_similar(positive=['awsl'], topn=5))
'''
import jieba
from analysor import get_emotion

jieba.dt.tmp_dir = "../data/jieba"

names = ["无", "调侃", "赞叹", "感伤", "愤怒", "质疑", "冷静讨论"]


def test(text):
    tokens = list(jieba.cut(text))
    e = get_emotion(tokens)
    print(names[e])
