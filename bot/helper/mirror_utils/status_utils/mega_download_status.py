from bot.helper.ext_utils.bot_utils import get_readable_file_size,MirrorStatus, get_readable_time
from bot import DOWNLOAD_DIR

class MegaDownloadStatus:
    """
    A class representing the status of a Mega download.
    """

    def __init__(self, obj, listener):
        """
        Initialize a new MegaDownloadStatus object.

        :param obj: The download object to monitor.
        :type obj: object
        :param listener: The listener object to use for sending messages.
        :type listener: object
        """
        self.__uid = obj.uid  # The unique identifier for the download.
        self.__listener = listener  # The listener object for sending messages.
        self.__obj = obj  # The download object to monitor.
        self.message = listener.message  # The message object to send responses to.

    def name(self) -> str:
        """
        Get the name of the download.

        :return: The name of the download.
        :rtype: str
        """
        return self.__obj.name

    def progress_raw(self):
        """
        Calculate the progress of the download in raw format (as a percentage).

        :return: The progress of the download as a percentage.
        :rtype: float
        """
        try:
            return round(self.processed_bytes() / self.__obj.size * 100,2)
        except ZeroDivisionError:
            return 0.0

    def progress(self):
        """
        Get the progress of the download as a formatted string.

        :return: The progress of the download as a formatted string.
        :rtype: str
        """
        return f"{self.progress_raw()}%"

    def status(self) -> str:
        """
        Get the current status of the download.

        :return: The current status of the download.
        :rtype: str
        """
        return MirrorStatus.STATUS_DOWNLOADING

    def processed_bytes(self):
        """
        Get the number of bytes that have been processed by the download.

        :return: The number of processed bytes.
        :rtype: int
        """
        return self.__obj.downloaded_bytes

    def eta(self):
        """
        Calculate the estimated time of arrival for the download.

        :return: The estimated time of arrival as a formatted string.
        :rtype: str
        """
        try:
            seconds = (self.size_raw() - self.processed_bytes()) / self.speed_raw()
            return f'{
