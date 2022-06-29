'''
Hls push control class use for stored stream information, update it, push stream's .ts file for hls streamming
Author: ThangNX - thangnx97@gmail.com
'''

import array
from default import DEFAULT_TMP, PUSH_FILE_HLS_PATH, CMS_SERVER
from os.path import join
from fileHelper import isFolder, createFolder, writeFileConfig, cleatTsM3u8FileInFolder, clearInFolder
from hlsPusher import HlsPusher
from time import sleep
from stream import Stream
import logging
from datetime import datetime
from threading import Lock, Thread
import subprocess
import shlex

STS_OK = 1 #APP running
STS_FOLDER_CAM = 2 #Can not create stream folder
STS_APP = 3 #App not run
STS_FOLDER_TMP = 4 #Can not create TMP folder
STS_STREAM = 5 #Can not get stream to provide hls


class GstApp:
    def __init__(self, stream_id ):
        self.stream_id = stream_id

    def get_streamId(self):
        return self.stream_id


class HlsPushControl:
    def __init__(self, log=logging):
        self.streams = []
        self.hlsThread = {}
        self.gstAppList = []
        self.log = log
        self.status = {}
        self.threadLock = Lock()
        self.watchAppThread = None
        self.threadAppRun = False
        self.prepareTmpDir()

    def load_config(self):
        pass

    def get_hlsThread(self):
        return self.hlsThread
        
    def addStream(self, stream: Stream):
        streamInList = self.checkStreamInList(stream.get_streamId())
        if streamInList == False:
            self.streams.append(stream)
            sorted(self.streams, key= lambda x: x.get_streamId())
        else:
            streamInList.set_url(stream.get_url())
    
    def findAppById(self, streamId):
        for app in self.gstAppList:
            if app.stream_id == streamId:
                return app
        return None
    '''
    Remove stream:
    form list streams
    app from gstAppList
    from status dict
    '''
    def removeStream(self, stream: Stream):
        return True

    def removeById(self, id):
        return True


    def checkStreamInList(self, streamId):
        for stream in self.streams:
            # if stream.get_streamId() > streamId:
            #     return False
            if stream.get_streamId() == streamId:
                # return stream
                return True
        return False

    def showListCam(self):
        print('[')
        for stream in self.streams:
            stream.show()
        print(']')

    '''
    After add stream or modify stream
    Create tmp folder for stream and it's hls script, and app
    '''
    def createTmpFolder(self, stream: Stream):
        status = STS_FOLDER_TMP
        sts = status
        ret = True
        if not isFolder(DEFAULT_TMP):
            ret = createFolder(DEFAULT_TMP)
        if ret:
            dirPath = DEFAULT_TMP + stream.get_path()
            print('dirpath: ', dirPath)

            if not isFolder(dirPath):
                ret = createFolder(dirPath)
            if not ret:
                self.status[stream.get_streamId()] = STS_FOLDER_CAM
            else:
                if stream.get_url() is not None:
                    depay = ' ! '
                    enc = ' ! '
                    parser = ' ! '
                    res = str(stream.get_resolution()).split('x')

                    if ('H.265' in stream.get_inputCodec()):
                        depay += 'rtph265depay'
                    elif ('H.264' in stream.get_inputCodec()):
                        depay += 'rtph264depay'

                    if ('H.265' in stream.get_outputCodec()):
                        enc += 'nvv4l2h265enc bitrate=' + str(stream.get_bitrate())
                        parser += 'h265parse'
                    else:
                        enc += 'nvv4l2h264enc disable-cabac=true bitrate=' + str(stream.get_bitrate())
                        parser += 'h264parse'

                    cmd = "#!/bin/sh\n" \
                            + "cd "+ dirPath + "\n" \
                            + "gst-launch-1.0 rtspsrc location=" + stream.get_url() + depay \
                            + " ! nvv4l2decoder ! n.sink_0 nvstreammux name=n batch-size=1 width=" + res[0] \
                            + " height=" + res[1] + enc \
                            + " maxperf-enable=true idrinterval=60 " + parser \
                            + " ! mpegtsmux ! hlssink playlist-location=index.m3u8 playlist-length=3 " \
                            + " max-files=5 target-duration=3 --gst-debug=3 >loggst.txt 2>&1 &\n"
                    ret =  writeFileConfig(join(dirPath, 'runGst.sh'), cmd)
                    if ret:
                        subprocess.call(shlex.split(join(dirPath, 'runGst.sh')))
                        app = GstApp(stream.get_streamId())
                        self.gstAppList.append(app)
                        sts = STS_OK
                    else:
                        sts = STS_APP # APP NOT CREATE
                        self.log.error("Cannot create app")
                else:
                    sts = STS_STREAM #COULD NOT GET STREAM
                    self.log.error("Stream not found")
        self.status[stream.get_streamId()] = sts
        return ret

    '''
    After first load
    Prepare tmp folder for stream
    '''
    def prepareTmpDir(self):
        '''
        Check TMP folder exits. If not, create it
        Check all stream folder exits, if not create it
        '''
        ret = True
        if not isFolder(DEFAULT_TMP):
            ret = createFolder(DEFAULT_TMP)
        # else:
            
            #Clear in tmp dir
            # clearInFolder(DEFAULT_TMP)
        if ret:
            for stream in self.streams:
                self.createTmpFolder(stream)

    '''
    Generate master playlist
    for each camera
    '''
    def generateMasterPlaylist(self, camid, listStreams):
        # TODO
        tag = '#EXTM3U\n#EXT-X-VERSION:6\n'
        for stream in listStreams:
            tag += '#EXT-X-STREAM-INF:BANDWIDTH=' + str(stream.get_bitrate()) \
                    + ',RESOLUTION=' + stream.get_resolution() + '\n'\
                    + stream.get_resolution() + '/index.m3u8\n\n' 
        dirPath = join(DEFAULT_TMP, camid, 'master.m3u8')
        ret = writeFileConfig(dirPath, tag)
        if ret:
            self.log.info('\nWrite new master playlist: ' + dirPath + '\n')
        else:
            self.log.error('\nError writing master playlist: ' + dirPath + '\n')

    def startPushByStream(self, stream: Stream):
        pusher = HlsPusher(stream.tmpFolder, stream.get_streamId(), "", "", CMS_SERVER + PUSH_FILE_HLS_PATH)
        self.hlsThread[stream.get_streamId()] = {"pusher": pusher, "last_event": datetime.now(), "running": True}
        return pusher.runAsync()

    def startPushByCamId(self, camid):
        needNew = True
        ret = False

        # Get stream with the camera
        listStreamsByCam = []
        for stream in self.streams:
            if (camid in stream.get_streamId()):
                listStreamsByCam.append(stream)
        if (len(listStreamsByCam) <= 0):
            self.log.error("Camera " + camid + " has no transcoding streams yet")
            return False
        
        # self.threadLock.acquire()
        # for stream in listStreamsByCam:
        #     if stream.get_streamId() in self.hlsThread:
        #         thread = self.hlsThread[stream.get_streamId()]
        #         if "running" in thread and "pusher" in thread:
        #             if not thread["running"]:
        #                 thread['last_event'] = datetime.now()
        #                 thread['pusher'].runAsync()
        #                 thread['running'] = True
        #                 ret = True
        #             else:
        #                 ret = True
        #             needNew = False
        #         else:
        #             needNew = True

        #     if needNew:
        #         self.log.debug("Run as new camera")
        #         # Check stream.get_streamId() in list
        #         streamExists = self.checkStreamInList(stream.get_streamId())
        #         if not streamExists:
        #             self.log.error("Stream " + stream.get_streamId() + " is not in list")
        #             self.threadLock.release()
        #             return False
        #         else:
        #             ret = self.startPushByStream(stream)

        self.generateMasterPlaylist(camid=camid, listStreams=listStreamsByCam)
        # self.threadLock.release()
        return ret

    def stopPushByCamId(self, streamId):
        self.threadLock.acquire()

        if streamId in self.hlsThread:
            self.log.info("Stop hls push: " + str(streamId))
            self.hlsThread[streamId]['pusher'].stop()
            self.hlsThread[streamId]['running'] = False
        else:
            self.log.info("Cam " + str(streamId) + " not in running")

        self.threadLock.release()

    #Stop and remove
    def stopAppByCamId(self, streamId):
        appCam = self.findAppById(streamId)
        if appCam is not None:
            self.gstAppList.remove(appCam)
            

    def updateConfig(self, config):
        liststreamId = [stream.get_streamId() for stream in config]
        #Remove deleted stream
        for stream in self.streams:
            if stream.get_streamId() not in liststreamId:
                self.removeById(stream.get_streamId())
                self.stopAppByCamId(stream.get_streamId())
        
        #Update new stream config
        for newStream in config:
            oldStream = self.checkStreamInList(newStream.get_streamId())
            if oldStream == False:
                self.addStream(newStream)
                self.createTmpFolder(newStream)
            else:
                #Modify stream
                isChange = False
                if newStream.get_url() != oldStream.get_url():
                    isChange = True
                if isChange:
                    self.stopAppByCamId(newStream.get_streamId())
                    self.stopPushByCamId(newStream.get_streamId())
                    oldStream.set_url(newStream.get_url())
                    self.createTmpFolder(oldStream)
        # self.showListCam()
        return True


    '''
    Get application status
    '''
    def getStatus(self):
        return [{'stream_id':k, 'status': v} for k, v in self.status.items()]
        # return self.status.copy()
    
    def startAppThread(self):
        self.log.debug("Start watching app thread")
        if self.threadAppRun:
            return
        self.threadAppRun = True
        while self.threadAppRun:
            for app in self.gstAppList:
                    self.log.debug("App: " + str(app.stream_id) + " still running")
                    self.status[app.stream_id] = STS_OK
            sleep(10)

    #Run 1 time
    def startWatchApp(self):
        if self.watchAppThread is not None:
            self.log.info("Watching app thread already run")
            return
        self.watchAppThread = Thread(target=self.startAppThread)
        self.watchAppThread.start()
        
    '''
    Polling hls pusher
    Check if client do not require hls, then stop pushing
    '''
    def poll(self):
        hlsThreads = self.get_hlsThread()
        now = datetime.now()
        self.threadLock.acquire()
        for streamId in hlsThreads:
            try:
                thread = hlsThreads[streamId]
                diff = now - thread['last_event']
                if thread['running'] and diff.total_seconds() > 360: #2xpoll time
                    self.log.error("stop thread stream: " + streamId + " diff sec: " + str(diff.total_seconds()))
                    thread['pusher'].stop()
                    thread['running'] = False
            except Exception as e:
                self.log.erorr(e)
        self.threadLock.release()

def main():
    dirPath = "/home/map/tmp/2"
    cmd = "cd "+ dirPath + "\n"
    cmd += "gst-launch-1.0 rtspsrc location=\"" + "rtsp://" + "\" is-live=true ! rtph264depay ! mpegtsmux ! hlssink max-files=5 playlist-length=3 playlist-location=index.m3u8 playlist-root=\"/get-file-hls/" + str(2) +"\" target-duration=1 --gst-debug=3 >loggst.txt 2>&1"
    writeFileConfig(join(dirPath, 'rungst.sh'), cmd)
    exit(0)

    import urllib3
    urllib3.disable_warnings()

    stream = Camera()
    stream2 = Camera()
    stream.set_streamId(8)

    control = HlsPushControl()
    control.addStream(stream)
    control.prepareTmpDir()

    control.showListCam()
    control.startPushByCamId(8)

    sleep(20)
    stream11 = Camera()
    stream11.set_streamId(12)
    stream11.set_url("abc")

    stream12 = Camera()
    stream12.set_streamId(10)
    listCam = [stream12, stream11]
    control.updateConfig(listCam)
    control.showListCam()

    exit(0)
    
    while True:
        print("Main thread")
        sleep(5)
    exit(0)

if __name__ == "__main__":
    main()


