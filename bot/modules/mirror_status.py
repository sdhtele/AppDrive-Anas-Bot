from psutil import cpu_percent, virtual_memory, disk_usage  # Import necessary modules for system resource usage
from time import time  # Import time module for calculating uptime
from threading import Thread  # Import threading module for asynchronous message deletion
from telegram.ext import CommandHandler, CallbackQueryHandler  # Import necessary modules for Telegram bot handlers

# Import various utility functions from the bot module
from bot import dispatcher, status_reply_dict, status_reply_dict_lock, download_dict, download_dict_lock, botStartTime
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, auto_delete_message, sendStatusMessage, update_all_messages
from bot.helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time  # Import functions for formatting file sizes and time
from bot.helper.telegram_helper.filters import CustomFilters  # Import custom filters for the bot
from bot.helper.telegram_helper.bot_commands import BotCommands  # Import bot commands

def mirror_status(update, context):
    """
    This function sends the current system status and clears any existing status messages.
    """
    with download_dict_lock:
        # Check if there are any active downloads
        if len(download_dict) == 0:
            currentTime = get_readable_time(time() - botStartTime)
            total, used, free, _ = disk_usage('.')
            free = get_readable_file_size(free)
            message = 'No Active Downloads !\n___________________________'
            message += f"\n<b>CPU:</b> {cpu_percent()}% | <b>FREE:</b> {free}" \
                       f"\n<b>RAM:</b> {virtual_memory().percent}% | <b>UPTIME:</b> {currentTime}"
            reply_message = sendMessage(message, context.bot, update)
            # Start a new thread to automatically delete the reply message after some time
            Thread(target=auto_delete_message, args=(context.bot, update.message, reply_message)).start()
            return

    index = update.effective_chat.id
    with status_reply_dict_lock:
        # Delete any existing status message for the current chat
        if index in status_reply_dict.keys():
            deleteMessage(context.bot, status_reply_dict[index])
            del status_reply_dict[index]

    # Send the current system status and update the status_reply_dict
    sendStatusMessage(update, context.bot)
    deleteMessage(context.bot, update.message)

def status_pages(update, context):
    """
    This function handles callback queries for navigating through status pages.
    """
    query = update.callback_query
    data = query.data
    data = data.split(' ')
    query.answer()  # Answer the callback query to remove the loading state
    done = turn(data)  # Update the status pages and return True if all pages have been shown
    if done:
        # If all pages have been shown, update all messages
        update_all_messages()
    else:
        # If not all pages have been shown, delete the current message
        query.message.delete()

# Create handlers for the mirror_status and status_pages functions
mirror_status_handler = CommandHandler(BotCommands.StatusCommand, mirror_status,
                                       filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

status_pages_handler = CallbackQueryHandler(status_pages, pattern="status", run_async=True)

# Add the handlers to the dispatcher
dispatcher.add_handler(mirror_status_handler)
dispatcher.add_handler(status_pages_handler)
