class StopServiceException(Exception):
    def __str__(self):
        return "Error was occured, the Backup System is terminating..."
