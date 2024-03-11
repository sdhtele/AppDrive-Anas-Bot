from bot.helper.ext_utils.bot_utils import get_readable_file_size, MirrorStatus  # Import necessary modules

class ExtractStatus:
    def __init__(self, name, path, size):
        """
        Initialize the ExtractStatus class with name, path, and size.

        :param name: The name of the file being extracted
        :param path: The path of the file being extracted
        :param size: The size of the file being extracted
        """
        self.__name = name
        self.__path = path
        self.__size = size

    # The progress of the extract function cannot be tracked. 
    # If this is possible in the future, we should implement it.

    def progress(self):
        """
        Return a dummy value for the progress of the extract function since it cannot be tracked.

        :return: A dummy string '0'
        """
        return '0'

    def speed(self):
        """
        Return a dummy value for the speed of the extract function since it cannot be tracked.

        :return: A dummy string '0'
        """
        return '0'

    def name(self):
        """
        Return the name of the file being extracted.

        :return: The name of the file
        """
        return self.__name

    def path(self):
        """
        Return the path of the file being extracted.

        :return: The path of the file
        """
        return self.__path

    def size(self):
        """
        Return the size of the file being extracted in a readable format.

        :return: The size of the file in a readable format
        """
        return get_readable_file_size(self.__size)

    def eta(self):
        """
        Return a dummy value for the estimated time of arrival since it cannot be calculated.

        :return: A dummy string '0s'
        """
        return '0s'

    def status(self):
        """
        Return the current status of the extract function.

        :
