from dataclasses import dataclass
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow, QVBoxLayout
from PySide6.QtCore import Qt, QSize, QRect, QDateTime, QTimer
from PySide6.QtGui import QPainter, QPaintEvent, QIcon, QFont, QMouseEvent, QBrush, QPen, QRegion, QColor
from qt_material import apply_stylesheet
import enum
import random
import sys
import requests
import re
import ffmpeg
import os
import time
import webbrowser
# from moviepy.editor import *

class CustomTitleBar(QtWidgets.QWidget):
    # 标题栏
    def __init__(self, word, parent=None):
        super().__init__(parent)

        self.setFixedHeight(30)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.titleLabel = QtWidgets.QLabel(word)
        self.titleLabel.setStyleSheet("color: white; font-size: 15pt; font-weight: bold;")
        self.minimizeButton = QtWidgets.QPushButton("")
        self.minimizeButton.setFixedSize(30, 30)
        self.minimizeButton.setStyleSheet(
            "QPushButton{border-image:url('./images/min.png');background:#363636;border-radius:10px;}"  # 29c941
            "QPushButton:hover{background:#1ac033;}"
        )
        self.minimizeButton.clicked.connect(self.minimize)

        self.maximizeButton = QtWidgets.QPushButton("")
        self.maximizeButton.setFixedSize(30, 30)
        self.maximizeButton.setStyleSheet(
            "QPushButton{border-image:url('./images/max.png');background:#363636;border-radius:10px;}"
            "QPushButton:hover{background:#ecae27;}"
        )
        self.maximizeButton.clicked.connect(self.maximize_restore)

        self.closeButton = QtWidgets.QPushButton("")
        self.closeButton.setFixedSize(30, 30)
        self.closeButton.setStyleSheet(
            "QPushButton{border-image:url('./images/close.png');background:#363636;border-radius:10px;}"
            "QPushButton:hover{background:#eb4845;}"
        )
        self.closeButton.clicked.connect(self.close)

        layout.addWidget(self.titleLabel)
        layout.addStretch()
        layout.addWidget(self.minimizeButton)
        layout.addWidget(self.maximizeButton)
        layout.addWidget(self.closeButton)

        self.setLayout(layout)
        self.start = None
        self.pressing = False
        self._left_btn_pressed = False

    def minimize(self):
        # 界面最小化
        self.window().showMinimized()

    def maximize_restore(self):
        # 界面最大化
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def close(self):
        # 关闭界面
        self.window().close()

    def mousePressEvent(self, event: QMouseEvent):
        # 光标按下处理
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos()
            self.pressing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        # 光标移动处理
        if self.pressing:
            self.window().move(self.window().pos() + event.globalPos() - self.start)
            self.start = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        # 光标松开处理
        self.pressing = False

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self._left_btn_pressed = True
    #
    #         # 如果支持 QWindow::startSystemMove，就调用
    #         # 先拿到 QWindow 对象
    #         window_handle = self.windowHandle()
    #         if window_handle is not None:
    #             window_handle.startSystemMove()
    #
    #         event.accept()
    #
    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self._left_btn_pressed = False
    #         event.accept()
    #
    # def mouseMoveEvent(self, event):
    #     # 如果不支持 startSystemMove，就回退到手动移动的方式
    #     if self._left_btn_pressed:
    #         # 手动更新位置的逻辑
    #         # 可能需要考虑 Wayland 环境下 globalPos() 不正确的问题
    #         pass
    #     event.accept()


