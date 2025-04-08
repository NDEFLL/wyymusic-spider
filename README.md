# 网易云音乐歌单爬虫

这是一个网易云音乐数据采集项目，包含两个主要部分：
1. 基于Scrapy框架的歌单信息爬虫
2. 基于JS逆向技术的评论数据采集脚本

## 功能特点

- 歌单爬虫部分：
  - 爬取网易云音乐热门歌单信息
  - 自动下载歌单封面图片到本地文件夹
  - 数据存储到MySQL数据库
  - 支持分页爬取
  - 自动处理图片命名和存储

- 评论采集部分：
  - 使用JS逆向技术获取评论数据
  - 支持获取歌单评论信息
  - 实时打印评论数据（包括评论ID、内容、时间、IP位置、用户ID、点赞数等）

## 项目结构

```
.
├── Music/                    # Scrapy爬虫项目目录
│   ├── spiders/
│   │   ├── musicList.py      # 主爬虫文件
│   │   ├── execute.py        # 爬虫执行文件
│   │   └── __init__.py
│   ├── items.py              # 数据模型定义
│   ├── pipelines.py          # 数据处理管道
│   ├── settings.py           # 项目配置
│   ├── middlewares.py        # 中间件
│   └── __init__.py
├── comments.py               # 评论爬取脚本
└── scrapy.cfg                # Scrapy项目配置文件
```

## 安装说明

1. 确保已安装Python 3.9或更高版本
2. 安装项目依赖：
   ```bash
   # 核心框架依赖
   pip install scrapy           # 爬虫框架
   
   # 数据库操作依赖
   pip install pymysql          # MySQL数据库连接
   
   # 评论爬取脚本依赖（用于comments.py）
   pip install pycryptodome     # 用于AES加密（评论API加密）
   pip install requests         # 用于发送HTTP请求（评论API调用）
   ```

3. 配置MySQL数据库：
   - 创建数据库：`musiclist`
   - 修改`pipelines.py`中的数据库连接信息：
     ```python
     host='localhost'
     port=3306
     user='用户名'
     password='密码'
     db='数据库名'
     ```

4. 配置图片存储路径：
   - 在`settings.py`中修改`IMAGES_STORE`路径：
     ```python
     IMAGES_STORE = "你的图片存储路径"
     ```

## 使用方法

1. 运行歌单爬虫：
   ```bash
   cd Music/spiders
   python execute.py
   ```
   - 这将爬取歌单信息并存储到MySQL数据库
   - 同时下载歌单封面图片到指定本地文件夹

2. 运行评论采集：
   ```bash
   python comments.py
   ```
   - 这将获取歌单评论数据并在控制台打印
   - 评论数据包括：评论ID、内容、时间、IP位置、用户ID、点赞数等

## 数据字段说明

爬取的数据包括以下字段：
- 歌单ID
- 歌单名称
- 作者名称
- 创建日期
- 播放量
- 标签（最多3个）
- 收藏量
- 转发量
- 评论量
- 歌曲数量
- 封面图片URL
- 评论数据（包括评论ID、内容、时间、IP位置、用户ID、点赞数等）

## 注意事项

1. 请遵守网易云音乐的robots.txt规则
2. 建议设置适当的下载延迟，避免对目标网站造成过大压力
3. 确保有足够的磁盘空间存储图片
4. 数据库连接信息请妥善保管

## 许可证

MIT License 
