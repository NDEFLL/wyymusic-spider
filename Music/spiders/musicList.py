import scrapy
from ..items import MusicItem
from copy import deepcopy
import re

class MusiclistSpider(scrapy.Spider):
    name = "musicList"
    allowed_domains = ["music.163.com"]
    # start_urls = ["https://music.163.com/discover/playlist"]
    start_urls = ["https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=175"]

    offset = -1      #用于记录当前爬取的页数

    def parse(self, response):
        #获取到一页的全部歌单
        liList = response.xpath("//div[@id='m-disc-pl-c']/div/ul[@id='m-pl-container']/li")

        #遍历一页的所有歌单，获取到歌单详细页面的信息
        for li in liList:
            musicItem = MusicItem()

            #歌单的id
            a_href = li.xpath("./div/a[@class = 'msk']/@href").extract_first()
            musicItem["SongsListID"] = a_href[13:]
            print(a_href)

            #详细页面url
            songs_Url = "https://music.163.com/" + a_href
            musicItem["SongsUrl"] = songs_Url
            # 调用SongsListPageParse来获取歌单详细页面的信息
            yield scrapy.Request(songs_Url,meta={"musicItem": deepcopy(musicItem)},
                                 callback=self.SongsListPageParse,)

        if self.offset < 20:     #设置offset为最后的页数-1，因为第一页的offset为0
            self.offset += 1
            # 获取下一页的Url地址   offset为(页数-1)*35
            nextpage_a_url = "https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=" + str(
                self.offset * 35)
            # print('正在爬取第' + str(self.offset + 1) + '页')
            yield scrapy.Request(nextpage_a_url, callback=self.parse)

    def SongsListPageParse(self,response):
        cntc = response.xpath("//div[@class='cntc']")
        musicItem = response.meta['musicItem']

        #歌单名
        songsListName = cntc.xpath("./div[@class='hd f-cb']/div/h2//text()").extract_first()
        musicItem["SongListName"] = songsListName

        # 歌单作者名
        user_name = cntc.xpath("././div[@class='user f-cb']/span[@class='name']/a/text()").extract_first()
        musicItem["AuthorName"] = user_name

        #歌单创建日期
        time = cntc.xpath("./div[@class='user f-cb']/span[@class='time s-fc4']/text()").extract_first()
        musicItem["CreationDate"] = time[0:10]

        #歌单收藏量
        aList = cntc.xpath("./div[@id='content-operation']/a")
        Collection = aList[2].xpath("./@data-count").extract_first()
        musicItem["Collection"] = Collection

        #转发量
        Forwarding = aList[3].xpath("./@data-count").extract_first()
        musicItem["Forwarding"] = Forwarding

        #评论量
        Comment = aList[5].xpath("./i/span[@id='cnt_comment_count']/text()").extract_first()
        musicItem["Comment"] = Comment

        #歌曲数量
        songtbList = response.xpath("//div[@class='n-songtb']/div")
        songsCount = songtbList[0].xpath("./span[@class='sub s-fc3']/span[@id='playlist-track-count']/text()").extract_first()
        musicItem["SongsCount"] = songsCount

        #播放量
        playCount = songtbList[0].xpath("./div[@class='more s-fc3']/strong[@id='play-count']/text()").extract_first()
        musicItem["PlayCount"] = playCount

        #歌单标签
        tags = ""
        tagList = cntc.xpath("./div[@class='tags f-cb']/a")
        for a in tagList:
            tags = tags + a.xpath("./i/text()").extract_first() + ","
        # 去除尾部的逗号
        tags = tags.rstrip(',')

        # 使用条件判断避免索引超出范围
        tag_list = tags.split(",")  # 将字符串转为列表
        # 默认值为空字符串，确保即使没有标签也不会报错
        tag1 = tag_list[0] if len(tag_list) > 0 else ""
        tag2 = tag_list[1] if len(tag_list) > 1 else ""
        tag3 = tag_list[2] if len(tag_list) > 2 else ""

        musicItem["Tag1"] = tag1
        musicItem["Tag2"] = tag2
        musicItem["Tag3"] = tag3

        #图片名称
        pic_name = "歌单 《"+songsListName + "》 封面"
        #去除图片名称中的特殊字符，以确保在保存图片时能够正确地给图片重命名并保存
        cleaned_filename = re.sub(r'[\\/:"*?<>/【】|]', '', pic_name)
        musicItem["PicName"] = cleaned_filename

        # 图片链接
        pic_url = response.xpath("//div[@class='cover u-cover u-cover-dj']/img/@src").extract_first()
        musicItem["PicUrl"] = response.urljoin(pic_url)

        yield musicItem





