from telegram import InlineKeyboardButton

class ButtonMaker:
    """
    This class is used to create and manage a list of InlineKeyboardButton objects,
    which can then be easily arranged into a grid-like structure (an InlineKeyboardMarkup)
    and added to a message in the Telegram API.
    """

    def __init__(self):
        """
        Initialize an empty list of buttons.
        """
        self.button = []

    def buildbutton(self, key, link):
        """
        Add a new InlineKeyboardButton to the list with the specified key text and URL.

        :param key: The text to display on the button
        :param link: The URL to link the button to
        """
        self.button.append(InlineKeyboardButton(text=key, url=link))

    def sbutton(self, key, data):
        """
        Add a new InlineKeyboardButton to the list with the specified key text and callback data.

        :param key: The text to display on the button
        :param data: The callback data to associate with the button
        """
        self.button.append(InlineKeyboardButton(text=key, callback_data=data))

    def build_menu(self, n_cols, footer_buttons=None, header_buttons=None):
        """
        Arrange the current list of buttons into a grid with the specified number of columns.
        Optionally, add a list of buttons to the top (header) and/or bottom (footer) of the menu.

        :param n_cols: The number of columns in the grid
        :param footer_buttons: An optional list of buttons to add to the bottom of the menu
        :param header_buttons: An optional list of buttons to add to the top of the menu
        :return: A list of rows, where each row is a list of buttons
        """
        menu = [self.button[i:i + n_cols] for i in range(0, len(self.button), n_cols)]

        # Add the optional header and foot
