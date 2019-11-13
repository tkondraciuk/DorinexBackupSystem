from SMWinservice import SMWinservice


class BackupWindowsService(SMWinservice):
    def __init__(self):
        self._svc_name_ = "DorinexBackupSystem"
        self._svc_display_name_ = "Dorinex Backup System"
        self._svc_description_ = "It makes backup of important Dorinex files " \
                                 "and store them on the external network location"
        pass

    def Start(self):
        self.running = True
        pass

    def Stop(self):
        self.running = False
        pass

    def Main(self):
        pass
