from subprocess import run  # Import run function from subprocess module
from telegram import ParseMode  # Import ParseMode from telegram module
from telegram.ext import CommandHandler  # Import CommandHandler from telegram.ext module

from bot import LOGGER, dispatcher  # Import LOGGER and dispatcher from bot.py
from bot.helper.telegram_helper.filters import CustomFilters  # Import CustomFilters from bot.helper.telegram_helper.filters
from bot.helper.telegram_helper.bot_commands import BotCommands  # Import BotCommands from bot.helper.telegram_helper.bot_commands
from bot.helper.telegram_helper.message_utils import sendMessage  # Import sendMessage from bot.helper.telegram_helper.message_utils


def shell(update, context):
    message = update.effective_message
    cmd = message.text.split(' ', 1)
    if len(cmd) == 1:
        return sendMessage('No command to execute was given.', context.bot, update)
    cmd = cmd[1]
    process = run(cmd, capture_output=True, shell=True)
    # ...


    reply = ''
    stderr = process.stderr.decode('utf-8')
    stdout = process.stdout.decode('utf-8')
    if len(stdout) != 0:
        reply += f"*Stdout*\n<code>{stdout}</code>\n"
        LOGGER.info(f"Shell - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"*Stderr*\n<code>{stderr}</code>\n"
        LOGGER.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        # ...
    elif len(reply) != 0:
        sendMessage(reply, context.bot, update)
    else:
        sendMessage('No Reply', context.bot, update)


SHELL_HANDLER = CommandHandler(BotCommands.ShellCommand, shell,
                                                  filters=CustomFilters.owner_filter,
