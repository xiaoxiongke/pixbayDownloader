# https://pixabay.com/api/videos/?key=23946513-5258cec0cebe448ba5a533e87&q=yellow+flowers

import imp
from urllib.parse import urlencode
from urllib import parse
from enum import Enum, unique

import requests
import os,sys
import time
# todo: 可以改成自动获取API_KEY
API_KEY = "your api key" # 替换成你的API_KEY
# todo: 可以改成自己的保存路径
DOWNLOAD_FILE_PATH = '/Users/xxx/Desktop/pixabayDownload/' # 替换成你的保存路径
class Spider():

    @unique
    class DownloadType(Enum):
        All = 0 # 默认下载全部
        Video = 1
        Photo = 2

    def __init__(self):
        self.keyword = input('欢迎使用pixabay视频搜索下载器\n请输入搜索关键词(推荐输入英文)：')
        self.downloadType = input("下载类型:0全部(默认),1:视频,2:图片)\n")
        self.p = 1080 #默认1080p
        self.videoPage = 1
        self.picPage = 1
        self.perPage = 20
        self.picURL = "https://pixabay.com/api/?key="+API_KEY+"&q="+parse.quote(self.keyword)+"&pretty=true"+"&page="+str(self.picPage)+"&per_page="+str(self.perPage)
        self.videoURL = "https://pixabay.com/api/videos/?key="+API_KEY+"&q="+parse.quote(self.keyword)+"&pretty=true"+"&page="+str(self.videoPage)+"&per_page="+str(self.perPage)
        self.path = DOWNLOAD_FILE_PATH
        self.searchedKeywordsDirPath = ""
        # 是否存在
        self.isExists = os.path.exists(self.path)
        # 判断结果
        if not self.isExists:
            # 如果不存在则创建目录
            os.makedirs(self.path)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            pass
    
    def getSource(self, url):
        results = requests.get(url).json()
        return results

    def downloadResource(self,type):
        if not os.path.exists(self.searchedKeywordsDirPath):
            os.makedirs(self.searchedKeywordsDirPath)

        if type == self.DownloadType.Photo:
            self.downloadPhoto()
        elif type == self.DownloadType.Video:
            self.downloadVideo()
        else:
            self.downloadVideo()
            self.downloadPhoto()


    def downloadPhoto(self):
        while True:
            self.picURL = "https://pixabay.com/api/?key="+API_KEY+"&q="+parse.quote(self.keyword)+"&pretty=true"+"&page="+str(self.picPage)+"&per_page="+str(self.perPage)
            results = spider.getSource(self.picURL)
            print("找到了"+str(len(results['hits']))+"个图片")
            # 下载图片
            if results['totalHits'] == 0:
                print("没有找到图片")
                break
            print("正在下载第"+str(self.picPage)+"页")
            for picBlock in results["hits"]:
                downloadPicUrl = ""
                try:
                    downloadPicUrl = picBlock["fullHDURL"]
                except:
                    print("没有1080p图片,换为其他大图")
                    downloadPicUrl = picBlock["largeImageURL"]
                tags = picBlock["tags"]
                picName = tags+"_"+str(picBlock["imageHeight"])+"p.jpg"
                print("正在下载:"+picName)
                downloadPic = requests.get(downloadPicUrl)
                filePath = self.searchedKeywordsDirPath+"/"+picName
                # 保存文件 如果文件已存在则改名称
                if os.path.exists(filePath):
                    filePath = self.searchedKeywordsDirPath+"/"+picName+"_"+str(time.time())+".jpg"
                with open(filePath, 'wb') as f:
                    f.write(downloadPic.content)
                print("下载完成:" + picName)
                time.sleep(1)
            self.picPage += 1
            if len(results["hits"]) < self.perPage:
                print("已到达最后一页")
                break
        self.picPage = 1

    def downloadVideo(self):
        while True:
            self.videoURL = "https://pixabay.com/api/videos/?key="+API_KEY+"&q="+parse.quote(self.keyword)+"&pretty=true"+"&page="+str(self.videoPage)+"&per_page="+str(self.perPage)
            results = self.getSource(self.videoURL)
            print("找到了"+str(len(results['hits']))+"个视频")
            if results['totalHits'] == 0:
                print("没有找到视频")
                break
            print("正在下载第"+str(self.videoPage)+"页")
            # 下载视频
            for videoBlock in results["hits"]:
                videos = videoBlock["videos"]
                tags = videoBlock["tags"]
                for video,value in videos.items():
                    if value["height"] <= spider.p and value["height"] > 720 or value["height"] == "1080":
                        videoURL = value["url"]
                        videoName = tags+"_"+str(value["height"])+"p.mp4"
                        print("正在下载:"+videoName)
                        downloadVideo = requests.get(videoURL)
                        filePath = self.searchedKeywordsDirPath+"/"+videoName
                        # 保存文件 如果文件已存在则改名称
                        if os.path.exists(filePath):
                            filePath = self.searchedKeywordsDirPath+"/"+videoName+"_"+str(time.time())+".mp4"
                        with open(filePath, 'wb') as f:
                            f.write(downloadVideo.content)
                        print("下载完成:" + videoName)
                time.sleep(1)
            self.videoPage += 1
            if len(results["hits"]) < self.perPage:
                print("已到达最后一页")
                break
        self.videoPage = 1



if __name__ == '__main__':
    spider = Spider()
    # 搜索视频的对应文件夹路径
    spider.searchedKeywordsDirPath = spider.path+spider.keyword
    spider.downloadResource(spider.downloadType)
