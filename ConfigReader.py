import yaml
import os

import LoggerUtils
from StopServiceException import StopServiceException

logger = LoggerUtils.getLogger('ConfigReader')
configPath = os.environ['DorinexBackupSystem_home'] + '\\config.yaml'


def loadConfigs():
    try:
        with open(configPath, 'r') as configFile:
            configs = yaml.full_load(configFile)
    except Exception as e:
        logger.error(e)
        logger.error("System was't able to read configs. Check the \'config.yaml\'.")
        raise StopServiceException
    return configs
    pass


configs = loadConfigs()
try:
    timeInterval = float(configs['timeInterval'])
    host = configs['remoteStorage']['host']
    login = configs['remoteStorage']['login']
    password = configs['remoteStorage']['password']
    uploadLocation = configs['remoteStorage']['uploadLocation']
    filesToBackup = configs['filesToBackup']
except KeyError as ke:
    logger.warning('Key {} not found in config file. It may cause some problems in the future.'.format(ke.args[0]))
