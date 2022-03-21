import bilibili
import os
import jieba
import requests
import re

jieba.dt.tmp_dir = "../data/jieba"

download_path = "../data/download/"
list_file = "../data/list.txt"

video_set = set(os.listdir(download_path))


def download(video_id):
    print("Downloading " + video_id, end=' ')
    if (video_id in video_set):
        print("Pass")
    else:
        _, dm_list = bilibili.get_danmaku(video_id)
        with open(download_path + video_id, "w", encoding="utf-8") as out:
            out.writelines(["\t".join(list(jieba.cut(dm.text.strip()))) + "\n" for dm in dm_list])
        print("OK")


def download_raw(video_ids):
    ret = []
    for video_id in video_ids:
        print("Downloading " + video_id, end=' ')
        _, dm_list = bilibili.get_danmaku(video_id)
        ret.extend([dm_list[i].text for i in range(0, len(dm_list), max(50, len(dm_list) // 100))])
        print("OK")
    return ret


with open(list_file, "r", encoding="utf-8") as file:
    for line in file:
        download(line.strip())
'''
with open(list_file, "a", encoding="utf-8") as file:
    res = requests.get("https://api.bilibili.com/x/web-interface/popular/series/one?number=150")
    s = set(re.findall("BV[a-zA-Z0-9]{10}", res.text))
    list.writelines([line + '\n' for line in s])
'''
'''
ids = []
with open("select_list.txt", "r", encoding="utf-8") as file:
    for line in file:
        ids.append(line.strip())

lines = download_raw(ids)
lines = list(dict.fromkeys(lines))

with open("select.txt", "w", encoding="utf-8") as out:
    out.writelines([line + "\n" for line in lines])
'''
'''
ids = ["av73437753"]

lines = download_raw(ids)
lines = list(dict.fromkeys(lines))

with open("addition.txt", "w", encoding="utf-8") as out:
    out.writelines([line + "\n" for line in lines])
'''