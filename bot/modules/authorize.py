from bot import AUTHORIZED_CHATS, SUDO_USERS, dispatcher, DB_URI  # Import required modules and variables
from bot.helper.telegram_helper.message_utils import sendMessage  # Import sendMessage function
from telegram.ext import CommandHandler  # Import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters  # Import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands  # Import BotCommands
from bot.helper.ext_utils.db_handler import DbManger  # Import DbManger

def authorize(update, context):
    """
    Function to authorize a user or a chat in the bot.
    """
    reply_message = None
    message_ = None
    reply_message = update.message.reply_to_message  # Get the replied message, if any
    message_ = update.message.text.split(' ')  # Split the message into a list

    if len(message_) == 2:
        user_id = int(message_[1])  # Get the user ID from the message

        if user_id in AUTHORIZED_CHATS:  # Check if the user is already authorized
            msg = 'User Already Authorized!'
        elif DB_URI is not None:  # If DB_URI is not None, use the database to authorize the user
            msg = DbManger().user_auth(user_id)
            AUTHORIZED_CHATS.add(user_id)
        else:
            AUTHORIZED_CHATS.add(user_id)  # Otherwise, add the user to the AUTHORIZED_CHATS set
            with open('authorized_chats.txt', 'a') as file:
                file.write(f'{user_id}\n')  # Write the user ID to the authorized_chats.txt file
                msg = 'User Authorized'
    elif reply_message is None:
        # Trying to authorize a chat
        chat_id = update.effective_chat.id  # Get the chat ID

        if chat_id in AUTHORIZED_CHATS:  # Check if the chat is already authorized
            msg = 'Chat Already Authorized!'
        elif DB_URI is not None:  # If DB_URI is not None, use the database to authorize the chat
            msg = DbManger().user_auth(chat_id)
            AUTHORIZED_CHATS.add(chat_id)
        else:
            AUTHORIZED_CHATS.add(chat_id)  # Otherwise, add the chat to the AUTHORIZED_CHATS set
            with open('authorized_chats.txt', 'a') as file:
                file.write(f'{chat_id}\n')  # Write the chat ID to the authorized_chats.txt file
                msg = 'Chat Authorized'
    else:
        # Trying to authorize someone by replying
        user_id = reply_message.from_user.id  # Get the user ID from the replied message

        if user_id in AUTHORIZED_CHATS:  # Check if the user is already authorized
            msg = 'User Already Authorized!'
        elif DB_URI is not None:  # If DB_URI is not None, use the database to authorize the user
            msg = DbManger().user_auth(user_id)
            AUTHORIZED_CHATS.add(user_id)
        else:
            AUTHORIZED_CHATS.add(user_id)  # Otherwise, add the user to the AUTHORIZED_CHATS set
            with open('authorized_chats.txt', 'a') as file:
                file.write(f'{user_id}\n')  # Write the user ID to the authorized_chats.txt file
                msg = 'User Authorized'

    sendMessage(msg, context.bot, update)  # Send the result message

    # ... (Rest of the functions)

# ... (Rest of the code)
