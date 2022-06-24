import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


'''
Setup logging
'''
def setupLog(saveFile, sLevel):
    logLevel = logging.ERROR
    sLevel = sLevel.upper()
    if sLevel == "DEBUG":
        logLevel = logging.DEBUG
    elif sLevel == "INFO":
        logLevel = logging.INFO
    elif sLevel == "ERROR":
        logLevel = logging.ERROR
    if saveFile:
        _now = datetime.now()
        _log_file_name = _now.strftime("%Y-%m-%d_%H-%M-%S") + ".log"
        # logging.basicConfig(format='%(asctime)s %(message)s',  datefmt='%Y-%m-%d %H:%M:%S ', filename= _log_file_name + '.log', level=logLevel)
        _log_format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(funcName)s(%(lineno)d) %(message)s')
        handler = RotatingFileHandler(_log_file_name, mode='a', maxBytes= 5*1024*1024, backupCount=10, delay=0)
        handler.setFormatter(_log_format)
        log = logging.getLogger()
        log.setLevel(logLevel)
        log.addHandler(handler)
        return log
    else:
        logging.basicConfig(format = '%(asctime)s %(levelname)s %(filename)s:%(funcName)s(%(lineno)d) %(message)s')
        log = logging.getLogger()
        log.setLevel(logLevel)
        return log