# Leech Settings V2 Implement By - @VarnaX-279

import os
from os import remove as osremove, path as ospath, mkdir
from threading import Thread
from PIL import Image
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup

# Import necessary modules from the bot package
from bot import AS_DOC_USERS, AS_MEDIA_USERS, dispatcher, AS_DOCUMENT, app, AUTO_DELETE_MESSAGE_DURATION, DB_URI
from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage, auto_delete_message
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper import button_build
from bot.helper.ext_utils.db_handler import DbManger

def getleechinfo(from_user):
    """Generate leech settings information for a given user."""
    user_id = from_user.id
    name = from_user.full_name
    buttons = button_build.ButtonMaker()

    # Define the thumbnail path
    thumbpath = f"Thumbnails/{user_id}.jpg"

    # Set leech type and available options based on user's current settings
    if (
        user_id in AS_DOC_USERS
        or user_id not in AS_MEDIA_USERS
        and AS_DOCUMENT
    ):
        ltype = "DOCUMENT"
        buttons.sbutton("Send As Media", f"leechset {user_id} med")
    else:
        ltype = "MEDIA"
        buttons.sbutton("Send As Document", f"leechset {user_id} doc")

    # Check if the thumbnail exists and create corresponding options
    if ospath.exists(thumbpath):
        thumbmsg = "Exists"
        buttons.sbutton("Delete Thumbnail", f"leechset {user_id} thumb")
    else:
        thumbmsg = "Not Exists"

    # Add a "Close" button if the auto-delete duration is not set
    if AUTO_DELETE_MESSAGE_DURATION == -1:
        buttons.sbutton("Close", f"leechset {user_id} close")

    # Create the InlineKeyboardMarkup with the buttons
    button = InlineKeyboardMarkup(buttons.build_menu(1))

    # Generate the message text
    text = f"<u>Leech Settings for <a href='tg://user?id={user_id}'>{name}</a></u>\n"\
           f"Leech Type <b>{ltype}</b>\n"\
           f"Custom Thumbnail <b>{thumbmsg}</b>"
    return text, button

def editLeechType(message, query):
    """Edit the leech settings type for a user."""
    msg, button = getleechinfo(query.from_user)
    editMessage(msg, message, button)

def leechSet(update, context):
    """Display the leech settings for a user."""
    msg, button = getleechinfo(update.message.from_user)
    choose_msg = sendMarkup(msg, context.bot, update, button)
    # Start a new thread to auto-delete the message after a certain duration
    Thread(target=auto_delete_message, args=(context.bot, update.message, choose_msg)).start()

def setLeechType(update, context):
    """Update the leech settings for a user based on the user's selection."""
    query = update.callback_query
    message = query.message
    user_id = query.from_user.id
    data = query.data
    data = data.split(" ")

    # Check if the user is authorized to make changes and if the user ID matches
    if user_id != int(data[1]):
        query.answer(text="Not Yours!", show_alert=True)
    else:
        # Update the leech type based on the user's selection
        if data[2] == "doc":
            if user_id in AS_MEDIA_USERS:
                AS_MEDIA_USERS.remove(user_id)
            AS_DOC_USERS.add(user_id)
            if DB_URI is not None:
                DbManger().user_doc(user_id)
            query.answer(text="Your File Will Deliver As Document!", show_alert=True)
            editLeechType(message, query)
        elif data[2] == "med":
            if user_id in AS_DOC_USERS:
                AS_DOC_USERS.remove(user_id)
            AS_MEDIA_USERS.add(user_id)
            if DB_URI is not None:
                DbManger().user_media(user_id)
            query.answer(text="Your File Will Deliver As Media!", show_alert=True)
            editLeechType(message, query)
        elif data[2] == "thumb":
            path = f"Thumbnails/{user_id}.jpg"
            # Remove the thumbnail if it exists
            if ospath.lexists(path):
                osremove(path)
                if DB_URI is not None:
                    DbManger().user_rm_thumb(user_id, path)
                query.answer(text="Thumbnail Removed!", show_alert=True)
                editLeechType(message, query)
            else:
                query.answer(text="Old Settings", show_alert=True)
        elif data[2] == "close":
            # Close the message and the reply message if they exist
            try:
                query.message.delete()
                query.message.reply_to_message.delete()
            except:
                pass

def setThumb(update, context):
    """Save a custom thumbnail for a user."""
    user_id = update.message.from_user.id
    reply_to
