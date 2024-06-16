import configparser
import src.logger
import sys, os

# ACCESS and SECRET KEY
ACCESS_KEY = None
SECRET_KEY = None

# Program Log Setting
# Log Level [DEBUG, INFO, ERROR, OFF]
LOG_LEVEL = 'ERROR'
# Dogee Program Log Saving Path
LOG_SAVEPATH = './data/Dogee.log'

# Push Service Setting
# deerpush
PUSHDEER_KEYS = []
# pushover
PUSHOVER_APP_TOKEN = None
PUSHOVER_USERS = []

# CDN Log Saving Setting
CDN_LOG_SAVE_ENABLE = False
# Merge Log
MERGE_LOG = True
# CDN Log Store Path
CDN_LOGS_STOREPATH = './data/cdnlog'
# TimeZone
CDN_LOGS_TIMEZONE = 'Asia/Chongqing'



def convert_str_to_list(s : str) -> list:
    '''
    Convert string to list

    :param s: string to convert
    :returns: list
    '''
    s = "".join(s.split()) # Remove the spaces
    return s.split(',')

# Load Configuration File
config = configparser.ConfigParser()
try:
    with open('config.ini') as f:
        config.read_file(f)
except IOError:
    logger.new('error', 'Cannot open configuration file.')

sections = config.sections()
for s in sections:
    if s == 'doge-cloud-key':
        this_config = config['doge-cloud-key']
        ACCESS_KEY = this_config.get('access_key')
        SECRET_KEY = this_config.get('secret_key')
    elif s == 'dogee-log':
        this_config = config['dogee-log']
        if 'log_level' in this_config:
            LOG_LEVEL = this_config['log_level'].upper()
        if 'log_savepath' in this_config:
            LOG_SAVEPATH = this_config['log_savepath']
    elif s == 'dogee-push':
        this_config = config['dogee-push']
        if 'pushdeer_keys' in this_config:
            keys = this_config['pushdeer_keys']
            PUSHDEER_KEYS = convert_str_to_list(keys)
        if 'pushover_app_token' in this_config and 'pushover_user_key' in this_config:
            PUSHOVER_APP_TOKEN = this_config['pushover_app_token']
            PUSHOVER_USERS = convert_str_to_list(this_config['pushover_user_key'])
    elif s == 'doge-cloud-cdn-log-download':
        this_config = config['doge-cloud-cdn-log-download']
        CDN_LOG_SAVE_ENABLE = True
        if 'merge_log' in this_config:
            MERGE_LOG = this_config.getboolean('merge_log')
        if 'cdn_logs_storepath' in this_config:
            CDN_LOGS_STOREPATH = this_config['cdn_logs_storepath']
        if 'timezone' in this_config:
            CDN_LOGS_TIMEZONE = this_config['timezone']


# Sanity Check
# Make sure access_key and secret_key are not empty
if not ACCESS_KEY or not SECRET_KEY:
    logger.new('error', 'ACCESS_KEY and SECRET_KEY cannot be empty.')
    sys.exit(1)

# Create Necessary Directory
# if not os.path.exists(LOG_SAVEPATH):
#     os.makedirs(LOG_SAVEPATH)


# # Print Configuration Setting
# print('------------Config-Setting-------------')
# print('ACCESS_KEY:', ACCESS_KEY)
# print('SECRET_KEY:', SECRET_KEY)
# print('LOG_LEVEL:', LOG_LEVEL)
# print('LOG_SAVEPATH:', LOG_SAVEPATH)
# print('PUSHDEER_KEYS:', PUSHDEER_KEYS)
# print('PUSHOVER_APP_TOKEN:', PUSHOVER_APP_TOKEN)
# print('PUSHOVER_USERS:', PUSHOVER_USERS)
# print('CDN_LOG_SAVE_ENABLE:', CDN_LOG_SAVE_ENABLE)
# print('MERGE_LOG:', MERGE_LOG)
# print('CDN_LOGS_STOREPATH:', CDN_LOGS_STOREPATH)
# print('CDN_LOGS_TIMEZONE:', CDN_LOGS_TIMEZONE)
# print('---------End--Config-Setting-----------')