import requests
import json
from default import CMS_SERVER
from default import SERIAL_NUMBER, EDGE_ID, LOGIN_PATH, GET_CONFIG_PATH, SERIAL_NUMBER, DEFAULT_PRIVATE_PATH, DEFAULT_PASSPHRASE, UPDATE_STS_PATH , DEFAULT_DEEP_APP, DEFAULT_DEEP_APP_CFG, DEFAULT_DEEP_APP_CFG_ZIP, GET_FILE_CONFIG
import threading
import logging
from time import sleep

class RequestControl:
    def __init__(self, log = logging): 
        self.cms_addr = CMS_SERVER
        self.login_uri = CMS_SERVER + LOGIN_PATH
        self.get_config_uri = CMS_SERVER + GET_CONFIG_PATH
        self.update_status_uri = CMS_SERVER + UPDATE_STS_PATH
        self.serial_number = SERIAL_NUMBER
        self.token = ""
        self.jwt_token = ""
        self.id = EDGE_ID
        self.is_auth = False
        self.runningThread = 0
        self.log = log

    def login(self):
        pass

    
    def tryLogin(self):

        self.login()


    def tryLoginUntilSuccess(self):
        self.login()
