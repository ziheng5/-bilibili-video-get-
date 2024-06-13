from PySide6 import QtWidgets
import sys
import requests
import re
import ffmpeg
import os
import time

ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')

class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('小工具食用指南')
        self.resize(500, 400)

        self.second_layout = QtWidgets.QVBoxLayout(self)
        tips1 = QtWidgets.QLabel('a. 本工具可以通过输入BV号，直接获取相应的B站音视频资源喵')
        tips2 = QtWidgets.QLabel('b. 在获取视频资源之前，请务必先输入下载位置喵（填入绝对路径）')
        tips3 = QtWidgets.QLabel('   [例如：C:/Users/21993/anaconda3/envs，视频即下载到envs文件夹中]\n   可以右键想要使用的文件夹，点击复制文件地址，粘贴到框里')
        tips4 = QtWidgets.QLabel('c. 爬取时有四种模式喵：')
        tips5 = QtWidgets.QLabel('   1. 模式一：仅下载音频')
        tips6 = QtWidgets.QLabel('   2. 模式二：仅下载视频画面')
        tips7 = QtWidgets.QLabel('   3. 模式三：分别下载音频和视频画面')
        tips8 = QtWidgets.QLabel('   4. 模式四：下载完整的视频')
        tips9 = QtWidgets.QLabel('d. 做完以上工作，就可以开始获取视频了喵~')

        self.second_layout.addWidget(tips1)
        self.second_layout.addWidget(tips2)
        self.second_layout.addWidget(tips3)
        self.second_layout.addWidget(tips4)
        self.second_layout.addWidget(tips5)
        self.second_layout.addWidget(tips6)
        self.second_layout.addWidget(tips7)
        self.second_layout.addWidget(tips8)
        self.second_layout.addWidget(tips9)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.mode = 5
        self.bv = ''
        self.path = ''

        self.setWindowTitle('小帮手')

        self.resize(500, 400)

        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)

        # 食用指南
        button = QtWidgets.QPushButton('食用指南')
        button.clicked.connect(self.open_new_window)

        # 输入BV号的那一行Layout
        BV_layout = QtWidgets.QHBoxLayout()
        tip_label = QtWidgets.QLabel('请输入BV号：')
        self.put_BV = QtWidgets.QLineEdit()
        self.put_BV.setPlaceholderText('在此输入BV号喵')
        self.search_button = QtWidgets.QPushButton('开始获取')
        BV_layout.addWidget(tip_label)
        BV_layout.addWidget(self.put_BV)
        BV_layout.addWidget(self.search_button)
        self.search_button.clicked.connect(self.start)

        # 输入文件路径的那一行
        path_layout = QtWidgets.QHBoxLayout()
        self.path_tip = QtWidgets.QLabel('请输入下载路径喵：')
        self.put_path = QtWidgets.QLineEdit()
        self.put_path.setPlaceholderText('在此输入下载路径喵')
        path_layout.addWidget(self.path_tip)
        path_layout.addWidget(self.put_path)

        # 模式选择
        mode_layout = QtWidgets.QVBoxLayout()
        self.buttongroup = QtWidgets.QButtonGroup()
        button1 = QtWidgets.QRadioButton('模式1', centralWidget)
        button2 = QtWidgets.QRadioButton('模式2', centralWidget)
        button3 = QtWidgets.QRadioButton('模式3', centralWidget)
        button4 = QtWidgets.QRadioButton('模式4', centralWidget)
        self.buttongroup.addButton(button1, 1)
        self.buttongroup.addButton(button2, 2)
        self.buttongroup.addButton(button3, 3)
        self.buttongroup.addButton(button4, 4)
        mode_layout.addWidget(button1)
        mode_layout.addWidget(button2)
        mode_layout.addWidget(button3)
        mode_layout.addWidget(button4)

        self.buttongroup.buttonClicked.connect(self.choose_mode)




        # 进程窗口
        bottom_layout = QtWidgets.QHBoxLayout()
        self.text_output = QtWidgets.QTextBrowser()
        bottom_layout.addLayout(mode_layout)
        bottom_layout.addWidget(self.text_output)


        # 创建主Layout
        main_layout = QtWidgets.QVBoxLayout(centralWidget)
        main_layout.addWidget(button)
        main_layout.addLayout(path_layout)
        main_layout.addLayout(BV_layout)
        main_layout.addLayout(bottom_layout)




    def open_new_window(self):
        # 实例化一个对话框类
        self.dlg = MyDialog()
        # 显示对话框，代码阻塞在这里，
        # 等待对话框关闭后，才能继续往后执行
        self.dlg.exec()

    def choose_mode(self, item):
        choice = int(item.text()[-1])
        self.mode = choice
        a = time.ctime() + '  ' + '选择了模式' + str(choice) + '喵~'
        self.text_output.append(a)

    def get_path(self):
        path = self.put_path.text()
        self.path = path.replace('"', '')
        self.path = path.replace('\\', '/')
        self.bv = self.put_BV.text()
        # print(self.path)
        # print(self.bv)

    def start(self):

        b = time.ctime() + '  ' + '正在初始化喵~'
        self.text_output.append(b)

        path = self.put_path.text()
        self.path = path.replace('"', '')
        self.path = path.replace('\\', '/')
        self.bv = self.put_BV.text()

        headers = {
            'Referer': 'https://www.bilibili.com/',
            'Cookie': 'buvid3=F2C086D6-980D-4B08-2039-90451B86FC5503334infoc; b_nut=1706971003; CURRENT_FNVAL=4048; _uuid=27EA6B36-B49E-10495-7266-22AEF10B445BA04197infoc; buvid4=AF72FD25-BDBA-85A0-81DA-0ED41CCBC43604473-024020314-rnWmI1GPxhMVnt9%2Fucqn7Pyj8YqnYHfkGc7OH4Iju7OsT2P%2BCb4vmMfNTHqQwYYh; rpdid=0zbfVHh5Qc|16Cmid9l|3wc|3w1Rwh8p; hit-dyn-v2=1; enable_web_push=DISABLE; header_theme_version=CLOSE; DedeUserID=1386461614; DedeUserID__ckMd5=044cac87dfcee9c0; FEED_LIVE_VERSION=V8; CURRENT_QUALITY=64; buvid_fp_plain=undefined; fingerprint=cd288fc41c970be741e38da4c6248870; buvid_fp=cd288fc41c970be741e38da4c6248870; home_feed_column=5; PVID=2; b_lsid=CDDF7293_18FF1A8458D; bmg_af_switch=1; bmg_src_def_domain=i2.hdslb.com; bp_t_offset_1386461614=940200665075941396; browser_resolution=1920-302; SESSDATA=b2e74371%2C1733298294%2C6fa87%2A61CjDz4czyXoBL_KyF_Xo4uYNBdr7CWi_iXAd9Bk0vBfbBlR96Qe8onvgbPc7-tQthIxASVjdZYzMwMGtRYVBTdVNaQmJla05QNU9XcFZRVlNvLU1VRTd4Ui0zWENfcXUxVDBOajZZc05WemNaVV8zdFZpV0NZT2FvanlCck9PaHhpSXFaNDlQekl3IIEC; bili_jct=632ff8691d5cdfdb4fc2d576eac35376; sid=qejryjq2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

        url = 'https://www.bilibili.com/video/' + self.bv + '/?spm_id_from=333.788.recommend_more_video.0&vd_source=e019291aba8990e4938de7d22ea58de3'
        direct = requests.get(url, headers=headers).text
        pattern = re.compile('"baseUrl":"(.*?)"')
        pattern1 = re.compile('"title":"(.*?)",')
        lis = pattern.findall(direct)
        lis0 = pattern1.findall(direct)
        title = lis0[0].replace(' ', '_')

        videoU = lis[0]
        audioU = lis[-1]

        c = time.ctime() + '  ' + '初始化完成喵~'
        self.text_output.append(c)

        if self.mode > 2:

            video = requests.get(videoU, headers=headers).content
            audio = requests.get(audioU, headers=headers).content

            if self.mode == 4:

                try:
                    # print(time.ctime(), "模式四开始运行喵~")
                    d = time.ctime() + '  模式四开始运行，请稍等喵~'
                    self.text_output.append(d)

                    with open(self.path + '/' + 'audio.mp3', 'wb') as f:
                        f.write(audio)
                        f.close()
                    with open(self.path + '/' + 'video.mp4', 'wb') as f:
                        f.write(video)
                        f.close()

                    audio = ffmpeg.input(f'{self.path}/audio.mp3')
                    video = ffmpeg.input(f'{self.path}/video.mp4')
                    print(time.ctime(), "正在合并音视频喵~")
                    e = time.ctime() + "  正在合并音视频，请稍等喵~"
                    self.text_output.append(e)
                    out = ffmpeg.output(video, audio, f'{self.path}/' + title + '.mp4')
                    out.run()

                    # video_clip = VideoFileClip(f'{self.path}/video.mp4')
                    # audio_clip = AudioFileClip(f'{self.path}/audio.mp3')
                    # print(time.ctime(), "正在合并音视频喵~")
                    # e = time.ctime() + "  正在合并音视频，请稍等喵~"
                    # self.text_output.append(e)
                    #
                    # video_clip = video_clip.set_audio(audio_clip)
                    # video_clip.write_videofile(self.path + '/' + title + ".mp4")

                    os.remove(self.path + '/' + 'audio.mp3')
                    os.remove(self.path + '/' + 'video.mp4')

                    # print(time.ctime(), '视频下载成功了喵~')
                    f = time.ctime() + '  视频下载成功了喵~'
                    self.text_output.append(f)

                except:

                    # print(time.ctime(), '出错了喵QAQ')
                    g = time.ctime() + '  出错了喵QAQ'
                    self.text_output.append(g)

            else:

                try:

                    # print(time.ctime(), '模式三开始运行喵~')
                    h = time.ctime() + '  模式三开始运行喵~'
                    self.text_output.append(h)

                    with open(self.path + '/' + title + '_audio.mp3', 'wb') as f:
                        f.write(audio)
                        f.close()
                    with open(self.path + '/' + title + '_video.mp4', 'wb') as f:
                        f.write(video)
                        f.close()
                    # print(time.ctime(), '音频和画面下载成功了喵！')
                    i = time.ctime() + '  音频和画面下载成功了喵！'
                    self.text_output.append(i)

                except:

                    # print(time.ctime(), '出错了喵QAQ')
                    j = time.ctime() + '  出错了喵QAQ'
                    self.text_output.append(j)

        else:

            if self.mode == 2:

                try:

                    # print(time.ctime(), '模式二开始运行喵~')
                    k = time.ctime() + '  模式二开始运行喵~'
                    self.text_output.append(k)

                    video = requests.get(videoU, headers=headers).content
                    with open(self.path + '/' + title + '_video.mp4', 'wb') as f:
                        f.write(video)
                        f.close()
                    # print(time.ctime(), '画面下载成功了喵！')
                    l = time.ctime() + '  画面下载成功了喵！'
                    self.text_output.append(l)

                except:

                    # print(time.ctime(), '出错了喵QAQ')
                    m = time.ctime() + '  出错了喵QAQ'
                    self.text_output.append(m)

            elif self.mode == 1:

                try:

                    # print(time.ctime(), '模式一开始运行喵~')
                    n = time.ctime() + '  模式一开始运行喵~'
                    self.text_output.append(n)

                    audio = requests.get(audioU, headers=headers).content
                    with open(self.path + '/' + title + '_audio.mp3', 'wb') as f:
                        f.write(audio)
                        f.close()
                    # print(time.ctime(), '音频下载成功了喵！')
                    o = time.ctime() + '  音频下载成功了喵！'
                    self.text_output.append(o)

                except:

                    # print(time.ctime(), '出错了喵QAQ')
                    p = time.ctime() + '  出错了喵QAQ'
                    self.text_output.append(p)

            else:
                # print('请选择模式喵！')
                q = '请选择模式喵！'
                self.text_output.append(q)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()