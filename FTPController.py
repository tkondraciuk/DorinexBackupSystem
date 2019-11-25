import ftplib
import os
import socket
import ConfigReader
import LoggerUtils

from ftplib import FTP
from StopServiceException import StopServiceException


class FTPController:
    rootPathEnVar = "DorinexBackupSystem_home"
    STOR_command = "STOR %s"
    loggerName = 'FTPController'
    isInit = True;

    def __init__(self):
        self.logger = LoggerUtils.getLogger(self.loggerName)
        self.session = FTP()
        self._loadConfig()
        self._setConnection()
        self.isInit = False
        pass

    def _loadConfig(self):
        self.host = ConfigReader.host
        self.login = ConfigReader.login
        self.password = ConfigReader.password
        self.uploadLocation = ConfigReader.uploadLocation
        pass

    def uploadFile(self, filePath):
        if not self.isConnectionActive():
            self._setConnection()

        if self.session.pwd() != self.uploadLocation:
            self.session.cwd(self.uploadLocation)

        file = open(filePath, 'rb')
        try:
            self.session.storbinary(self._getSTORCommand(filePath), file)
        except IOError as e:
            self.logger.error(e)

        pass

    def _getSTORCommand(self, filePath):
        return self.STOR_command % os.path.basename(filePath)

    def _setConnection(self):
        try:
            self.session.connect(self.host)
            self.session.login(self.login, self.password)
        except (ftplib.error_perm, TimeoutError):
            self.logger.error('Server connection failed. '
                              'Make sure that host is online and connection data are correct.')
            raise StopServiceException

        try:
            self.session.cwd(self.uploadLocation)
        except ftplib.error_perm:
            self.logger.error('Upload location (%s) does not exist at the host\'s machine.')
            raise StopServiceException

        if self.isInit:
            self.logger.info('Connection with %s established.', self.host)
        else:
            self.logger.info('Connection with %s refreshed', self.host)

    def isConnectionActive(self):
        try:
            self.session.voidcmd('NOOP')
        except (socket.error, IOError):
            return False
        return True

    def __del__(self):
        self.session.close()
