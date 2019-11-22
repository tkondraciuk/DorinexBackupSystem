import random
import sys
import time
from pathlib import Path

import servicemanager as servicemanager

import LoggerUtils
from SMWinservice import SMWinservice
from RepeatingTimer import RepeatingTimer
from _datetime import timedelta

from BackupService import BackupService
from StopServiceException import StopServiceException


def test():
    print("Hello world")


class BackupWindowsService(SMWinservice):
    loggerName = 'BackupWindowsService'
    interval = timedelta(seconds=10).seconds
    _svc_display_name_ = "Dorinex Backup System"
    _svc_name_ = "DorinexBackupSystem"
    _svc_description_ = "It makes backup of important Dorinex files " \
                        "and store them on the external network location"

    def __init__(self, args):
        self.logger = LoggerUtils.getLogger(self.loggerName)
        super().__init__(args)
        self.isrunning = False
        pass

    def start(self):
        self.logger.info("Starting the Backup System...")
        try:
            self.backupService = BackupService()
            self.timer = RepeatingTimer(self.interval, self.backupService.makeBackup)
            self.isrunning = True
        except StopServiceException as e:
            self.logger.error(e)
            self.SvcStop()
        pass

    def stop(self):
        self.timer.cancel()
        self.isrunning = False
        self.logger.info('The Backup System was stopped.')
        pass

    def main(self):
        self.timer.start()
        self.logger.info("The Backup System was successfully started.")
        try:
            while self.isrunning:
                pass
        except StopServiceException as e:
            self.logger.error(e)
            self.SvcStop()

        pass


if __name__ == '__main__':
    BackupWindowsService.parse_command_line()
