from time import sleep # Import sleep function from time module
from telegram import InlineKeyboardMarkup, Message, Update # Import necessary classes from telegram module
from telegram.error import RetryAfter # Import RetryAfter exception
from pyrogram.errors import FloodWait # Import FloodWait exception

from bot import AUTO_DELETE_MESSAGE_DURATION, LOGGER, status_reply_dict, status_reply_dict_lock, Interval, DOWNLOAD_STATUS_UPDATE_INTERVAL, RSS_CHAT_ID, rss_session, bot # Import required variables and objects from bot module

def sendMessage(text: str, bot, update: Update):
    """
    Send a message to the chat where the update came from.

    Args:
    text (str): The text of the message to be sent.
    bot: The bot object used to send the message.
    update: The update object containing information about the incoming update.

    Returns:
    Message: The message object representing the sent message.
    """
    try:
        # Send the message using the bot object
        return bot.send_message(update.message.chat_id,
                            reply_to_message_id=update.message.message_id,
                            text=text, allow_sending_without_reply=True, parse_mode='HTMl', disable_web_page_preview=True)
    except RetryAfter as r:
        # If a RetryAfter exception is raised, log the warning and sleep for the specified time
        LOGGER.warning(str(r))
        sleep(r.retry_after * 1.5)
        return sendMessage(text, bot, update)
    except Exception as e:
        # If any other exception is raised, log the error
        LOGGER.error(str(e))
        return

def sendMarkup(text: str, bot, update: Update, reply_markup: InlineKeyboardMarkup):
    """
    Send a message with a custom keyboard to the chat where the update came from.

    Args:
    text (str): The text of the message to be sent.
    bot: The bot object used to send the message.
    update: The update object containing information about the incoming update.
    reply_markup: The InlineKeyboardMarkup object representing the custom keyboard.

    Returns:
    Message: The message object representing the sent message.
    """
    try:
        # Send the message with the custom keyboard using the bot object
        return bot.send_message(update.message.chat_id,
                            reply_to_message_id=update.message.message_id,
                            text=text, reply_markup=reply_markup, allow_sending_without_reply=True,
                            parse_mode='HTMl', disable_web_page_preview=True)
    except RetryAfter as r:
        # If a RetryAfter exception is raised, log the warning and sleep for the specified time
        LOGGER.warning(str(r))
        sleep(r.retry_after * 1.5)
        return sendMarkup(text, bot, update, reply_markup)
    except Exception as e:
        # If any other exception is raised, log the error
        LOGGER.error(str(e))
        return

def editMessage(text: str, message: Message, reply_markup=None):
    """
    Edit an existing message in the chat.

    Args:
    text (str): The new text of the message.
    message: The Message object representing the message to be edited.
    reply_markup: The InlineKeyboardMarkup object representing the new custom keyboard (optional).

    Returns:
    None
    """
    try:
        # Edit the message using the bot object
        bot.edit_message_text(text=text, message_id=message.message_id,
                              chat_id=message.chat.id,reply_markup=reply_markup,
                              parse_mode='HTMl', disable_web_page_preview=True)
    except RetryAfter as r:
        # If a RetryAfter exception is raised, log the warning and sleep for the specified time
        LOGGER.warning(str(r))
        sleep(r.retry_after * 1.5)
        return editMessage(text, message, reply_markup)
    except Exception as e:
        # If any other exception is raised, log the error
        LOGGER.error(str(e))
        return

def sendRss(text: str, bot):
    """
    Send a message to the RSS_CHAT_ID with the specified text.

    Args:
    text (str): The text of the message to be sent.
    bot: The bot object used to send the message.

    Returns:
    Message: The message object representing the sent message.
    """
    if rss_session is None:
        # If rss_session is None, send the message using the bot object
        try:
            return bot.send_message(RSS_CHAT_ID, text, parse_mode='HTMl', disable_web_page_preview=True)
        except RetryAfter as r:
            # If a RetryAfter exception is raised, log the warning and sleep for the specified time
            LOGGER.warning(str(r))
            sleep(r.retry_after * 1.5)
            return sendRss(text, bot)
        except Exception as e:
            # If any other exception is raised, log the error
            LOGGER.error(str(e))
            return
    else:
        # If rss_session is not None, send the message using the rss_session object
        try:
            return rss_session.send_message(RSS_CHAT_ID, text, parse_mode='HTMl', disable_web_page_preview=True)
        except FloodWait as e:
            # If a FloodWait exception is raised, log the warning and sleep for the specified time
            LOGGER.warning(str(e))
            sleep(e.x * 1.5)
            return sendRss(text, bot)
        except Exception as e:
            # If any other exception is raised, log the error
            LOGGER.error(str(e))
            return

