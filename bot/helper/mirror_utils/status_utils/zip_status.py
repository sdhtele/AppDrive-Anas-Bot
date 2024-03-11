from bot.helper.ext_utils.bot_utils import get_readable_file_size, MirrorStatus  # Import necessary modules

class ZipStatus:
    def __init__(self, name, path, size):
        """
        Initialize the ZipStatus class with the name, path, and size of the file being archived.
        """
        self.__name = name  # Name of the file being archived
        self.__path = path  # Path of the file being archived
        self.__size = size  # Size of the file being archived

    def progress(self):
        """
        Return the current progress of the archiving process as a string.
        """
        return '0'  # Placeholder value, should be updated to reflect the actual progress

    def speed(self):
        """
        Return the current speed of the archiving process as a string.
        """
        return '0'  # Placeholder value, should be updated to reflect the actual speed

    def name(self):
        """
        Return the name of the file being archived.
        """
        return self.__name

    def path(self):
        """
        Return the path of the file being archived.
        """
        return self.__path

    def size(self):
        """
        Return the size of the file being archived in a human-readable format.
        """
        return get_readable_file_size(self.__size)

    def eta(self):
        """
        Return the estimated time until the archiving process is complete as a string.
        """
        return '0s'  # Placeholder value, should be updated to reflect the actual ETA

    def status(self):
        """
        Return the current status of the archiving process.
        """
        return MirrorStatus.STATUS_ARCHIVING  # The status of the archiving process

    def processed_bytes(self):
        """
        Return the number of bytes that have been processed in the archiving process.
        """
        return 0  # Placeholder value, should be updated to reflect the actual number of processed bytes

