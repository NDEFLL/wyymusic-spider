import base64
import binascii
import json
import random

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


# 需要爬取不同歌单/歌曲，修改rid，threadID，需要修改页码修改pageSize 和 offset
# 如修改歌单id：
"""
    for id in ids:
    d = {
        "rid": f"A_PL_0_{id}",    
        "threadId": f"A_PL_0_{id}"
        ...
    }
"""
d = {
    "rid": f"A_PL_0_13400885874",     #歌曲/歌单编号  歌单编号为A_PL_0_歌单ID  歌曲编号为R_SO_4_歌曲ID
    "threadId": f"A_PL_0_13400885874",    #歌曲/歌单编号
    "pageNo": "1",      #页码
    "pageSize": "20",  #每页的评论数
    "cursor": "-1",    #分页请求中的游标，"-1"表示从第一页开始
    "offset": "0",     #控制页数，0-19第一页 20-39第二页，以此类推
    "orderType": "1",   #排序方式：1 可能表示按热度排序，2 可能是按时间
    "csrf_token": ""
}
e = "010001"    #RSA公钥指数
# RSA公钥模数
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g = "0CoJUm6Qyw8W8jud"  # 第一次AES加密的密钥
i = "0vRj1pvBw2fdb7PS"  # 第二次AES加密的密钥

# AES加密函数
# a是原始明文，b是密钥
def b(a,b):
    c = b.encode('utf-8')
    d = "0102030405060708".encode('utf-8')  # 固定iv向量
    e = a.encode('utf-8')
    e = pad(e, 16)  #填充

    # 创建AES加密对象
    cipher = AES.new(c, AES.MODE_CBC, d)

    # 加密数据
    encrypted_data = cipher.encrypt(e)

    # 返回Base64编码结果
    return base64.b64encode(encrypted_data).decode('utf-8')

encSecKey = "59fffb04b63fc73a2978e07aca285578743dfc7685f2f25531740b199f68ba9bcfc140e1e2a67795fa2f98715d589ddfd8863daa0f5ebb0a5ed87a9d7d4a08c0d1c59d8b033971865703f1bc01d1035a470f075ce230a4ae640205eb23bb118198e63c65e97e153057d4f6aba275d1e76d04f73f8bba5ae28b0f01d16b0c551b"

# 调用两次b函数，传入的数据格式为json
d = json.dumps(d)   #将字典转换为JSON字符串
params = b(d,g)
params = b(params,i)

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
# 请求头
headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://music.163.com/'
}

# 请求数据体
data = {
    "params":params,
    "encSecKey":encSecKey
}

# 发送post请求并携带encText和encSecKey得到评论的json格式
respond = requests.post(url, headers=headers, data=data).json()
comments = respond["data"]["comments"]
for comment in comments:
    comment_id = comment['commentId']   #评论id
    playlist_id = id    #评论的歌单id
    content = comment['content']    #评论内容
    time = comment['time']      #评论时间
    ip_location = comment['ipLocation']['location']     #用户ip
    likes = comment['likedCount']   #点赞数
    print(comment_id,playlist_id,time,content,ip_location,likes)

