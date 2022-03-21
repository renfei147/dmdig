import imp
import os
from flask import Flask, jsonify
import bilibili
import math
from danmaku import Danmaku
import jieba
from analysor import get_emotion

jieba.dt.tmp_dir = "../data/jieba"
app = Flask(__name__, static_url_path="", static_folder="../html")
app.config["JSON_AS_ASCII"] = False
IS_SERVERLESS = bool(os.environ.get('SERVERLESS'))


@app.route("/")
def home():
    return app.send_static_file("index.html")


@app.route("/api/bilibili/<video_id>")
def process(video_id):
    try:
        length, dms = bilibili.get_danmaku(video_id)
        slice_length = 2
        slice_num = math.ceil((length + 5) / slice_length)
        slices = [{"n": 0, "w": {}, "e": [0] * 7} for i in range(slice_num)]
        for dm in dms:
            s = slices[math.floor(dm.time / slice_length)]
            s["n"] += 1
            tokens = list(jieba.cut(dm.text))
            for word in tokens:
                if (word in s["w"]):
                    s["w"][word] += 1
                else:
                    s["w"][word] = 1
            e = get_emotion(tokens)
            s["e"][e] += 1
        return jsonify({"success": True, "video_length": length, "slice_length": slice_length, "slices": slices})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


app.run(debug=IS_SERVERLESS != True, port=9000, host='0.0.0.0')