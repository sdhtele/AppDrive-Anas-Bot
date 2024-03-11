# watch function initiates the downloading process and presents the user with a list of available qualities and formats
def _watch(bot, update, isZip=False, isLeech=False, pswd=None, tag=None):

# _qual_subbuttons function generates inline buttons for different bitrates of a specific video quality
def _qual_subbuttons(task_id, qual, msg):

# _audio_subbuttons function generates inline buttons for different audio bitrates, with an optional playlist parameter to handle playlists
def _audio_subbuttons(task_id, msg, playlist=False):

# select_format function is a callback function for the inline buttons. It handles user selections and initiates the downloading process based on the user's choice
def select_format(update, context):

# _auto_cancel function is a utility function that cancels the downloading process if it takes too long
def _auto_cancel(msg, msg_id):

# watch function is a command handler for initiating the downloading process without zip or leech options
def watch(update, context):

# watchZip function is a command handler for initiating the downloading process with zip option
def watchZip(update, context):

# leechWatch function is a command handler for initiating the downloading process with leech option
def leechWatch(update, context):

# leechWatchZip function is a command handler for initiating the downloading process with zip and leech options
def leechWatchZip(update, context):
