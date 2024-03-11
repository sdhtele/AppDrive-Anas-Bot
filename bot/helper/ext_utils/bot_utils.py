from re import match, findall  # Importing regular expression functions
from threading import Thread, Event  # Importing threading functions
from time import time  # Importing time functions
from math import ceil  # Importing math functions
from psutil import virtual_memory, cpu_percent, disk_usage  # Importing psutil functions
from requests import head as rhead  # Importing requests function
from urllib.request import urlopen  # Importing urllib function
from telegram import InlineKeyboardMarkup  # Importing Telegram function

from bot.helper.telegram_helper.bot_commands import BotCommands  # Importing custom bot commands
from bot import download_dict, download_dict_lock, STATUS_LIMIT, botStartTime  # Importing custom variables
from bot.helper.telegram_helper.button_build import ButtonMaker  # Importing custom button builder

# Regular expression for magnet links
MAGNET_REGEX = r"magnet:\?xt=urn:btih:[a-zA-Z0-9]*"

# Regular expression for URLs
URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"

# Global variables for pagination
COUNT = 0
PAGE_NO = 1

class MirrorStatus:  # Class for mirror status
    # Status constants
    STATUS_UPLOADING = "Uploading...📤"
    STATUS_DOWNLOADING = "Downloading...📥"
    STATUS_CLONING = "Cloning...♻️"
    STATUS_WAITING = "Queued...💤"
    STATUS_FAILED = "Failed 🚫. Cleaning Download..."
    STATUS_PAUSE = "Paused...⛔️"
    STATUS_ARCHIVING = "Archiving...🔐"
    STATUS_EXTRACTING = "Extracting...📂"
    STATUS_SPLITTING = "Splitting...✂️"
    STATUS_CHECKING = "CheckingUp...📝"
    STATUS_SEEDING = "Seeding...🌧"

# Size units for file sizes
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

class setInterval:  # Class for setting interval
    def __init__(self, interval, action):  # Constructor
        self.interval = interval
        self.action = action
        self.stopEvent = Event()
        thread = Thread(target=self.__setInterval)  # Creating a new thread
        thread.start()

    def __setInterval(self):  # Method for setting interval
        nextTime = time() + self.interval
        while not self.stopEvent.wait(nextTime - time()):
            nextTime += self.interval
            self.action()

    def cancel(self):  # Method for canceling the interval
        self.stopEvent.set()

def get_readable_file_size(size_in_bytes) -> str:  # Function for getting readable file size
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

def getDownloadByGid(gid):  # Function for getting download by gid
    with download_dict_lock:
        for dl in list(download_dict.values()):
            status = dl.status()
            if (
                status
                not in [
                    MirrorStatus.STATUS_ARCHIVING,
                    MirrorStatus.STATUS_EXTRACTING,
                    MirrorStatus.STATUS_SPLITTING,
                ]
                and dl.gid() == gid
            ):
                return dl
    return None

def getAllDownload():  # Function for getting all downloads
    with download_dict_lock:
        for dlDetails in list(download_dict.values()):
            status = dlDetails.status()
            if (
                status
                not in [
                    MirrorStatus.STATUS_ARCHIVING,
                    MirrorStatus.STATUS_EXTRACTING,
                    MirrorStatus.STATUS_SPLITTING,
                    MirrorStatus.STATUS_CLONING,
                    MirrorStatus.STATUS_UPLOADING,
                    MirrorStatus.STATUS_CHECKING,
                ]
                and dlDetails
            ):
                return dlDetails
    return None

def get_progress_bar_string(status):  # Function for getting progress bar string
    completed = status.processed_bytes() / 8
    total = status.size_raw() / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 8
    p_str = '■' * cFull
    p_str += '□' * (12 - cFull)
    p_str = f"[{p_str}]"
    return p_str

def get_readable_message():  # Function for getting readable message
    with download_dict_lock:
        msg = ""
        dlspeed_bytes = 0
        uldl_bytes = 0
        START = 0
        if STATUS_LIMIT is not None:
            tasks = len(download_dict)
            global pages
            pages = ceil(tasks/STATUS_LIMIT)
            if PAGE_NO > pages and pages != 0:
                globals()['COUNT'] -= STATUS_LIMIT
                globals()['PAGE_NO'] -= 1
            START = COUNT
        for index, download in enumerate(list(download_dict.values())[START:], start=1):
            msg += f"<b>Name:</b>
