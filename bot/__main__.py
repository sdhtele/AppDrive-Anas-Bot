import signal  # Importing signal module to handle SIGINT signal

from os import path as ospath, remove as osremove, execl as osexecl  # Importing necessary functions from os module
from subprocess import run as srun  # Importing run function from subprocess module
from asyncio import run as asyrun  # Importing run function from asyncio module
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, Process as psprocess  # Importing necessary functions from psutil module
from time import time  # Importing time function from time module
from pyrogram import idle  # Importing idle function from pyrogram module
from sys import executable  # Importing executable from sys module
from telegram import ParseMode, InlineKeyboardMarkup  # Importing necessary classes from telegram module
from telegram.ext import CommandHandler  # Importing CommandHandler from telegram.ext module

# Importing various modules, classes, and functions from other files in the same package
from wserver import start_server_async
from bot import bot, app, dispatcher, updater, botStartTime, IGNORE_PENDING_REQUESTS, IS_VPS, PORT, alive, web, OWNER_ID, AUTHORIZED_CHATS, LOGGER, Interval, nox, rss_session, a2c
from .helper.ext_utils.fs_utils import start_cleanup, clean_all, exit_clean_up
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage, sendLogFile
from .helper.ext_utils.telegraph_helper import telegraph
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.button_build import ButtonMaker
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, shell, eval, delete, speedtest, count, leech_settings, search, rss

def stats(update, context):
    """
    This function sends various system stats as a message.
    """
    currentTime = get_readable_time(time() - botStartTime)
    total, used, free, disk= disk_usage('/')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(net_io_counters().bytes_sent)
    recv = get_readable_file_size(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = get_readable_file_size(swap.total)
    swap_u = get_readable_file_size(swap.used)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = get_readable_file_size(memory.total)
    mem_a = get_readable_file_size(memory.available)
    mem_u = get_readable_file_size(memory.used)
    stats = f'<b>Bot Uptime:</b> {currentTime}\n\n'\
            f'<b>Total Disk Space:</b> {total}\n'\
            f'<b>Used:</b> {used} | <b>Free:</b> {free}\n\n'\
            f'<b>Upload:</b> {sent}\n'\
            f'<b>Download:</b> {recv}\n\n'\
            f'<b>CPU:</b> {cpuUsage}%\n'\
            f'<b>RAM:</b> {mem_p}%\n'\
            f'<b>DISK:</b> {disk}%\n\n'\
            f'<b>Physical Cores:</b> {p_core}\n'\
            f'<b>Total Cores:</b> {t_core}\n\n'\
            f'<b>SWAP:</b> {swap_t} | <b>Used:</b> {swap_p}%\n'\
            f'<b>Memory Total:</b> {mem_t}\n'\
            f'<b>Memory Free:</b> {mem_a}\n'\
            f'<b>Memory Used:</b> {mem_u}\n©️ Modded By @Kai_8_4'
    sendMessage(stats, context.bot, update)

def start(update, context):
    """
    This function sends a welcome message and an inline keyboard with buttons to the user.
    """
    buttons = ButtonMaker()
    buttons.buildbutton("Repo", "https://www.github.com/anasty17/mirror-leech-telegram-bot")
    buttons.buildbutton("Report Group", "https://t.me/+MwgSi5vmQEA2N2Vk")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(2))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        start_string = f'''
This bot can mirror all your links to Google Drive!
Type /{BotCommands.HelpCommand} to get a list of available commands
'''
        sendMarkup(start_string, context.bot, update, reply_markup)
    else:
        sendMarkup('Not Authorized user, deploy your own mirror-leech bot', context.bot, update, reply_markup)

def restart(update, context):
    """
    This function restarts the bot and sends a message to the user.
    """
    restart_message = sendMessage("Restarting...", context.bot, update)
    if Interval:
        Interval[0].cancel()
    alive.kill
