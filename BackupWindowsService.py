import random
import sys
import time
from pathlib import Path

import servicemanager as servicemanager

from SMWinservice import SMWinservice
from threading import Timer
from _datetime import timedelta


from BackupService import BackupService


def test():
    print("Hello world")


class BackupWindowsService(SMWinservice):
    interval = timedelta(seconds=10).seconds
    _svc_display_name_ = "Dorinex Backup System"
    _svc_name_ = "DorinexBackupSystem"
    _svc_description_ = "It makes backup of important Dorinex files " \
                        "and store them on the external network location"

    def __init__(self, args):
        super().__init__(args)
        pass

    def start(self):
        self.isrunning = True
        self.backupService = BackupService()
        self.running = True
        self.timer = Timer(self.interval, test)
        pass

    def stop(self):
        self.isrunning = False
        # self.running = False
        pass

    def Main(self):
        while self.running:
            if not self.timer.is_alive():
                self.Start()
        self.timer.cancel()

        pass

if __name__ == '__main__':
    BackupWindowsService.parse_command_line()

