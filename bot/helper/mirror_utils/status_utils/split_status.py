from bot.helper.ext_utils.bot_utils import get_readable_file_size, MirrorStatus  # Import necessary modules

class SplitStatus:
    def __init__(self, name, path, size):
        """
        Initialize the SplitStatus class with the name, path, and size of the file being split.
        """
        self.__name = name  # Name of the file being split
        self.__path = path  # Path of the file being split
        self.__size = size  # Size of the file being split

    def progress(self):
        """
        Return the current progress of the file split as a string.
        """
        return '0'  # Placeholder value for progress

    def speed(self):
        """
        Return the current speed of the file split as a string.
        """
        return '0'  # Placeholder value for speed

    def name(self):
        """
        Return the name of the file being split.
        """
        return self.__name  # Return the name attribute

    def path(self):
        """
        Return the path of the file being split.
        """
        return self.__path  # Return the path attribute

    def size(self):
        """
        Return the size of the file being split in a human-readable format.
        """
        return get_readable_file_size(self.__size)  # Convert the size to a human-readable format

    def eta(self):
        """
        Return the estimated time of arrival (ETA) of the file split as a string.
        """
        return '0s'  # Placeholder value for ETA

    def status(self):
        """
        Return the current status of the file split.
        """
        return MirrorStatus.STATUS_SPLITTING  # Return the current status

    def processed_bytes(self):
        """
        Return the number of bytes processed during the file split.
        """
        return 0  # Placeholder value for processed bytes
