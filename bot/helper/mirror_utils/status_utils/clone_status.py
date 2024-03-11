from bot.helper.ext_utils.bot_utils import MirrorStatus, get_readable_file_size, get_readable_time

class CloneStatus:
    def __init__(self, obj, size, update, gid):
        """
        Initialize the CloneStatus object with the required parameters.
        :param obj: The object being cloned
        :param size: The total size of the object being cloned
        :param update: The update object containing message details
        :param gid: The global ID of the cloning operation
        """
        self.__obj = obj
        self.__size = size
        self.message = update.message
        self.__gid = gid

    def processed_bytes(self):
        """
        Return the number of bytes transferred so far.
        :return: The number of bytes transferred
        """
        return self.__obj.transferred_size

    def size_raw(self):
        """
        Return the total size of the object being cloned in bytes.
        :return: The total size of the object being cloned
        """
        return self.__size

    def size(self):
        """
        Return the total size of the object being cloned in a human-readable format.
        :return: The total size of the object being cloned in a human-readable format
        """
        return get_readable_file_size(self.__size)

    def status(self):
        """
        Return the current status of the cloning operation.
        :return: The current status of the cloning operation
        """
        return MirrorStatus.STATUS_CLONING

    def name(self):
        """
        Return the name of the object being cloned.
        :return: The name of the object being cloned
        """
        return self.__obj.name

    def gid(self) -> str:
        """
        Return the global ID of the cloning operation.
        :return: The global ID of the cloning operation
        """
        return self.__gid

    def progress_raw(self):
        """
        Calculate the progress of the cloning operation as a percentage.
        :return: The progress of the cloning operation as a percentage
        """
        try:
            return self.__obj.transferred_size / self.__size
