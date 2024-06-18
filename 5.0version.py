from PySide6 import QtWidgets, QtGui
import sys
import requests
import re
import ffmpeg
import os
import time
from qt_material import apply_stylesheet

ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')


class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('食用指南')
        self.resize(500, 400)
        self.setWindowOpacity(0.9)

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
        # tips10 = QtWidgets.QLabel('DecisionError: You haven\'t read enough books.')
        # tips11 = QtWidgets.QLabel('DirectionError: Something went wrong on the way you\'ve chosen.')
        tips1.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips2.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips3.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips4.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips5.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips6.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips7.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips8.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips9.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')

        self.second_layout.addWidget(tips1)
        self.second_layout.addWidget(tips2)
        self.second_layout.addWidget(tips3)
        self.second_layout.addWidget(tips4)
        self.second_layout.addWidget(tips5)
        self.second_layout.addWidget(tips6)
        self.second_layout.addWidget(tips7)
        self.second_layout.addWidget(tips8)
        self.second_layout.addWidget(tips9)
        # self.second_layout.addWidget(tips10)
        # self.second_layout.addWidget(tips11)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.mode = 5
        self.bv = ''
        self.path = ''
        self.window().setStyleSheet(u"color:white;")
        self.setWindowTitle('小帮手')
        # palette = QPalette()
        # palette.setColor(QPalette.Window, QColor(0, 0, 0))
        # self.setPalette(palette)
        self.resize(500, 400)

        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)

        # 食用指南
        button = QtWidgets.QPushButton('食用指南')
        button.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; color: #76EEC6;')
        button.clicked.connect(self.open_new_window)

        # 输入BV号的那一行Layout
        BV_layout = QtWidgets.QHBoxLayout()
        tip_label = QtWidgets.QLabel('请输入BV号：')
        tip_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.put_BV = QtWidgets.QLineEdit()
        self.put_BV.setPlaceholderText('在此输入BV号喵')
        self.put_BV.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.search_button = QtWidgets.QPushButton('开始获取')
        self.search_button.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; color: #76EEC6;')
        BV_layout.addWidget(tip_label)
        BV_layout.addWidget(self.put_BV)
        BV_layout.addWidget(self.search_button)
        self.search_button.clicked.connect(self.start)
        tip_label.setStyleSheet("""
                        QLabel {
                            font-family: Microsoft Yahei;
                            font-size: 10pt;
                            font-weight: bold;
                        }
                    """)


        # 输入文件路径的那一行
        path_layout = QtWidgets.QHBoxLayout()
        self.path_tip = QtWidgets.QLabel('请输入下载路径：')
        self.path_tip.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.put_path = QtWidgets.QLineEdit()
        self.put_path.setPlaceholderText('在此输入下载路径喵')
        self.put_path.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        path_layout.addWidget(self.path_tip)
        path_layout.addWidget(self.put_path)



        # 模式选择
        mode_layout = QtWidgets.QVBoxLayout()
        self.buttongroup = QtWidgets.QButtonGroup()
        button1 = QtWidgets.QRadioButton('模式1', centralWidget)
        button1.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        button2 = QtWidgets.QRadioButton('模式2', centralWidget)
        button2.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        button3 = QtWidgets.QRadioButton('模式3', centralWidget)
        button3.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        button4 = QtWidgets.QRadioButton('模式4', centralWidget)
        button4.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.buttongroup.addButton(button1, 1)
        self.buttongroup.addButton(button2, 2)
        self.buttongroup.addButton(button3, 3)
        self.buttongroup.addButton(button4, 4)
        mode_layout.addWidget(button1)
        mode_layout.addWidget(button2)
        mode_layout.addWidget(button3)
        mode_layout.addWidget(button4)

        self.buttongroup.buttonClicked.connect(self.choose_mode)




        # 进程窗口与进度条
        process_layout = QtWidgets.QVBoxLayout()
        bottom_layout = QtWidgets.QHBoxLayout()

        self.text_output = QtWidgets.QTextBrowser()
        self.process = QtWidgets.QProgressBar()
        self.process.setRange(0, 4)
        process_layout.addWidget(self.text_output)
        process_layout.addWidget(self.process)
        self.process.setStyleSheet(u"QProgressBar::chunk\n"
                                    "{\n"
                                    "border-radius:11px;\n"
                                    # "background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 #01FAFF,stop:1  #26B4FF);\n"
                                    "background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 #76EEC6,stop:1  #76EEC6);\n"
                                    "}\n"
                                    "QProgressBar#progressBar\n"
                                    "{\n"
                                    "height:22px;\n"
                                    "text-align:center;/*\u6587\u672c\u4f4d\u7f6e*/\n"
                                    "font-size:14px;\n"
                                    "color:white;\n"
                                    "border-radius:11px;\n"
                                    # "background: #1D5573 ;\n"
                                    "background: #000000 ;\n"
                                    "}")


        bottom_layout.addLayout(mode_layout)
        bottom_layout.addLayout(process_layout)


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
        self.process.reset()
        # self.pro = progress_page()
        # self.pro.exec()

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
        self.process.setValue(1)
        time.sleep(1)

        if self.mode > 2:

            video = requests.get(videoU, headers=headers).content
            audio = requests.get(audioU, headers=headers).content

            if self.mode == 4:

                try:
                    # print(time.ctime(), "模式四开始运行喵~")
                    d = time.ctime() + '  模式四开始运行，请稍等喵~'
                    self.process.setValue(2)
                    self.text_output.append(d)
                    time.sleep(1)

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
                    self.process.setValue(3)
                    time.sleep(1)

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
                    self.process.setValue(4)

                except:

                    # print(time.ctime(), '出错了喵QAQ')
                    g = time.ctime() + '  出错了喵QAQ'
                    self.text_output.append(g)

            else:

                try:

                    # print(time.ctime(), '模式三开始运行喵~')
                    h = time.ctime() + '  模式三开始运行喵~'
                    self.text_output.append(h)
                    self.process.setValue(2)
                    time.sleep(1)

                    with open(self.path + '/' + title + '_audio.mp3', 'wb') as f:
                        f.write(audio)
                        f.close()
                    with open(self.path + '/' + title + '_video.mp4', 'wb') as f:
                        f.write(video)
                        f.close()
                    # print(time.ctime(), '音频和画面下载成功了喵！')
                    i = time.ctime() + '  音频和画面下载成功了喵！'
                    self.text_output.append(i)
                    self.process.setValue(4)

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
                    self.process.setValue(2)
                    time.sleep(1)

                    video = requests.get(videoU, headers=headers).content
                    with open(self.path + '/' + title + '_video.mp4', 'wb') as f:
                        f.write(video)
                        f.close()
                    # print(time.ctime(), '画面下载成功了喵！')
                    l = time.ctime() + '  画面下载成功了喵！'
                    self.text_output.append(l)
                    self.process.setValue(4)


                except:

                    # print(time.ctime(), '出错了喵QAQ')
                    m = time.ctime() + '  出错了喵QAQ'
                    self.text_output.append(m)

            elif self.mode == 1:

                try:

                    # print(time.ctime(), '模式一开始运行喵~')
                    n = time.ctime() + '  模式一开始运行喵~'
                    self.text_output.append(n)
                    self.process.setValue(2)
                    time.sleep(1)

                    audio = requests.get(audioU, headers=headers).content
                    with open(self.path + '/' + title + '_audio.mp3', 'wb') as f:
                        f.write(audio)
                        f.close()
                    # print(time.ctime(), '音频下载成功了喵！')
                    o = time.ctime() + '  音频下载成功了喵！'
                    self.text_output.append(o)
                    self.process.setValue(4)

                except:

                    # print(time.ctime(), '出错了喵QAQ')
                    p = time.ctime() + '  出错了喵QAQ'
                    self.text_output.append(p)

            else:
                # print('请选择模式喵！')
                q = '请选择模式喵！'
                self.text_output.append(q)


app = QtWidgets.QApplication(sys.argv)
apply_stylesheet(app, theme='dark_teal.xml')

# ['dark_amber.xml',
#  'dark_blue.xml',
#  'dark_cyan.xml',
#  'dark_lightgreen.xml',
#  'dark_pink.xml',
#  'dark_purple.xml',
#  'dark_red.xml',
#  'dark_teal.xml',
#  'dark_yellow.xml',
#  'light_amber.xml',
#  'light_blue.xml',
#  'light_cyan.xml',
#  'light_cyan_500.xml',
#  'light_lightgreen.xml',
#  'light_pink.xml',
#  'light_purple.xml',
#  'light_red.xml',
#  'light_teal.xml',
#  'light_yellow.xml']

window = MainWindow()
window.show()
app.exec()