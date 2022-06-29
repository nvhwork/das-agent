'''
DAS-AGENT version 0.1
Use for Edge device as: Jetson Nano, Xavier, Protect
Author: ThangNX - thangnx97@gmail.com
'''

import os
import subprocess
from time import sleep
from default import RECONNECT_TIME
import logging
from hlsPushControl import HlsPushControl
from requestControl import RequestControl
from stream import Stream
import sys
import json
import threading
from version import __version
from mylog import setupLog
from threading import Lock
import pymysql
import signal

MAX_TRY = 5

log = logging
room_sid = ''
onvifScanner = None
reqCtl = None
token = None
needLogin = True
connectLock = Lock()


'''
Create socketio client
'''
# # standard Python

isConnect = False

scanLook = Lock()
infoOnvifLock = Lock()
scan_onvif_num = 0
get_info_onvif_num = 0
MAX_REQ = 2
hlsCtl = None


def on_play_hls(data):
    try:
        jobj = json.loads(data)
        stream_id = jobj['stream_id']
        ret = False
        if hlsCtl is not None:
            if hlsCtl.checkCamInList(stream_id) is not None:
                log.debug('Cam id ' + str(stream_id))
                ret = hlsCtl.startPushByCamId(stream_id)
        else:
            log.error('Start false')
    except Exception as e:
        log.error(e)
    #run hls pusher


def welcome():
    print('DAS-Agent version: ', __version)
    print('-' *50)
    
def parseConfig(hlsPushControl):
    listStreams = []
    db = pymysql.connect(
        host = 'localhost',
        user = 'hoangnv',
        password = 'bkcs2022',
        database = 'transcoding'
    )
    cursor = db.cursor()
    sql = "SELECT stream_id, stream_bitrate, stream_width, stream_height, camera_name, camera_url, camera_codec, stream_codec " \
        + "FROM streams JOIN cameras ON cameras.camera_name = streams.stream_input_camera"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print("Error: Unable to fetch data")
    db.close()

    for row in results:
        stream = Stream()
        stream.set_streamId(row[0])
        stream.set_bitrate(row[1])

        resolution = str(row[2]) + 'x' + str(row[3])
        stream.set_resolution(resolution)
        stream.set_path('/' + row[4] + '/' + resolution)
        stream.set_url(row[5])
        stream.set_inputCodec(row[6])
        stream.set_outputCodec(row[7])
        listStreams.append(stream)

    return hlsPushControl.updateConfig(listStreams)

#Check all puser
def pollHls(log, hlsCtl):
    while True and hlsCtl is not None:
        sleep(60)
        log.info('Poll running')
        hlsCtl.poll()
    log.info('End of poll task')
 
def run_poll_async(log, hlsCtl):
    poll_thread = threading.Thread(target=pollHls, args =(log, hlsCtl))
    poll_thread.start()

def loginAndGetConfigUtilSuccess():
    global reqCtl, token, hlsCtl
    
    parseConfig(hlsCtl)

    ret = True
    return ret

def run(isFile, logLevel):
    global hlsCtl, log, onvifScanner, reqCtl
    welcome()

    log = setupLog(isFile, logLevel)
    # onvifScanner = OnvifScanner(log)

    reqCtl = RequestControl(log)
    hlsCtl = HlsPushControl(log)
    streamIds = []

    print('Log in to CMS...')
    ret = loginAndGetConfigUtilSuccess()

    # run_poll_async(log, hlsCtl)

    db = pymysql.connect(
        host = 'localhost',
        user = 'hoangnv',
        password = 'bkcs2022',
        database = 'transcoding'
    )
    cursor = db.cursor()
    sql = "SELECT stream_input_camera FROM streams GROUP BY stream_input_camera"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            streamIds.append(row[0])
    except:
        print("Error: Unable to fetch data")
    db.close()

    hlsCtl.startWatchApp()

    for i in streamIds:
        print('\tCamera name: ' + i)
        hlsCtl.startPushByCamId(i)

    while True:
        sleep(RECONNECT_TIME)

    print('Bye.')

# Handle program when terminating
def sigterm_handler(_signo, _stack_frame):
    print("Program ended!")
    subprocess.run(['rm', '-r', '/home/e-ai/transcoding/cms/public/hls'])
    os._exit(0)

def main():
    isFile = False
    logLevel = 'error'
    for arg in sys.argv:
        if arg == '-v':
            logLevel = 'info'
        if arg == '-V':
            logLevel = 'debug'
        if arg == '-f':
            isFile = True
    run(isFile, logLevel)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sigterm_handler)

try:
    main()

finally:
    pass