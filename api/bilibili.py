import dm_data_pb2
import requests
import math
import re
from danmaku import Danmaku


def get_danmaku(video_id):
    p = 0
    params = {}
    try:
        parts = video_id.split(":", 1)
        if (len(parts) == 2):
            p = int(parts[1]) - 1
        id = parts[0]
        if re.search("^BV[a-zA-Z0-9]{10}$", id):
            params["bvid"] = id
        elif (id[:2] == 'av'):
            params["aid"] = int(id[2:])
        else:
            raise ValueError()
    except ValueError:
        raise RuntimeError("格式错误")

    res = requests.get("https://api.bilibili.com/x/player/pagelist?", params=params).json()
    cid = res["data"][p]["cid"]
    duration = res["data"][p]["duration"]

    view_data_params = {"type": 1, "oid": cid}
    view_data_res = requests.get("https://api.bilibili.com/x/v2/dm/web/view", view_data_params)
    view_data = dm_data_pb2.DmWebViewReply()
    view_data.ParseFromString(view_data_res.content)
    if (view_data.state == 1):
        raise RuntimeError("该视频关闭弹幕")
    seg_length = view_data.dmSge.pageSize / 1000
    total_dm = view_data.count

    dm_list = []
    seg_num = math.ceil(duration / seg_length)
    seg_data = dm_data_pb2.DmSegMobileReply()
    for i in range(seg_num):
        seg_data_params = {"type": 1, "oid": cid, 'segment_index': i + 1}
        seg_data_res = requests.get("https://api.bilibili.com/x/v2/dm/web/seg.so", seg_data_params)
        seg_data.ParseFromString(seg_data_res.content)
        for dm in seg_data.elems:
            dm_list.append(Danmaku(dm.progress / 1000, dm.content))
    return duration, dm_list