class MyDialog(QtWidgets.QDialog):
    # 食用指南界面
    def __init__(self):
        super().__init__()
        self.setWindowTitle('食用指南')
        self.resize(500, 400)
        self.setWindowOpacity(0.9)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._left_btn_pressed = False

        self.setMinimumSize(QSize(300, 100))

        titleBar = CustomTitleBar('>>食用指南<<', self)

        self.second_layout = QtWidgets.QVBoxLayout(self)
        tips1 = QtWidgets.QLabel('a. 本工具可以通过输入BV号，直接获取相应的B站音视频资源喵')
        tips2 = QtWidgets.QLabel('b. 在获取视频资源之前，请务必先输入下载位置喵（填入绝对路径）')
        tips3 = QtWidgets.QLabel('   【可以右键想要使用的文件夹，点击复制文件地址，粘贴到框里】')
        tips4 = QtWidgets.QLabel('c. 爬取时有四种模式喵：')
        tips5 = QtWidgets.QLabel('   1. 模式一：仅下载音频')
        tips6 = QtWidgets.QLabel('   2. 模式二：仅下载视频画面')
        tips7 = QtWidgets.QLabel('   3. 模式三：分别下载音频和视频画面')
        tips8 = QtWidgets.QLabel('   4. 模式四：下载完整的视频')
        tips9 = QtWidgets.QLabel('d. 做完以上工作，就可以开始获取视频了喵~')
        tips10 = QtWidgets.QLabel('【如需定制软件或小工具可联系作者本人：2199325776（QQ号）】')


        tips1.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips2.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips3.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips4.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips5.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips6.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips7.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips8.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips9.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        tips10.setStyleSheet('font-family: Microsoft Yahei; font-size: 11pt; font-weight: bold')

        do_not_click = QtWidgets.QPushButton('不要点我喵')
        do_not_click.setStyleSheet("QPushButton:hover{background:#136763;}")
        do_not_click.clicked.connect(self.dont_click)
        do_not_click.resize(50, 30)



        self.second_layout.addWidget(titleBar)
        self.second_layout.addWidget(tips1)
        self.second_layout.addWidget(tips2)
        self.second_layout.addWidget(tips3)
        self.second_layout.addWidget(tips4)
        self.second_layout.addWidget(tips5)
        self.second_layout.addWidget(tips6)
        self.second_layout.addWidget(tips7)
        self.second_layout.addWidget(tips8)
        self.second_layout.addWidget(tips9)
        self.second_layout.addWidget(tips10)
        # self.second_layout.addWidget(tips11)

        dont = QtWidgets.QHBoxLayout(self)
        dont.addWidget(do_not_click)

        self.second_layout.addLayout(dont)
        self.second_layout.setContentsMargins(20, 20, 20, 20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the rounded rectangle background
        rect = self.rect()
        # color = QColor(255, 255, 255)  # Set the desired background color
        # painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    #         event.accept()
    #
    # def mouseMoveEvent(self, event):
    #     if event.buttons() & Qt.LeftButton:
    #         self.move(event.globalPosition().toPoint() - self.drag_position)
    #         event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._left_btn_pressed = True

            # 如果支持 QWindow::startSystemMove，就调用
            # 先拿到 QWindow 对象
            window_handle = self.windowHandle()
            if window_handle is not None:
                window_handle.startSystemMove()

            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._left_btn_pressed = False
            event.accept()

    def mouseMoveEvent(self, event):
        # 如果不支持 startSystemMove，就回退到手动移动的方式
        if self._left_btn_pressed:
            # 手动更新位置的逻辑
            # 可能需要考虑 Wayland 环境下 globalPos() 不正确的问题
            pass
        event.accept()


    def dont_click(self):


        play = random.randint(1, 7)

        if play == 6:
            x = random.randint(0, 800)
            y = random.randint(0, 500)
            self.window().move(x, y)

        if play == 5:
            self.anim = QtCore.QPropertyAnimation(self.window(), b'geometry')
            self.anim.setDuration(400)
            x = self.window().x()
            y = self.window().y()
            self.anim.setStartValue(QtCore.QRect(x, y, 500, 400))
            self.anim.setEndValue(QtCore.QRect(x-50, y, 500, 400))
            self.anim.start()

        if play == 4:
            self.anim = QtCore.QPropertyAnimation(self.window(), b'geometry')
            self.anim.setDuration(400)
            x = self.window().x()
            y = self.window().y()
            self.anim.setStartValue(QtCore.QRect(x, y, 500, 400))
            self.anim.setEndValue(QtCore.QRect(x, y+50, 500, 400))
            self.anim.start()

        if play == 3:
            self.anim = QtCore.QPropertyAnimation(self.window(), b'geometry')
            self.anim.setDuration(400)
            x = self.window().x()
            y = self.window().y()
            self.anim.setStartValue(QtCore.QRect(x, y, 500, 400))
            self.anim.setEndValue(QtCore.QRect(x+50, y, 500, 400))
            self.anim.start()

        if play == 2:
            self.anim = QtCore.QPropertyAnimation(self.window(), b'geometry')
            self.anim.setDuration(400)
            x = self.window().x()
            y = self.window().y()
            self.anim.setStartValue(QtCore.QRect(x, y, 500, 400))
            self.anim.setEndValue(QtCore.QRect(x, y-50, 500, 400))
            self.anim.start()

        if play == 1:
            url = "https://www.bilibili.com/video/BV1GJ411x7h7"
            webbrowser.open(url, new=0, autoraise=True)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, headers):
        super().__init__()
        self.headers = headers
        self.mode0 = '爬取单个视频'
        self.mode = 0
        self.bv = ''
        self.path = ''

        # 初始化
        self.window().setStyleSheet(u"color:white; border-radius: 5px")
        self.setWindowTitle('小帮手')
        self.setWindowFlags(Qt.FramelessWindowHint)    # 隐藏原版标题栏
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(450, 500)
        self._left_btn_pressed = False

        title_Bar = CustomTitleBar('小帮手    ฅ^•ω•^ฅ', self)
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)

        # 食用指南
        button = QtWidgets.QPushButton('食 用 指 南 （必 看）')
        button.setStyleSheet("QPushButton:hover{background:#136763;}")
        button.clicked.connect(self.open_new_window)

        # 输入BV号的那一行Layout
        BV_layout = QtWidgets.QHBoxLayout()
        tip_label = QtWidgets.QLabel('请输入BV号：')
        tip_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.put_BV = QtWidgets.QLineEdit()
        self.put_BV.setPlaceholderText('在此输入BV号喵')
        self.put_BV.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; ')
        self.search_button = QtWidgets.QPushButton('开始获取')
        self.search_button.setStyleSheet("QPushButton:hover{background:#136763;}")
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

        # 输入文件路径的那一行的Layout
        path_layout = QtWidgets.QHBoxLayout()
        self.path_tip = QtWidgets.QLabel('请输入下载路径：')
        self.path_tip.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.put_path = QtWidgets.QLineEdit()
        self.put_path.setPlaceholderText('在此输入下载路径喵')
        self.put_path.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        path_layout.addWidget(self.path_tip)
        path_layout.addWidget(self.put_path)



        # 爬取方式选择
        mode_tip = QtWidgets.QLabel('模式选择')
        mode_tip.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        mode_layout = QtWidgets.QVBoxLayout()
        self.button0 = QtWidgets.QComboBox()
        self.button0.addItems(['爬取单个视频', '（施工中）'])
        self.button0.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.button0.currentIndexChanged.connect(self.choose_mode0)

        # 模式选择单选按钮
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
        main_mode = QtWidgets.QVBoxLayout()
        main_mode.addWidget(self.button0)
        main_mode.addLayout(mode_layout)

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
                                    "background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 #76EEC6,stop:1  #76EEC6);\n"
                                    "}\n"
                                    "QProgressBar#progressBar\n"
                                    "{\n"
                                    "height:22px;\n"
                                    "text-align:center;/*\u6587\u672c\u4f4d\u7f6e*/\n"
                                    "font-size:14px;\n"
                                    "color:white;\n"
                                    "border-radius:11px;\n"
                                    "background: #000000 ;\n"
                                    "}")
        bottom_layout.addLayout(main_mode)
        bottom_layout.addLayout(process_layout)
        main_mode.setContentsMargins(0, 0, 10, 0)
        mode_layout.setContentsMargins(10, 0, 0, 0)

        # 创建主Layout
        main_layout = QtWidgets.QVBoxLayout(centralWidget)
        main_layout.addWidget(title_Bar)
        self.block_line = QtWidgets.QLabel('')
        main_layout.addWidget(self.block_line)
        main_layout.addWidget(button)
        main_layout.addLayout(path_layout)
        main_layout.addLayout(BV_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.setContentsMargins(20, 15, 20, 15)

        # 启动动画
        self.anim = QtCore.QPropertyAnimation(self.window(), b'geometry')
        self.anim.setDuration(100)
        x = 550
        y = 200
        self.anim.setStartValue(QtCore.QRect(x, y, 450, 500))
        self.anim.setEndValue(QtCore.QRect(x, y-50, 450, 500))
        self.anim.start()



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the rounded rectangle background
        rect = self.rect()
        color = QColor(255, 255, 255)  # Set the desired background color
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)



    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    #         event.accept()
    #
    # def mouseMoveEvent(self, event):
    #     if event.buttons() & Qt.LeftButton:
    #         self.move(event.globalPosition().toPoint() - self.drag_position)
    #         event.accept()





    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._left_btn_pressed = True

            # 如果支持 QWindow::startSystemMove，就调用
            # 先拿到 QWindow 对象
            window_handle = self.windowHandle()
            if window_handle is not None:
                window_handle.startSystemMove()

            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._left_btn_pressed = False
            event.accept()

    def mouseMoveEvent(self, event):
        # 如果不支持 startSystemMove，就回退到手动移动的方式
        if self._left_btn_pressed:
            # 手动更新位置的逻辑
            # 可能需要考虑 Wayland 环境下 globalPos() 不正确的问题
            pass
        event.accept()

    def open_new_window(self):
        # 实例化一个对话框类

        self.dlg = MyDialog()
        # 显示对话框，代码阻塞在这里，
        # 等待对话框关闭后，才能继续往后执行
        self.dlg.exec()

    def choose_mode0(self):
        mode0 = self.button0.currentText()
        if mode0 == '爬取单个视频':
            w = QDateTime.currentDateTime()
            w = w.toString('yyyy-MM-dd hh:mm:ss dddd')
            w = w + '\n切换模式：爬取单个视频\n'
            self.text_output.append(w)
        elif mode0 == '爬取视频合集':
            w = QDateTime.currentDateTime()
            w = w.toString('yyyy-MM-dd hh:mm:ss dddd')
            w = w + '\n切换模式：爬取视频合集\n'
            self.text_output.append(w)

    def choose_mode(self, item):
        choice = int(item.text()[-1])
        self.mode = choice
        a = QDateTime.currentDateTime()
        a = a.toString('yyyy-MM-dd hh:mm:ss dddd')
        a = a + '\n选择了模式' + str(choice) + '喵~\n'
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

        if self.mode == 0:
            # print('请选择模式喵！')
            q = '请选择模式喵！\n'
            self.text_output.append(q)


        else:
            path = self.put_path.text()
            self.path = path.replace('"', '')
            self.path = path.replace('\\', '/')
            self.bv = self.put_BV.text()

            if self.bv == '':
                self.text_output.append('请输入BV号喵！\n')
                return

            if path == '':
                self.text_output.append('请输入下载路径喵！\n')
                return

            b = QDateTime.currentDateTime()
            b = b.toString('yyyy-MM-dd hh:mm:ss dddd')
            b = b + '\n正在初始化喵~\n'
            self.text_output.append(b)

            headers = self.headers

            url = 'https://www.bilibili.com/video/' + self.bv + '/?spm_id_from=333.788.recommend_more_video.0&vd_source=e019291aba8990e4938de7d22ea58de3'
            direct = requests.get(url, headers=headers).text
            pattern = re.compile('"baseUrl":"(.*?)"')
            pattern1 = re.compile('"title":"(.*?)",')
            lis = pattern.findall(direct)
            lis0 = pattern1.findall(direct)
            title = lis0[0].replace(' ', '_')

            videoU = lis[0]
            audioU = lis[-1]

            c = QDateTime.currentDateTime()
            c = c.toString('yyyy-MM-dd hh:mm:ss dddd')
            c = c + '\n初始化完成喵~\n'
            self.text_output.append(c)
            self.process.setValue(1)
            time.sleep(1)


            if self.mode > 2:

                video = requests.get(videoU, headers=headers).content
                audio = requests.get(audioU, headers=headers).content

                if self.mode == 4:

                    try:
                        # print(time.ctime(), "模式四开始运行喵~")
                        d = QDateTime.currentDateTime()
                        d = d.toString('yyyy-MM-dd hh:mm:ss dddd')
                        d = d + '\n模式四开始运行，请稍等喵~\n'
                        self.process.setValue(2)
                        self.text_output.append(d)
                        time.sleep(1)

                        with open(self.path + '/' + 'audio.mp3', 'wb') as f:
                            f.write(audio)
                            f.close()
                        with open(self.path + '/' + 'video.mp4', 'wb') as f:
                            f.write(video)
                            f.close()
                        print(1)
                        audio = ffmpeg.input(f'{self.path}/audio.mp3')
                        video = ffmpeg.input(f'{self.path}/video.mp4')


                        # print(time.ctime(), "正在合并音视频喵~\n")
                        e = QDateTime.currentDateTime()
                        e = e.toString('yyyy-MM-dd hh:mm:ss dddd')
                        e = e + "\n正在合并音视频，请稍等喵~\n"
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
                        f = QDateTime.currentDateTime()
                        f = f.toString('yyyy-MM-dd hh:mm:ss dddd')
                        f = f + '\n视频下载成功了喵~\n'
                        self.text_output.append(f)
                        self.process.setValue(4)

                    except:

                        # print(time.ctime(), '出错了喵QAQ')
                        g = QDateTime.currentDateTime()
                        g = g.toString('yyyy-MM-dd hh:mm:ss dddd')
                        g = g + '\n出错了喵QAQ\n'
                        self.text_output.append(g)

                else:

                    try:

                        # print(time.ctime(), '模式三开始运行喵~')
                        h = QDateTime.currentDateTime()
                        h = h.toString('yyyy-MM-dd hh:mm:ss ')
                        h = h + '\n模式三开始运行喵~\n'
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
                        i = QDateTime.currentDateTime()
                        i = i.toString('yyyy-MM-dd hh:mm:ss dddd')
                        i = i + '\n音频和画面下载成功了喵！\n'
                        self.text_output.append(i)
                        self.process.setValue(4)

                    except:

                        # print(time.ctime(), '出错了喵QAQ')
                        j = QDateTime.currentDateTime()
                        j = j.toString('yyyy-MM-dd hh:mm:ss dddd')
                        j = j + '\n出错了喵QAQ\n'
                        self.text_output.append(j)

            else:

                if self.mode == 2:

                    try:

                        # print(time.ctime(), '模式二开始运行喵~')
                        k = QDateTime.currentDateTime()
                        k = k.toString('yyyy-MM-dd hh:mm:ss dddd')
                        k = k + '\n模式二开始运行喵~\n'
                        self.text_output.append(k)
                        self.process.setValue(2)
                        time.sleep(1)

                        video = requests.get(videoU, headers=headers).content
                        with open(self.path + '/' + title + '_video.mp4', 'wb') as f:
                            f.write(video)
                            f.close()
                        # print(time.ctime(), '画面下载成功了喵！')
                        l = QDateTime.currentDateTime()
                        l = l.toString('yyyy-MM-dd hh:mm:ss dddd')
                        l = l + '\n画面下载成功了喵！\n'
                        self.text_output.append(l)
                        self.process.setValue(4)


                    except:

                        # print(time.ctime(), '出错了喵QAQ')
                        m = QDateTime.currentDateTime()
                        m = m.toString('yyyy-MM-dd hh:mm:ss dddd')
                        m = m + '\n出错了喵QAQ\n'
                        self.text_output.append(m)

                elif self.mode == 1:

                    try:

                        # print(time.ctime(), '模式一开始运行喵~')
                        n = QDateTime.currentDateTime()
                        n = n.toString('yyyy-MM-dd hh:mm:ss dddd')
                        n = n + '\n模式一开始运行喵~\n'
                        self.text_output.append(n)
                        self.process.setValue(2)
                        time.sleep(1)

                        audio = requests.get(audioU, headers=headers).content
                        with open(self.path + '/' + title + '_audio.mp3', 'wb') as f:
                            f.write(audio)
                            f.close()
                        # print(time.ctime(), '音频下载成功了喵！')
                        o = QDateTime.currentDateTime()
                        o = o.toString('yyyy-MM-dd hh:mm:ss dddd')
                        o = o + '\n音频下载成功了喵！\n'
                        self.text_output.append(o)
                        self.process.setValue(4)

                    except:

                        # print(time.ctime(), '出错了喵QAQ')
                        p = QDateTime.currentDateTime()
                        p = p.toString('yyyy-MM-dd hh:mm:ss dddd')
                        p = p + '\n出错了喵QAQ\n'
                        self.text_output.append(p)


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     apply_stylesheet(app, theme='dark_teal.xml')
#
#     # ['dark_amber.xml',
#     #  'dark_blue.xml',
#     #  'dark_cyan.xml',
#     #  'dark_lightgreen.xml',
#     #  'dark_pink.xml',
#     #  'dark_purple.xml',
#     #  'dark_red.xml',
#     #  'dark_teal.xml',
#     #  'dark_yellow.xml',
#     #  'light_amber.xml',
#     #  'light_blue.xml',
#     #  'light_cyan.xml',
#     #  'light_cyan_500.xml',
#     #  'light_lightgreen.xml',
#     #  'light_pink.xml',
#     #  'light_purple.xml',
#     #  'light_red.xml',
#     #  'light_teal.xml',
#     #  'light_yellow.xml']
#
#     window = MainWindow()
#     window.show()
#     app.exec()