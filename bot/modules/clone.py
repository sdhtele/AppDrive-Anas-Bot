@new_thread  # Decorator to run the function in a new thread
def cloneNode(update, context):
    # Extract the link from the user message
    args = update.message.text.split(" ", maxsplit=1)
    reply_to = update.message.reply_to_message
    link = ''
    if len(args) > 1:
        link = args[1]
    elif reply_to is not None:
        if len(link) == 0:
            link = reply_to.text
    # Check if the link is a GDrive link, GDtot link, DriveApp link, or AppDrive link
    is_gdtot = is_gdtot_link(link)
    is_driveapp = 'driveapp.in' in link
    is_appdrive = 'appdrive.in' in link

    # Process the link based on its type
    if is_driveapp:
        # ... (code for DriveApp link processing)
    if is_appdrive:
        # ... (code for AppDrive link processing)
    if is_gdtot:
        # ... (code for GDtot link processing)

    # Process the GDrive link
    if is_gdrive_link(link):
        # Initialize GoogleDriveHelper()
        gd = GoogleDriveHelper()
        # Helper function to get file information from the GDrive link
        res, size, name, files = gd.helper(link)
        if res != "":
            # If an error occurs, send the error message
            return sendMessage(res, context.bot, update)

        # Check for duplicates and size limitations
        if STOP_DUPLICATE:
            LOGGER.info('Checking File/Folder if already in Drive...')
            # ... (code for checking duplicates)
        if CLONE_LIMIT is not None:
            LOGGER.info('Checking File/Folder Size...')
            # ... (code for checking size limitations)

        # If the file/folder has less than or equal to 20 files
        if files <= 20:
            msg = sendMessage(f"Cloning: <code>{link}</code>", context.bot, update)
            # Clone the file/folder
            result, button = gd.clone(link)
            deleteMessage(context.bot, msg)
        else:
            # ... (code for handling large file/folders)

        # Send the result message with the appropriate message or markup
        cc = f'\n\n<b>cc: </b>{tag}'
        if button in ["cancelled", ""]:
            sendMessage(f"{tag} {result}", context.bot, update)
        else:
            sendMarkup(result + cc, context.bot, update, button)

        # Delete the temporary file if it was a GDtot, DriveApp, or AppDrive link
        if is_gdtot:
            gd.deletefile(link)
        if is_driveapp:
            gd.deletefile(link)
        if is_appdrive:
            gd.deletefile(link)
    else:
        # If the link is not a valid GDrive link, send an error message
        sendMessage('Send Gdrive or GDrive Sites link along with command or by replying to the link by command', context.bot, update)
