'''
Simply streamera class use to store streamId, rtsp link as main stream and stream,
tmp folder stored .ts file use to hls streamming
Author: ThangNX - thangnx97@gmail.com

stream: {
    streamId:
    mainstreams:
    streams:
    tmpFolder: //Folder contain m3u8, ts file, mp4 file
}
'''

from os.path import join
from default import DEFAULT_TMP
import logging
class Stream:
    def __init__(self, log = logging):
        self.streamId = None
        self.url = None 
        self.path = None
        self.tmpFolder = join(DEFAULT_TMP, 'tmp')
        self.bitrate = 0
        self.resolution = None
        self.inputCodec = None
        self.log = log

    def show(self):
        dic = {
            'stream_id': self.streamId, 
            'bitrate': self.bitrate, 
            'resolution': self.resolution, 
            'url': self.url, 
            'path': self.path, 
            'tmp_folder': self.tmpFolder,
            'input_codec': self.inputCodec
        }
        print(dic)

    def get_streamId(self) -> str:
        return self.streamId

    def get_url(self) -> str:
        return self.url

    def get_path(self) -> str:
        return self.path

    def get_bitrate(self) -> int:
        return self.bitrate

    def get_resolution(self) -> str:
        return self.resolution

    def get_inputCodec(self) -> str:
        return self.inputCodec

    def set_streamId(self, streamId):
        self.streamId = streamId

    def set_url(self, url):
        self.url = url

    def set_path(self, str):
        self.path = str
        self.tmpFolder = DEFAULT_TMP + str

    def set_bitrate(self, bitrate):
        self.bitrate = bitrate

    def set_resolution(self, resolution):
        self.resolution = resolution

    def set_inputCodec(self, inputCodec):
        self.inputCodec = inputCodec
