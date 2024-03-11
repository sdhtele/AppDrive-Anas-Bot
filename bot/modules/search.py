import itertools

from requests import get as rget
from time import sleep
from threading import Thread
from html import escape
from urllib.parse import quote
from telegram import InlineKeyboardMarkup, CallbackQueryHandler
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackContext
from bot import dispatcher, LOGGER, SEARCH_API_LINK, SEARCH_PLUGINS, get_client
from bot.helper.ext_utils.telegraph_helper import telegraph
from bot.helper.telegram_helper.message_utils import editMessage, sendMessage, sendMarkup
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import get_readable_file_size
from bot.helper.telegram_helper import button_build

# Define global variables
SITES = {
    "1337x": "1337x",
    "yts": "YTS",
    "eztv": "EzTv",
    "tgx": "TorrentGalaxy",
    "torlock": "Torlock",
    "piratebay": "PirateBay",
    "nyaasi": "NyaaSi",
    "rarbg": "Rarbg",
    "ettv": "Ettv",
    "zooqle": "Zooqle",
    "kickass": "KickAss",
    "bitsearch": "Bitsearch",
    "glodls": "Glodls",
    "magnetdl": "MagnetDL",
    "limetorrent": "LimeTorrent",
    "torrentfunk": "TorrentFunk",
    "torrentproject": "TorrentProject",
    "all": "All"
}
SEARCH_LIMIT = 200

# Define helper functions
def button_builder(user_id, data, tool):
    buttons = button_build.ButtonMaker()
    if tool == 'api':
        for name, site in SITES.items():
            buttons.sbutton(site, f"torser {user_id} {name} {tool}")
    else:
        buttons.sbutton('All', f"torser {user_id} all {tool}")
        if not PLUGINS:
            qbclient = get_client()
            pl = qbclient.search_plugins()
            for name in pl:
                PLUGINS.append(name['name'])
            qbclient.auth_log_out()
        for siteName in PLUGINS:
            buttons.sbutton(siteName.capitalize(), f"torser {user_id} {siteName} {tool}")
    buttons.sbutton("Cancel", f"torser {user_id} cancel")
    button = InlineKeyboardMarkup(buttons.build_menu(2))
    return button

def torser(update, context):
    user_id = update.message.from_user.id
    try:
        key = update.message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return sendMessage("Send a search key along with command", context.bot, update)
    if SEARCH_API_LINK is not None and SEARCH_PLUGINS is not None:
        buttons = button_builder(user_id, 'api', 'api')
        sendMarkup('Choose tool to search:', context.bot, update, buttons)
    elif SEARCH_API_LINK is not None and SEARCH_PLUGINS is None:
        buttons = button_builder(user_id, 'api', 'api')
        sendMarkup('Choose site to search:', context.bot, update, buttons)
    elif SEARCH_API_LINK is None and SEARCH_PLUGINS is not None:
        buttons = button_builder(user_id, 'plugin', 'plugin')
        sendMarkup('Choose site to search:', context.bot, update, buttons)
    else:
        return sendMessage("No API link or search PLUGINS added for this function", context.bot, update)

def torserbut(update: CallbackQuery, context: CallbackContext):
    query = update
    user_id = query.from_user.id
    message = query.message
    key = message.reply_to_message.text.split(" ", maxsplit=1)[1]
    data = query.data
    data = data.split(" ")
    if user_id != int(data[1]):
        query.answer(text="Not Yours!", show_alert=True)
    elif data[2] == 'api':
        query.answer()
        buttons = button_builder(user_id, data[2], data[2])
        editMessage('Choose site to search:', message, buttons)
    elif data[2] == 'plugin':

