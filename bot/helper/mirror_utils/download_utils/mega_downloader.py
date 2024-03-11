import random
import string
from os import makedirs
from threading import Event
from mega import (MegaApi, MegaListener, MegaRequest, MegaTransfer, MegaError)
# Import necessary modules for Mega API integration

from bot import LOGGER, MEGA_API_KEY, download_dict_lock, download_dict, MEGA_EMAIL_ID, MEGA_PASSWORD, MEGA_LIMIT, STOP_DUPLICATE, ZIP_UNZIP_LIMIT
# Import necessary modules for bot integration and configuration

class MegaAppListener(MegaListener):
    def __init__(self, continue_event: Event, listener):
        # Initialize the MegaAppListener class with a continue event and a listener object
        self.continue_event = continue_event
        self.node = None
        self.public_node = None
        self.listener = listener
        self.uid = listener.uid
        self.__bytes_transferred = 0
        self.is_cancelled = False
        self.__speed = 0
        self.__name = ''
        self.__size = 0
        self.error = None
        self.gid = ""
        super(MegaAppListener, self).__init__()

    @property
    def speed(self):
        # Returns the speed of the download in bytes/second
        return self.__speed

    @property
    def name(self):
        # Returns the name of the download
        return self.__name

    def setValues(self, name, size, gid):
        # Sets the name, size, and global ID (gid) of the download
        self.__name = name
        self.__size = size
        self.gid = gid

    @property
    def size(self):
        # Returns the size of the download in bytes
        return self.__size

    @property
    def downloaded_bytes(self):
        # Returns the number of bytes downloaded
        return self.__bytes_transferred

    def onRequestFinish(self, api, request, error):
        # Handles the finish event of a Mega API request
        if str(error).lower() != "no error":
            self.error = error.copy()
            return
        # Handle different types of requests and set the continue event accordingly

    def onRequestTemporaryError(self, api, request, error: MegaError):
        # Handles temporary errors during Mega API requests
        LOGGER.error(f'Mega Request error in {error}')
        if not self.is_cancelled:
            self.is_cancelled = True
            self.listener.onDownloadError("RequestTempError: " + error.toString())
        self.error = error.toString()
        self.continue_event.set()

    def onTransferUpdate(self, api: MegaApi, transfer: MegaTransfer):
        # Handles updates to the download transfer
        if self.is_cancelled:
            api.cancelTransfer(transfer, None)
            self.continue_event.set()
            return
        # Update the speed and bytes transferred of the download

    def onTransferFinish(self, api: MegaApi, transfer: MegaTransfer, error):
        # Handles the finish event of a Mega transfer
        try:
            if self.is_cancelled:
                self.continue_event.set()
            elif transfer.isFinished() and (transfer.isFolderTransfer() or transfer.getFileName() == self.name):
                # Handle the completion of the download and set the continue event
                self.listener.onDownloadComplete()
                self.continue_event.set()
        except Exception as e:
            LOGGER.error(e)

    def onTransferTemporaryError(self, api, transfer, error):
        # Handles temporary errors during Mega transfers
        filen = transfer.getFileName()
        state = transfer.getState()
        errStr = error.toString()
        LOGGER.error(f'Mega download error in file {transfer} {filen}: {error}')
        if state in [1, 4]:
            # Handle specific states of the transfer and set the error message accordingly
            return

        self.error = errStr
        if not self.is_cancelled:
            self.is_cancelled = True
            self.listener.onDownloadError(f"TransferTempError: {errStr} ({filen})")
            self.continue_event.set()

    def cancel_download(self):
        # Cancels the download and sets the error message
        self.is_cancelled = True
        self.listener.onDownloadError("Download Canceled by user")


class AsyncExecutor:
    def __init__(self):
        # Initialize the AsyncExecutor class with a continue event
        self.continue_event = Event()

    def do(self, function, args):
        # Executes a function asynchronously and waits for it to complete
        self.continue_event.clear()
        function(*args)
        self.continue_event.wait()

listeners = []
