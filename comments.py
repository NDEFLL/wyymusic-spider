import requests
import json
import pymysql
# 实现AES加密需要的三个模块
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode

def conn_mysql():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        database='musiclist'
    )

    return conn

def close_conn(conn):
    if conn:
        conn.close()

sql = "select playlist_id from playlist;"
conn =  conn_mysql()
cursor = conn.cursor()
cursor.execute(sql)
result = cursor.fetchall()

# 使用列表推导式将每个元组中的元素提取出来
# 遍历元组中的元组，取每个元组中的第一个元素
ids = [x[0] for x in result]

# print(ids)

# py实现AES-CBC加密
def encrypt_aes(text, key, iv):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    padded_text = pad(text.encode('utf-   ++8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return b64encode(ciphertext).decode('utf-8')

# 仿照function b(a, b)构造加密函数
def b(a, b):
    c = b
    d = "0102030405060708"
    e = a
    f = encrypt_aes(e, c, d)
    return f

# 评论数据(i2x)
# d = {
#     "csrf_token": "",
#     "cursor": "-1",
#     "offset": "0",
#     "orderType": "1",
#     "pageNo": "1",
#     "pageSize": "20",   #评论数
#     "rid": "A_PL_0_26467411",   #歌曲/歌单编号  歌单编号为A_PL_0_歌单ID  歌曲编号为R_SO_4_歌曲ID
#     "threadId": "A_PL_0_26467411"   #歌曲/歌单编号
# }

for id in ids:
    d = {"rid": f"A_PL_0_{id}",     #歌曲/歌单编号  歌单编号为A_PL_0_歌单ID  歌曲编号为R_SO_4_歌曲ID
         "threadId": f"A_PL_0_{id}",    #歌曲/歌单编号
         "pageNo": "1",
         "pageSize": "20",  #每页的评论数
         "cursor": "-1",    #分页请求中的游标，"-1"表示从第一页开始
         "offset": "0",     #控制页数，0-19第一页 20-39第二页，以此类推
         "orderType": "1",
         "csrf_token": ""}  #CSRF令牌

    # 16位随机字符串
    i = "yBod36O44VkfXOta"
    # Pg2x(["流泪", "强"])
    e = "010001"
    # Pg2x(mR5W.md, mR5W.emj)
    f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    # Pg2x(["爱心", "女孩", "惊恐", "大笑"])
    g = "0CoJUm6Qyw8W8jud"

    # 将i2x转化为json格式
    d_json = json.dumps(d)

    # 调用两次b()函数得出encText
    encText = b(d_json, g)
    encText = b(encText, i)

    # 随机字符串获得encSecKey
    encSecKey = "36050b3d14c8421e47f4072b655e9e5b74dd301eb8a4317164d18aebff5201b5a4a248d8fdc332cc7ac16cc39c393c298dfc94f597be7232c4308fd8ca305d96e88ad8a2febd379de58722496e82e286d742c0766d12e0a0a0b0800881a43e1713770e474cf4848173834ee2e9b1feea0831834dd6cd0e2db273dea49f911d0b"
    # 请求头
    headers = {
        'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    }

    # 评论数据的请求地址
    url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='

    # 将encText和encSecKey打包起来
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }

    # 发送post请求并携带encText和encSecKey得到评论的json格式
    respond = requests.post(url, headers=headers, data=data).json()
    # 打印
    # print(respond)
    comments = respond["data"]["comments"]
    for comment in comments:
        comment_id = comment['commentId']
        playlist_id = id
        content = comment['content']
        time = comment['time']
        ip_location = comment['ipLocation']['location']
        userid = comment['ipLocation']['userId']
        likes = comment['likedCount']
        print(comment_id,playlist_id,time,content,ip_location,userid,likes)

