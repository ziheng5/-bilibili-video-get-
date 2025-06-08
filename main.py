from utils import *


if __name__ == '__main__':
    headers = {
        'Referer': 'https://www.bilibili.com/',
        'Cookie': 'buvid3=F2C086D6-980D-4B08-2039-90451B86FC5503334infoc; b_nut=1706971003; CURRENT_FNVAL=4048; _uuid=27EA6B36-B49E-10495-7266-22AEF10B445BA04197infoc; buvid4=AF72FD25-BDBA-85A0-81DA-0ED41CCBC43604473-024020314-rnWmI1GPxhMVnt9%2Fucqn7Pyj8YqnYHfkGc7OH4Iju7OsT2P%2BCb4vmMfNTHqQwYYh; rpdid=0zbfVHh5Qc|16Cmid9l|3wc|3w1Rwh8p; hit-dyn-v2=1; enable_web_push=DISABLE; header_theme_version=CLOSE; DedeUserID=1386461614; DedeUserID__ckMd5=044cac87dfcee9c0; FEED_LIVE_VERSION=V8; CURRENT_QUALITY=64; buvid_fp_plain=undefined; fingerprint=cd288fc41c970be741e38da4c6248870; buvid_fp=cd288fc41c970be741e38da4c6248870; home_feed_column=5; PVID=2; b_lsid=CDDF7293_18FF1A8458D; bmg_af_switch=1; bmg_src_def_domain=i2.hdslb.com; bp_t_offset_1386461614=940200665075941396; browser_resolution=1920-302; SESSDATA=b2e74371%2C1733298294%2C6fa87%2A61CjDz4czyXoBL_KyF_Xo4uYNBdr7CWi_iXAd9Bk0vBfbBlR96Qe8onvgbPc7-tQthIxASVjdZYzMwMGtRYVBTdVNaQmJla05QNU9XcFZRVlNvLU1VRTd4Ui0zWENfcXUxVDBOajZZc05WemNaVV8zdFZpV0NZT2FvanlCck9PaHhpSXFaNDlQekl3IIEC; bili_jct=632ff8691d5cdfdb4fc2d576eac35376; sid=qejryjq2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')

    window = MainWindow(headers)
    window.show()
    app.exec()