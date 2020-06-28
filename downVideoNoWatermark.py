# -*- coding: utf-8 -*-
"""
@Time      : 2020/6/24 11:06
@Author    : William.sv@icloud.com
@File      : downVideoNoWatermark.py
@ Software : PyCharm
@Desc      :
"""

import requests
from urllib import parse
from bs4 import BeautifulSoup as bs

class DyDown:
    def __init__(self):
        self.headers = {
            'Host': 'v.douyin.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.user_agent = {
            'pc': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'mobile': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }
        self.s = requests.session()

    def down(self):
        url = input('请输入需要下载的抖音视频链接：')
        video_down_url = self.__get_video_url(url)
        print('抖音视频无水印版下载链接为：' + video_down_url)
        save_name = input('视频名字保存为：')
        self.__save(video_down_url, save_name)

    def __get_video_url(self,url):
        video_down_url = ''
        self.headers['User-Agent'] = self.user_agent['pc']
        r = self.s.get(url=url,headers=self.headers,allow_redirects=False)
        soup = bs(r.content, 'html5lib')
        next_url = soup.find('a')['href']
        result = parse.urlparse((next_url))
        item_ids = result.path.split('/')[-2]
        video_api_url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + item_ids
        self.headers['Host'] = 'www.iesdouyin.com'
        self.headers['Accept'] = '*/*'
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['Referer'] = next_url
        video_url = self.s.get(url=video_api_url,headers=self.headers)
        data = video_url.json()
        if 'item_list' in data and len(data['item_list']) > 0:
            video_vid = data['item_list'][0]['video']['vid']
            video_down_url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=' + video_vid + '&ratio=720p&line=0'

        return video_down_url

    def __save(self,url,save_name):
        self.headers['Host'] = 'aweme.snssdk.com'
        self.headers['User-Agent'] = self.user_agent['mobile']
        self.headers['Accept'] = 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        r = self.s.get(url=url,headers=self.headers,allow_redirects=False)
        soup = bs(r.content, 'html5lib')
        next_url = soup.find('a')['href']
        r2 = self.s.get(url=next_url,stream=True)
        with open(r'.\\' + save_name + '.mp4', 'wb') as mp4:
            for chunk in r2.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    mp4.write(chunk)
        print('视频已保存~')


def main():
    DyDown().down()

if __name__ == '__main__':
    main()