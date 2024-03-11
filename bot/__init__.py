# Import necessary libraries and modules
import logging
import socket
import faulthandler

# Import libraries for handling Telegram bot and qBittorrent API
from telegram.ext import Updater as tgUpdater
from qbittorrentapi import Client as qbClient

# Import libraries for handling Aria2 API and subprocess management
from aria2p import API as ariaAPI, Client as ariaClient
from subprocess import Popen, run as srun, check_output

# Import libraries for time management and threading
from time import sleep, time
from threading import Thread, Lock

# Import libraries for handling pyrogram sessions and environment variables
import os
import environ
from dotenv import load_dotenv
