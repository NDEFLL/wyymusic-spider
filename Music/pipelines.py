# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
import pymysql

# 图片存储
class ImagePipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")
    def get_media_requests(self,item,info):
        pic_url = item['PicUrl']
        yield scrapy.Request(pic_url)   #发送请求下载图片   yield返回请求

    def item_completed(self, results, item, info):
        #获取图片路径同时判断这个路径是否正确，如果正确放到image_path里
        #遍历results，ok表示图片下载成功
        image_path = [x["path"] for ok, x in results if ok]
        if image_path:
            old_path = os.path.join(self.IMAGES_STORE, image_path[0])
            new_path = os.path.join(self.IMAGES_STORE, item["SongsListID"] + ".jpg")

            # 如果目标文件已存在，先删除（用于更新图片）
            if os.path.exists(new_path):
                os.remove(new_path)

            os.rename(old_path, new_path)

        return item

        #更新item中图片路径的字段
        # item["ImagePath"] = os.path.join(self.IMAGES_STORE + "/" + item["PicName"])

#数据库存储管道
class MySQLPipeline_songlist:
    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            user='用户名',
            password='密码',
            db='数据库'
        )
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        sql = ("insert into `playlist`(`playlist_id`,`title`,`creator`,`tag1`,`tag2`,`tag3`,"
               "`playcount`,`collection`,`shares`,`comments`,`songcount`,`create_time`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
               " ON DUPLICATE KEY UPDATE "
               " `title`=VALUES(`title`),"
               "`tag1`=VALUES(`tag1`),"
               "`tag2`=VALUES(`tag2`),"
               "`tag3`=VALUES(`tag3`),"
               "`playcount`=VALUES(`playcount`), "
               "`collection`=VALUES(`collection`),"
               "`shares`=VALUES(`shares`),"
               "`comments`=VALUES(`comments`),"
               "`songcount`=VALUES(`songcount`)")

        self.cursor.execute(sql, [item['SongsListID'], item['SongListName'],
                                  item['AuthorName'], item['Tag1'], item['Tag2'], item['Tag3'], item['PlayCount'],
                                  item['Collection'], item['Forwarding'], item['Comment'], item['SongsCount'],
                                  item['CreationDate']])
        self.conn.commit()

        return item

    def close_spider(self,spider):
        #关闭游标
        self.cursor.close()
        #关闭连接
        self.conn.close()
        print('MySQL数据写入完成')

