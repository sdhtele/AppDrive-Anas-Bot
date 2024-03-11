from time import sleep
from threading import Thread

from bot import aria2, download_dict_lock, download_dict, STOP_DUPLICATE, TORRENT_DIRECT_LIMIT, ZIP_UNZIP_LIMIT, LOGGER
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.ext_utils.bot_utils import is_magnet, getDownloadByGid, new_thread, get_readable_file_size
from bot.helper.mirror_utils.status_utils.aria_download_status import AriaDownloadStatus
from bot.helper.telegram_helper.message_utils import sendMarkup, sendStatusMessage, sendMessage
from bot.helper.ext_utils.fs_utils import get_base_name

# Function to start the listener for aria2 notifications
def start_listener():
    """
    Start listening to aria2 notifications in a threaded manner.
    Registers the following notification callbacks:
        - on_download_start
        - on_download_error
        - on_download_stop
        - on_download_complete
    """
    aria2.listen_to_notifications(threaded=True,
                                  on_download_start=__onDownloadStarted,
                                  on_download_error=__onDownloadError,
                                  on_download_stop=__onDownloadStopped,
                                  on_download_complete=__onDownloadComplete)

# Function to add a download to aria2 with the given link, path, listener, and filename
def add_aria2c_download(link: str, path, listener, filename):
    """
    Add a download to aria2 with the given parameters.
    If the link is a magnet link, use add_aria2.add_magnet, otherwise use add_aria2.add_uris.
    If there is an error during download addition, send the error message to the listener.
    Otherwise, add the download to the download_dict with the listener's uid as the key.
    """
    if is_magnet(link):
        download = aria2.add_magnet(link, {'dir': path, 'out': filename})
    else:
        download = aria2.add_uris([link], {'dir': path, 'out': filename})

    if download.error_message:
        error = str(download.error_message).replace('<', ' ').replace('>', ' ')
        LOGGER.info(f"Download Error: {error}")
        return sendMessage(error, listener.bot, listener.update)

    with download_dict_lock:
        download_dict[listener.uid] = AriaDownloadStatus(download.gid, listener)
        LOGGER.info(f"Started: {download.gid} DIR: {download.dir} ")
    sendStatusMessage(listener.update, listener.bot)

# Call the start_listener function to begin listening for aria2 notifications
start_listener()

