import requests
from os import walk
import os
import time
import json
from datetime import datetime


publicAddr = "http://161.202.197.249/"
localAddr = "http://192.168.1.120/"

LSTORE = {
    "last_ts_time": 0,
    "last_m3u8_time": 0,
    "pending_ts_time": '',
    "last_file_upload": ''
}
CAM_ID = None
HOST = None
PENDING_LIST = []
CONFIG_FILE = 'config.json'



def init():
    global CAM_ID, HOST
    try:
        f = open(CONFIG_FILE, "rt")
        ctx = f.read()

        jObj = json.loads(ctx)

        CAM_ID = jObj['cam_id']
        HOST = jObj['host']
        f.close()
    except Exception as e:
        print(e)
        CAM_ID = None
        HOST = None
    print(CAM_ID, HOST)

def uploadFile(filePath):
    now = datetime.now()
    current_time = now.strftime("[%Y-%m-%d %H:%M:%S] : ")
    print(current_time, "upload file ", filePath)
    try:
        files = {'file': open(filePath, 'rb')}
        send_data = {"cam_id": CAM_ID}
        print(send_data)
        res = requests.post(HOST + "api/upload-to-cache", files=files,data = send_data, verify= False)
    except Exception as e:
        print(e)
        return False
    now = datetime.now()
    current_time = now.strftime("[%Y-%m-%d %H:%M:%S] : ")
    print(current_time, res.status_code, res.text)
    if(res.status_code == 200):
        return True
    else:
        return False


def checkNewFileTs():
    now = datetime.now()
    current_time = now.strftime("[%Y-%m-%d %H:%M:%S] : ")
    listFile = []
    lastFileTs = 0
    #first get list file and file last modifile timestamp
    for (dirpath, dirnames, filenames) in walk(os.getcwd()):
        for filename in filenames:
            if filename.endswith('ts'):
                filePath = os.path.join(dirpath, filename)
                fileLastT = int(os.path.getmtime(filePath))
                if lastFileTs < fileLastT:
                    lastFileTs = fileLastT
                    LSTORE["pending_ts_time"] = fileLastT

                listFile.append((filePath, fileLastT,))
        break
    listFile = sorted(listFile, key= lambda m_tupe: m_tupe[1])
    if len(listFile) == 0:
        return None

    print(listFile[-1][0], os.path.getsize(listFile[-1][0]))

    now = datetime.now()
    current_time = now.strftime("[%Y-%m-%d %H:%M:%S] : ")
    #check if file not upload to server, upload it
    for (file, ltime) in listFile:
        if ltime > LSTORE['last_ts_time'] and ltime < LSTORE['pending_ts_time']:
            isUploaded = uploadFile(file)
            if isUploaded:
                LSTORE['last_ts_time'] = ltime

def handleM3u8(filePath):
    listFileName = []
    fileName = ""
    try:
        f = open(os.path.join(os.getcwd(), 'superindex.m3u8'))
        lines = f.readlines()
        for line in lines:
            line = line.rstrip().rstrip('\n')
            if line.endswith("ts"):
                fileName = line.split('/')[-1]
                listFileName.append(fileName)

    except Exception as e:
        print(e)

    for fileName in listFileName:
        if fileName != "":
            print('File name: ', fileName)
            filePath = os.path.join(os.getcwd(), fileName)
            if LSTORE['last_file_upload'] != filePath:
                isUploaded = uploadFile(filePath)
                if isUploaded:
                    LSTORE['last_file_upload'] = filePath

def checkFileM3u8():
    filePath = os.path.join(os.getcwd(), 'superindex.m3u8')
    lastChange = 0
    try:
        lastChange =  os.path.getmtime(filePath)
    except Exception as e:
        print(e)

    if lastChange > LSTORE['last_m3u8_time']:
        handleM3u8(filePath)
        isUploaded = uploadFile(filePath)
        if isUploaded:
            LSTORE['last_m3u8_time'] = lastChange

def runmain():
    checkNewFileTs()
    while True:
        print("Start loop")
        checkFileM3u8()
        #checkNewFileTs()
        time.sleep(1)
        print("Emd loop")

if __name__ == '__main__':
    #first read config
    init()
    print(CAM_ID, HOST)
    if CAM_ID is None or HOST is None:
        print("Error no config found")
        exit(0)
    runmain()


