from telegram.ext import CommandHandler  # Importing CommandHandler from telegram.ext

from bot import dispatcher  # Importing dispatcher from bot.helper.mirror_utils.upload_utils.gdriveTools
from bot.helper.telegram_helper.message_utils import deleteMessage, sendMessage  # Importing sendMessage and deleteMessage from bot.helper.telegram_helper.message_utils
from bot.helper.telegram_helper.filters import CustomFilters  # Importing CustomFilters from bot.helper.telegram_helper.filters
from bot.helper.telegram_helper.bot_commands import BotCommands  # Importing BotCommands from bot.helper.telegram_helper.bot_commands
from bot.helper.ext_utils.bot_utils import is_gdrive_link, is_gdtot_link, new_thread, appdrive_dl  # Importing is_gdrive_link, is_gdtot_link, new_thread, and appdrive_dl from bot.helper.ext_utils.bot_utils
from bot.helper.mirror_utils.download_utils.direct_link_generator import gdtot  # Importing gdtot from bot.helper.mirror_utils.download_utils.direct_link_generator
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException  # Importing DirectDownloadLinkException from bot.helper.ext_utils.exceptions

@new_thread  # Decorator to run the function in a new thread
def countNode(update, context):
    args = update.message.text.split(" ", maxsplit=1)  # Splitting the user's message into arguments
    reply_to = update.message.reply_to_message  # Getting the message that the user replied to
    link = ''  # Initializing the link variable
    if len(args) > 1:  # If there is more than one argument
        link = args[1]  # The second argument is the link
        if update.message.from_user.username:  # If the user has a username
            tag = f"@{update.message.from_user.username}"  # The tag is the username
        else:
            tag = update.message.from_user.mention_html(update.message.from_user.first_name)  # Otherwise, the tag is the user's first name
    elif reply_to is not None:  # If the user replied to a message
        if len(link) ==0:  # If the link is not provided in the command
            link = reply_to.text  # The link is the replied message
        if reply_to.from_user.username:  # If the user who sent the replied message has a username
            tag = f"@{reply_to.from_user.username}"  # The tag is the username
        else:
            tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)  # Otherwise, the tag is the user's first name
    gdtot_link = is_gdtot_link(link)  # Checking if the link is a Google Takeout link
    if 'driveapp.in' in link:  # If the link is an App Drive link
       is_driveapp = True
    if 'appdrive.in' in link:  # If the link is an App Drive link
       is_appdrive = True
    if is_driveapp:  # If the link is an App Drive link
        try:
            link = app
