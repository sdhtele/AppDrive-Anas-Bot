import os
# Importing required modules and functions from os, os.path, getcwd, chdir,
# traceback, textwrap, io, telegram, telegram.ext, contextlib, bot.helper.telegram_helper.filters,
# bot.helper.telegram_helper.bot_commands, bot.helper.telegram_helper.message_utils, and bot

from os import path as ospath, getcwd, chdir
from traceback import format_exc
from textwrap import indent
from io import StringIO, BytesIO
from telegram import ParseMode
from telegram.ext import CommandHandler
from contextlib import redirect_stdout

from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage
from bot import LOGGER, dispatcher

# Defining an empty dictionary 'namespaces' to store the required environment for each chat
namespaces = {}

def namespace_of(chat, update, bot):
    # A function to create and return the required environment for a chat
    if chat not in namespaces:
        # If the environment for the chat doesn't exist, create a new one
        namespaces[chat] = {
            '__builtins__': globals()['__builtins__'],
            'bot': bot,
            'effective_message': update.effective_message,
            'effective_user': update.effective_user,
            'effective_chat': update.effective_chat,
            'update': update
        }

    return namespaces[chat]
# End of namespace_of function

def log_input(update):
    # A function to log the input message
    user = update.effective_user.id
    chat = update.effective_chat.id
    LOGGER.info(
        f"IN: {update.effective_message.text} (user={user}, chat={chat})")
# End of log_input function

def send(msg, bot, update):
    # A function to send the output message
    if len(str(msg)) > 2000:
        # If the message length is greater than 2000, send it as a document
        with BytesIO(str.encode(msg)) as out_file:
            out_file.name = "output.txt"
            bot.send_document(
                chat_id=update.effective_chat.id, document=out_file)
    else:
        # Otherwise, send it as a message
        LOGGER.info(f"OUT: '{msg}'")
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"`{msg}`",
            parse_mode=ParseMode.MARKDOWN)
# End of send function

def evaluate(update, context):
    # A function to evaluate the given Python code
    bot = context.bot
    send(do(eval, bot, update), bot, update)
# End of evaluate function

def execute(update, context):
    # A function to execute the given commands
    bot = context.bot
    send(do(exec, bot, update), bot, update)
# End of execute function

def cleanup_code(code):
    # A function to clean up the given code
    if code.startswith('```') and code.endswith('```'):
        # If the code is in triple backticks, remove the triple backticks
        return '\n'.join(code.split('\n')[1:-1])
    return code.strip('` \n')
# End of cleanup_code function

def do(func, bot, update):
    # A function to perform the required action with the given function
    log_input(update)
    content = update.message.text.split(' ', 1)[-1]
    body = cleanup_code(content)
    env = namespace_of(update.message.chat_id, update, bot)

    chdir(getcwd())
    with open(
            ospath.join(getcwd(),
                         'bot/modules/temp.txt'),
            'w') as temp:
        # Writing the cleaned up code to a temporary file
        temp.write(body)

    stdout = StringIO()

    to_compile = f'def func():\n{indent(body, "  ")}'

    try:
        # Compiling and executing the code in a new environment
        exec(to_compile, env)
    except Exception as e:
        # If there is an error, return the error message
        return f'{e.__class__.__name__}: {e}'

    func = env['func']

    try:
        # Executing the function and capturing the output
        with redirect_stdout(stdout):
            func_return = func()
    except Exception as e:
        # If there is an error, return the error message
        value = stdout.getvalue()
        return f'{value}{format_exc()}'
    else:
        # If the function returns a value, add it to the output
        value = stdout.getvalue()
        result = None
        if func_return is None:
            if value:
                result = f'{value}'
            else:
                try:
                    # If the function doesn't return a value, try to evaluate the code
                    result = f'{repr(eval(body, env))}'
                except:
                    pass
        else:
            # If the function returns a value, add it to the output
            result = f'{value}{func_return}'
        if result:
            return result
# End of do function

def clear(update, context):
    # A function to clear the environment for the given chat
    bot = context.bot
    log_input(update)
    global namespaces
    if update.message.chat_id in namespaces:
        # If the environment exists, delete it
        del namespaces[update.message.chat_id]
    send("Cleared locals.", bot, update)
# End of clear function

def exechelp(update, context):
    # A function to show the help message for the executor
    help
