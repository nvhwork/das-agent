'''
Use http POST request to push file to server
Author: ThangNX - thangnx97@gmail.com
'''


import requests
from os.path import join, getmtime
import threading
from time import sleep
from datetime import datetime
import logging

class HlsPusher:
    def __init__(self, root_path, stream_id, rtsp_uri=None, push_token=None, push_uri=None, log=logging):
        self.is_run = False
        self.gst_hls_thread = None
        self.stream_id = stream_id
        self.rtsp_uri = rtsp_uri
        self.push_token = push_token
        self.push_uri = push_uri
        self.root_path = root_path
        self.last_m3u8_time = 0
        self.listFilePushed = []
        self.log = log

    def uploadFile(self, filePath):
        self.log.info("upload file " + filePath)
        try:
            files = {'file': open(filePath, 'rb')}
            send_data = {"stream_id": self.stream_id}
            print(str(send_data) + '\n')
            res = requests.post(self.push_uri, files=files, data=send_data, verify=False)
        except Exception as e:
            self.log.error(e)
            return False

        self.log.info("upload " + filePath + "code: " + str(res.status_code))
        if(res.status_code == 200):
            return True
        else:
            self.log.error("push file " + filePath + " error")
            print(res)
            # print(res.content)
            return False

        
    def handleM3u8(self, filePath):
        listFileName = []
        fileName = ""
        try:
            f = open(filePath, 'rt')
            lines = f.readlines()
            for line in lines:
                line = line.rstrip().rstrip('\n')
                splitLine  = line.split('/')
                if line.endswith("ts"):
                    if (len(splitLine) > 0):
                        fileName = line.split('/')[-1]
                    else:
                        fileName = line
                    print(fileName)
                    listFileName.append(fileName)

        except Exception as e:
            self.log.error(e)
        self.log.debug(listFileName)
        for fileName in listFileName:
            if fileName not in self.listFilePushed:
                ret = self.uploadFile(join(self.root_path, fileName))
                if ret:
                    self.listFilePushed.append(fileName)

        # Remove oll pushed file
        # while len(listFileName) >0 and len(self.listFilePushed) >0 and self.listFilePushed[0] not in listFileName:
        #     self.listFilePushed.pop(0)
            

    def checkFileM3u8(self):
        filePath = join(self.root_path, 'index.m3u8')
        lastChange = 0
        try:
            lastChange = getmtime(filePath)
        except Exception as e:
            self.log.error(e)

        if lastChange > self.last_m3u8_time:
            self.handleM3u8(filePath)
            isUploaded = self.uploadFile(filePath)
            if isUploaded:
                self.last_m3u8_time = lastChange

    def checkInfo(self):
        if self.stream_id is None or self.root_path is None or self.push_token is None or self.push_uri is None:
            return False
        return True


    def run_pusher(self):
        if self.checkInfo():
            self.checkFileM3u8()

    def run(self):
        self.is_run = True

        # Check pushing process every 3 seconds
        while self.is_run:
            self.log.debug("running")
            self.run_pusher()
            sleep(3)

        self.last_m3u8_time = 0
        self.gst_hls_thread = None

    def stop(self):
        self.log.info("stop pushing")
        self.is_run = False

    def runAsync(self):
        self.gst_hls_thread = threading.Thread(target=self.run)
        self.gst_hls_thread.start()
        return True


'''
For test
'''
def main():
    pusher = HlsPusher("/home/map/demoHls/hls", "data", push_token = "", push_uri = "https://hls.dasvision.vn/api/upload-to-cache")
    pusher.runAsync()

    while True:
        print("Input: ")
        inp = input()
        if inp == 'q':
            pusher.stop()
        sleep(5)

'''
for test
'''

if __name__ == "__main__":
    main()







