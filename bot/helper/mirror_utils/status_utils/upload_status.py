from bot.helper.ext_utils.bot_utils import MirrorStatus, get_readable_file_size, get_readable_time
from bot import DOWNLOAD_DIR


class UploadStatus:
    def __init__(self, obj, size, gid, listener):
        """
        Initialize the UploadStatus class with the necessary parameters.
        :param obj: The object being uploaded
        :param size: The total size of the object being uploaded
        :param gid: The global ID of the listener
        :param listener: The listener object
        """
        self.__obj = obj
        self.__size = size
        self.__uid = listener.uid
        self.__gid = gid
        self.message = listener.message

    def path(self):
        """
        Return the file path of the uploaded object.
        :return: The file path
        """
        return f"{DOWNLOAD_DIR}{self.__uid}"

    def processed_bytes(self):
        """
        Return the number of bytes that have been uploaded.
        :return: The number of uploaded bytes
        """
        return self.__obj.uploaded_bytes

    def size_raw(self):
        """
        Return the total size of the object being uploaded in bytes.
        :return: The total size in bytes
        """
        return self.__size

    def size(self):
        """
        Return the total size of the object being uploaded in a human-readable format.
        :return: The total size in a human-readable format
        """
        return get_readable_file_size(self.__size)

    def status(self):
        """
        Return the current status of the upload.
        :return: The current status
        """
        return MirrorStatus.STATUS_UPLOADING

    def name(self):
        """
        Return the name of the object being uploaded.
        :return: The name of the object
        """
        return self.__obj.name

    def progress_raw(self):
        """
        Calculate the progress of the upload in raw format (as a percentage).
        :return: The progress as a percentage
        """
        try:
            return self.__obj.uploaded_bytes / self.__size * 100
        except ZeroDivisionError:
            return 0

    def progress(self):
        """
        Return the progress of the upload in a human-readable format.
        :return: The progress as a formatted string

