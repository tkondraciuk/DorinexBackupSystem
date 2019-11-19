import logging
from datetime import date
import os

logDirectory = 'C:/Python/DorinexBackupSystem/logs/'


def get_log_file_name():
    return logDirectory + date.today().strftime('%Y-%m-%d') + ".log"


fileHandler = logging.FileHandler(get_log_file_name())
fileHandler.setLevel(logging.INFO)

dateFormat = '[%H:%M:%S]'
logFormat = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s', dateFormat)
fileHandler.setFormatter(logFormat)


def getLogger(name):
    logger = logging.getLogger(name)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)
    return logger
