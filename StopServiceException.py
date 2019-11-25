class StopServiceException(Exception):
    def __str__(self):
        return "Error was occurred, the Backup System is terminating..."
