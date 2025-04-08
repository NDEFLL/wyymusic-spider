# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ongsListID = scrapy.Field()  # 歌单id号（唯一标识符，用于数据关联）
    SongListName = scrapy.Field()  # 歌单名
    AuthorName = scrapy.Field()  # 作者名
    CreationDate = scrapy.Field()  # 歌单创建日期（时间序列分析）
    PlayCount = scrapy.Field()  # 播放量（衡量歌单热度）
    Tags = scrapy.Field()  # 标签名
    SongsUrl = scrapy.Field()  # 歌单域名，为下一次详细爬取留备份
    Collection = scrapy.Field()  # 歌单收藏量（衡量用户喜爱度）
    Forwarding = scrapy.Field()  # 转发量(分享量，衡量传播效果)
    Comment = scrapy.Field()  # 评论量（用户互动指标）
    SongsCount = scrapy.Field()  # 歌曲数量
    PicUrl = scrapy.Field()  # 图片url
    Pic = scrapy.Field()  # 图片
    PicName = scrapy.Field()  # 图片名称
    ImagePath = scrapy.Field()  # 图片路径
    Tag1 = scrapy.Field()
    Tag2 = scrapy.Field()
    Tag3 = scrapy.Field()
    songlist = scrapy.Field()  # 歌曲列表（歌曲ID、歌手、时长等）



