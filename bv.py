'''

食用说明（一定要看完！！！！！！）：

1. 本程序用来爬取bilibili网站的视频，零基础可放心食用
2. 此程序只支持单个视频爬取，如需批量爬取，请联系作者本人
3. 使用前请下载并安装好ffmpeg，并将其添加到环境变量中，以便调用
4. 使用前请先安装requests库和ffmpeg库(这两个库是第三方库，需要单独安装。其余库均为Python内置库)
5. 使用前，请先在第51行处填入自己B站首页的Cookie

'''
import requests
import re
import ffmpeg
import os
import time


# ===================步骤一：请输入BV号=====================

bv = 'BV1R8411X7Rg'

# =================步骤二：输入下载文件的文件夹====================

path = 'The_bin'               # (注：如果该文件夹位于程序所在的文件夹中，直接输入文件夹名称即可，否则输入文件夹的绝对路径)

# ==================步骤三：选择下载模式=====================

mode = 0

# =======================================================
# 一共有四种模式，即0、1、2、3                               #
# 0：仅下载音频                                            #
# 1：仅下载画面                                            #
# 2：分别下载音频和画面                                     #
# 3：下载视频                                             #
# =======================================================











headers = {
    'Referer': 'https://www.bilibili.com/',
    'Cookie': '',                                       # <------------在此填入你的B站首页Cookie
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

url = 'https://www.bilibili.com/video/' + bv + '/?spm_id_from=333.788.recommend_more_video.0&vd_source=e019291aba8990e4938de7d22ea58de3'
direct = requests.get(url, headers=headers).text
pattern = re.compile('"baseUrl":"(.*?)"')
pattern1 = re.compile('"title":"(.*?)",')
lis = pattern.findall(direct)
lis0 = pattern1.findall(direct)
title = lis0[0].replace(' ', '_')

videoU = lis[0]
audioU = lis[-1]

if mode > 1:

    video = requests.get(videoU, headers=headers).content
    audio = requests.get(audioU, headers=headers).content

    if mode == 3:

        try:
            print(time.ctime(), "模式三开始运行喵~")
            with open(path + '/' + 'audio.mp3', 'wb') as f:
                f.write(audio)
                f.close()
            with open(path + '/' + 'video.mp4', 'wb') as f:
                f.write(video)
                f.close()

            audio = ffmpeg.input(f'{path}/audio.mp3')
            video = ffmpeg.input(f'{path}/video.mp4')
            print(time.ctime(), "正在合并音视频喵~")
            out = ffmpeg.output(video, audio, f'{path}/' + title + '.mp4')
            out.run()

            os.remove(path + '/' + 'audio.mp3')
            os.remove(path + '/' + 'video.mp4')
            print(time.ctime(), '视频下载成功了喵！')

        except:

            print(time.ctime(), '出错了喵QAQ')

    else:

        try:

            print(time.ctime(), '模式二开始运行喵~')
            with open(path + '/' + title + '_audio.mp3', 'wb') as f:
                f.write(audio)
                f.close()
            with open(path + '/' + title + '_video.mp4', 'wb') as f:
                f.write(video)
                f.close()
            print(time.ctime(), '音频和画面下载成功了喵！')

        except:

            print(time.ctime(), '出错了喵QAQ')

else:

    if mode == 1:

        try:

            print(time.ctime(), '模式一开始运行喵~')
            video = requests.get(videoU, headers=headers).content
            with open(path + '/' + title + '_video.mp4', 'wb') as f:
                f.write(video)
                f.close()
            print(time.ctime(), '画面下载成功了喵！')

        except:

            print(time.ctime(), '出错了喵QAQ')

    else:

        try:

            print(time.ctime(), '模式零开始运行喵~')
            audio = requests.get(audioU, headers=headers).content
            with open(path + '/' + title + '_audio.mp3', 'wb') as f:
                f.write(audio)
                f.close()
            print(time.ctime(), '音频下载成功了喵！')

        except:

            print(time.ctime(), '出错了喵QAQ')