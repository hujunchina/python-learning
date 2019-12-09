"""
@time:      2019-12-09 10:03:06
@version:   v1.0
@author：   hujunchina@outlook.com
"""
import requests
import log
import os


class EZAPI(object):
    appKey = None
    appSecret = None
    appToken = None
    log = None

    # 初始化
    def __init__(self, app_key=None, app_secret=None):
        self.log = log.Log()
        if app_key is None:
            self.appKey = "c127ab47d5dc450088b7c9ce8a8aac85"
            self.log.warning("app key is none")
        else:
            self.appKey = app_key
        if app_secret is None:
            self.appSecret = "9316c6d3ece1d67e7eb8b386fb365fb5"
            self.log.warning("app secret is none")
        else:
            self.appSecret = app_secret
        self.log.info("EZAPI started")

    # 请求调用
    def post_request(self, url, params=None):
        return requests.request("POST", url, params=params)

    # 获得token
    def get_token(self):
        params = {'appKey': self.appKey, 'appSecret': self.appSecret}
        url = "https://open.ys7.com/api/lapp/token/get"
        ret = self.post_request(url, params)
        if ret.status_code is not 200:
            self.log.error("request failed with {0}".format(ret.status_code))
            return
        r = ret.json()
        self.appToken = r['data']['accessToken']
        self.log.info("app token is {0}".format(self.appToken))
        return self.appToken

    # 获得相机列表
    def get_camera_list(self, page_start=0, page_size=10):
        params = {'accessToken': self.appToken, 'pageStart':page_start, 'pageSize':page_size}
        url = "https://open.ys7.com/api/lapp/camera/list"
        ret = self.post_request(url, params)
        if ret.status_code is not 200:
            self.log.error("request failed with {0}".format(ret.status_code))
            return
        r = ret.json()
        if r['page']['total'] is 0:
            self.log.error("camera total is 0")
            return
        else:
            return r['data'][0]['deviceSerial']

    # 截图
    def camera_capture(self, device_serial=None, channel_no=1):
        if device_serial is None:
            self.log.error("device serial is none")
            return
        params = {'accessToken': self.appToken, 'deviceSerial': device_serial, 'channelNo': channel_no}
        url = 'https://open.ys7.com/api/lapp/device/capture'
        ret = self.post_request(url, params)
        if ret.status_code is not 200:
            self.log.error("request failed with {0}".format(ret.status_code))
            return
        r = ret.json()
        return r['data']['picUrl']

    # 保存图片
    def get_camera_picture(self, url):
        r = requests.get(url, stream=True)
        if r.status_code is not 200:
            self.log.error("request failed with {0}".format(r.status_code))
            return
        if r.status_code is 200:
            l = len(os.listdir("img"))
            pic = "{0}.jpg".format(l + 1)
            path = os.path.join("img", pic)
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)


if __name__ == '__main__':
    ezapi = EZAPI()
    ezapi.get_token()
    ezapi.get_camera_picture("https://img.ys7.com//group2/M00/74/22/CmGdBVjBVDCAaFNZAAD4cHwdlXA833.jpg")