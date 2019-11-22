import os
import yaml
from datetime import datetime
from zipfile import ZipFile

import LoggerUtils
from FTPController import FTPController
from StopServiceException import StopServiceException


class BackupService:
    rootPathEnVar = "DorinexBackupSystem_home"
    zipFilePath = ''
    loggerName = 'Backup Service'
    filesToBackup = []

    def __init__(self):
        self.logger = LoggerUtils.getLogger(self.loggerName)
        self._loadConfig()
        self.ftpController = FTPController()

    def makeBackup(self):
        self._packFiles()
        self.ftpController.uploadFile(self.zipFilePath)
        os.remove(self.zipFilePath)
        self.zipFilePath = ''

    def _getAllPaths(self, directory):
        if not os.path.exists(directory):
            self.logger.warning('%s not found. The file/directory will be skipped.', directory)
            return []
        if os.path.isfile(directory):
            return [directory]
        filePaths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                filePaths.append(path)
        return filePaths

    def _packFiles(self):
        paths = []
        for path in self.filesToBackup:
            paths.extend(self._getAllPaths(path))
        if self.zipFilePath == '':
            self._setZipFilePath()
        with ZipFile(self.zipFilePath, 'w') as zip:
            packed = 0
            for file in paths:
                zip.write(file)
                packed += 1
                self.logger.info('%s was successfully packed.', file)
            self.logger.info('%i of %i files was successfully packed.', packed, len(paths))

    def _setZipFilePath(self):
        zipFileName = datetime.now().strftime('%Y-%m-%d %H.%M') + ".zip"
        self.zipFilePath = os.environ[self.rootPathEnVar] + "\\zip\\" + zipFileName

    def _loadConfig(self):
        try:
            with open(os.environ[self.rootPathEnVar] + '\\config.yaml') as file:
                config = yaml.full_load(file)
            self.filesToBackup = config['filesToBackup']
        except Exception as e:
            self.logger.error(e)
            self.logger.error("System was't able to read configs. Check the \'config.yaml\'.")
            raise StopServiceException
        pass


# bs = BackupService()
# bs.makeBackup()
