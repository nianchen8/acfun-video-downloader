"""
缓存文件夹 获取的最终视频文件使用的都是绝对路径
D:/PycharmProjects/demo/文件保存/...
"""
import requests
import re
import json
import os
import time
import subprocess
import shutil

class Acfun:
    def __init__(self):
        self.av = ''
        self.m3u8_url = ''
        self.ts_urls = []
        self.dirname = ''
        self.title = ''

    # 从html中提取m3u8地址
    def get_m3u8_url (self):
        url = f'https://www.acfun.cn/v/{self.av}'
        cookies = {
            '_did': 'web_66863889621946DB',
            'lsv_js_player_v2_main': 'ca85g8',
            'safety_id': 'AAJGw7hWFc1z7HdvlyHBdXn3',
            '_did': 'web_66863889621946DB',
            'csrfToken': 'IScy5otm_kcvlwciqX9_l8Pp',
            'webp_supported': '%7B%22lossy%22%3Atrue%2C%22lossless%22%3Atrue%2C%22alpha%22%3Atrue%2C%22animation%22%3Atrue%7D',
            'Hm_lvt_2af69bc2b378fb58ae04ed2a04257ed1': '1774624043,1774693996',
            'HMACCOUNT': '85B371DDC9AC8F11',
            'cur_req_id': '6160208745A74BCF_self_2d45c537a4f93b4689463857c3114dd1',
            'cur_group_id': '6160208745A74BCF_self_2d45c537a4f93b4689463857c3114dd1_0',
            'Hm_lpvt_2af69bc2b378fb58ae04ed2a04257ed1': '1774694158',
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://www.acfun.cn/v/list123/index.htm',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
            # 'cookie': '_did=web_66863889621946DB; lsv_js_player_v2_main=ca85g8; safety_id=AAJGw7hWFc1z7HdvlyHBdXn3; _did=web_66863889621946DB; csrfToken=IScy5otm_kcvlwciqX9_l8Pp; webp_supported=%7B%22lossy%22%3Atrue%2C%22lossless%22%3Atrue%2C%22alpha%22%3Atrue%2C%22animation%22%3Atrue%7D; Hm_lvt_2af69bc2b378fb58ae04ed2a04257ed1=1774624043,1774693996; HMACCOUNT=85B371DDC9AC8F11; cur_req_id=6160208745A74BCF_self_2d45c537a4f93b4689463857c3114dd1; cur_group_id=6160208745A74BCF_self_2d45c537a4f93b4689463857c3114dd1_0; Hm_lpvt_2af69bc2b378fb58ae04ed2a04257ed1=1774694158',
        }
        response = requests.get(url, cookies=cookies, headers=headers)
        text = response.text
        p = re.compile(r'window.videoInfo = (\{.+?});\n')
        json_str = p.findall(text)[0]
        data = json.loads(json_str)
        self.title = data.get('title', self.av)  # 如果取不到则用 av 兜底
        video_data = json.loads(data["currentVideoInfo"]["ksPlayJson"])
        url = video_data['adaptationSet'][0]['representation'][0]['url']
        self.m3u8_url = url

    # 请求m3u8，提取所有ts地址
    def get_ts_urls(self):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://www.acfun.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://www.acfun.cn/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        r = requests.get(self.m3u8_url, headers=headers)
        text = r.text
        lines = text.split('\n')
        urls = [line for line in lines if not line.startswith('#')]
        self.ts_urls = urls

    # 创建缓存文件夹
    def create_cache_dir(self):
        self.dirname = f'D:/PycharmProjects/demo/文件保存/cache_{int(time.time()*1000)}'
        os.makedirs(self.dirname, exist_ok=True)

    # 下载所有的ts文件
    def download_ts(self):
        ts_headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://www.acfun.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://www.acfun.cn/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        urls = self.ts_urls
        txt = ''
        for index, url in enumerate(urls):
            url = url.strip()
            if not url:continue

            url = 'https://ali-safety-video.acfun.cn/mediacloud/acfun/acfun_video/'+ url
            r = requests.get(url, headers=ts_headers)
            with open(f'{self.dirname}/{index}.ts', 'wb') as f:
                f.write(r.content)
                txt += f'file {index}.ts\n'
        with open(f'{self.dirname}/list.txt', 'w') as f:
            f.write(txt)

    # 合并ts
    def merge_ts(self):
        ffmpeg_path = r'E:\ffmpeg-git-full\ffmpeg-2026-03-26-git-fd9f1e9c52-full_build\bin\ffmpeg.exe'
        safe_title = re.sub(r'[\\/*?:"<>|]', '_', self.title)
        output_path = f'D:/PycharmProjects/demo/文件保存/{safe_title}.mp4'
        subprocess.run([
            ffmpeg_path,
            '-f', 'concat',
            '-safe', '0',
            '-i', f'{self.dirname}/list.txt',
            '-c', 'copy',
            output_path,
            '-y',
            '-loglevel', 'error'
        ])

    # 清除缓存文件夹
    def clear_cache_dir(self):
        shutil.rmtree(self.dirname)
        print('缓存目录已删除')

    def run(self,video_id):
        self.av = video_id
        self.get_m3u8_url()
        self.get_ts_urls()
        self.create_cache_dir()
        self.download_ts()
        self.merge_ts()
        self.clear_cache_dir()

if __name__ == '__main__':
    acfun = Acfun()
    # acfun.run('ac48372480')
    # acfun.run('ac48384276')
    acfun.run('ac48384285')

