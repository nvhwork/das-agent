SERVER_ADDR = "http://127.0.0.1:5000"
RECONNECT_TIME = 5 # 30 seconds
EDGE_ID = 1
SERIAL_NUMBER="1422419148569"
CMS_SERVER = "http://192.168.1.129"
LOGIN_PATH = "/api/edge-login"
GET_CONFIG_PATH = "/api/edge-config"
UPDATE_STS_PATH = "/api/update-status"
PUSH_FILE_HLS_PATH = '/api/upload-to-cache'
GET_FILE_CONFIG = '/api/download-config-file'
DEFAULT_PRIVATE_PATH = "/home/map/.ssh/id_rsa"
DEFAULT_PASSPHRASE = None
from os.path import expanduser, join
HOME = expanduser("~")
DEFAULT_TMP = join(HOME, "tmp")
DEFAULT_DEEP_APP = join(HOME, 'deepApp')
DEFAULT_DEEP_APP_PATH = join(DEFAULT_DEEP_APP, 'dasApp.sh')
DEFAULT_DEEP_APP_CFG = join(DEFAULT_DEEP_APP, 'config')
DEFAULT_DEEP_APP_CFG_ZIP = join(DEFAULT_DEEP_APP, 'config.zip')


KEY_SERVER_ADDR='server_addr'
KEY_RECONECT_TIME = 'reconnect_time'
KEY_EDGE_ID = 'edge_id'
KEY_SN = 'sn'
KEY_CMS_ADDR = 'cms_addr'
KEY_LOGIN_P = 'login_path'
KEY_GET_CFG_P = 'config_path'
KEY_UPDATE_STS_P = 'update_sts_path'
KEY_PUSH_HLS_P = 'hls_path'
KEY_GET_FILE_CFG_P = 'get_file_cfg_path'
KEY_DEF_PRI_P = 'pri_path'
KEY_DEF_PASS = 'def_pass'
KEY_DEF_TMP_DIR = 'def_tmp_dir'
KEY_DEF_APP_DIR = 'def_app_dir'

import json

try:
    f = open('config.json')
    conf = json.load(f)
    if (KEY_SERVER_ADDR in conf):
        SERVER_ADDR = conf[KEY_SERVER_ADDR]

    if (KEY_RECONECT_TIME in conf):
        RECONNECT_TIME = conf[KEY_RECONECT_TIME]

    if (KEY_EDGE_ID in conf):
        EDGE_ID = conf[KEY_EDGE_ID]

    if (KEY_SN in conf):
        SERIAL_NUMBER = conf[KEY_SN]

    if (KEY_CMS_ADDR in conf):
        CMS_SERVER = conf[KEY_CMS_ADDR]

    if (KEY_LOGIN_P in conf):
        LOGIN_PATH = conf[KEY_LOGIN_P]

    if (KEY_GET_CFG_P in conf):
        GET_CONFIG_PATH = conf[KEY_GET_CFG_P]

    if (KEY_UPDATE_STS_P in conf):
        UPDATE_STS_PATH = conf[KEY_UPDATE_STS_P]

    if (KEY_PUSH_HLS_P in conf):
        PUSH_FILE_HLS_PATH = conf[KEY_PUSH_HLS_P]

    if (KEY_GET_FILE_CFG_P in conf):
        GET_FILE_CONFIG = conf[KEY_GET_FILE_CFG_P]

    if (KEY_DEF_PRI_P in conf):
        DEFAULT_PRIVATE_PATH = conf[KEY_DEF_PRI_P]

    if (KEY_DEF_PASS in conf):
        DEFAULT_PASSPHRASE = conf[KEY_DEF_PASS]

    if (KEY_DEF_TMP_DIR in conf):
        DEFAULT_TMP = conf[KEY_DEF_TMP_DIR]

    if (KEY_DEF_APP_DIR in conf):
        DEFAULT_DEEP_APP = conf[KEY_DEF_APP_DIR]
        DEFAULT_DEEP_APP_PATH = join(DEFAULT_DEEP_APP, 'dasApp.sh')
        DEFAULT_DEEP_APP_CFG = join(DEFAULT_DEEP_APP, 'config')
        DEFAULT_DEEP_APP_CFG_ZIP = join(DEFAULT_DEEP_APP, 'config.zip')
except Exception as e:
    print(e)
print(SERVER_ADDR)
print(RECONNECT_TIME)
print(EDGE_ID)
print(SERIAL_NUMBER)
print(CMS_SERVER)
print(LOGIN_PATH)
print(UPDATE_STS_PATH)
print(GET_CONFIG_PATH)
print(GET_FILE_CONFIG)
print(PUSH_FILE_HLS_PATH)
print(DEFAULT_PRIVATE_PATH)
print(DEFAULT_PASSPHRASE)
print(DEFAULT_TMP)
print(DEFAULT_DEEP_APP)
print(DEFAULT_DEEP_APP_CFG)
print(DEFAULT_DEEP_APP_CFG_ZIP)

#For server
DEFAULT_PORT = 5000
KEY_PATH = '/etc/apache2/ssl/dascam.key'
CERT_PATH = '/etc/apache2/ssl/dascan.crt'
ENV_PATH = '.env'
