import random
import string
import logging
from yt_dlp import YoutubeDL, DownloadError
from threading import RLock
from time import time
from re import search


