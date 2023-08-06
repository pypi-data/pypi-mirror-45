from colorama import init, Fore, Back, Style


class Logger(object):
    """
    Class to log styled messages to stdout.
    """

    def __init__(self):
        init()
        self._error_tag = ''
        self._info_tag = ''
        self._warn_tag = ''
        self._confirm_tag = ''
        self._norm_tag = ''

    def print_error(self, message, tag=None, bold=False, highlight=False, invert_color=False):
        """
        Prints a message to stdout with error style (red ANSI color)

        Args:
            message (str): Message to print.
            tag (str): Prefix to print with the message. If `None` the default.
                tag for this kind of messages is used. An empty string will remove
                the tag for this print.
            bold (bool): `True` to use bright style to print the message (kind of bold font).
                By default `False`.
            highlight (bool): `True` to use the color on the background and a high contrast
                color for the message text.
            invert_color (bool): `True` to invert font color when highlight flag is on, this will
                switch between black and white. By default `False`. Hightlight font color white
        """
        if tag is None:
            tag = self._error_tag

        style = Style.BRIGHT if bold else Style.NORMAL
        if highlight:
            style += "{}{}".format(Back.RED, Fore.WHITE if not invert_color and bold else Fore.BLACK)

        else:
            style += Fore.RED

        print("{}{}{}{}".format(style, tag, message, Style.RESET_ALL))

    def print_warn(self, message, tag=None, bold=False, highlight=False, invert_color=False):
        """
        Prints a message to stdout with warning style (yellow ANSI color)

        Args:
            message (str): Message to print.
            tag (str): Prefix to print with the message. If `None` the default.
                tag for this kind of messages is used. An empty string will remove
                the tag for this print.
            bold (bool): `True` to use bright style to print the message (kind of bold font).
                By default `False`.
            highlight (bool): `True` to use the color on the background and a high contrast
                color for the message text.
            invert_color (bool): `True` to invert font color when highlight flag is on, this will
                switch between black and white. By default `False`. Hightlight font color white.
        """
        if tag is None:
            tag = self._warn_tag

        style = Style.BRIGHT if bold else Style.NORMAL
        if highlight:
            style += "{}{}".format(Back.YELLOW, Fore.WHITE if not invert_color and bold else Fore.BLACK)

        else:
            style += Fore.YELLOW

        print("{}{}{}{}".format(style, tag, message, Style.RESET_ALL))

    def print_info(self, message, tag=None, bold=False, highlight=False, invert_color=False):
        """
        Prints a message to stdout with information style (cyan ANSI color)

        Args:
            message (str): Message to print.
            tag (str): Prefix to print with the message. If `None` the default.
                tag for this kind of messages is used. An empty string will remove
                the tag for this print.
            bold (bool): `True` to use bright style to print the message (kind of bold font).
                By default `False`.
            highlight (bool): `True` to use the color on the background and a high contrast
                color for the message text.
            invert_color (bool): `True` to invert font color when highlight flag is on, this will
                switch between black and white. By default `False`. Hightlight font color white.
        """
        if tag is None:
            tag = self._info_tag

        style = Style.BRIGHT if bold else Style.NORMAL
        if highlight:
            style += "{}{}".format(Back.CYAN, Fore.WHITE if not invert_color and bold else Fore.BLACK)

        else:
            style += Fore.CYAN

        print("{}{}{}{}".format(style, tag, message, Style.RESET_ALL))

    def print_confirm(self, message, tag=None, bold=False, highlight=False, invert_color=False):
        """
        Prints a message to stdout with confirmation style (green ANSI color)

        Args:
            message (str): Message to print.
            tag (str): Prefix to print with the message. If `None` the default.
                tag for this kind of messages is used. An empty string will remove
                the tag for this print.
            bold (bool): `True` to use bright style to print the message (kind of bold font).
                By default `False`.
            highlight (bool): `True` to use the color on the background and a high contrast
                color for the message text.
            invert_color (bool): `True` to invert font color when highlight flag is on, this will
                switch between black and white. By default `False`. Hightlight font color white.
        """
        if tag is None:
            tag = self._confirm_tag

        style = Style.BRIGHT if bold else Style.NORMAL
        if highlight:
            style += "{}{}".format(Back.GREEN, Fore.WHITE if not invert_color and bold else Fore.BLACK)

        else:
            style += Fore.GREEN

        print("{}{}{}{}".format(style, tag, message, Style.RESET_ALL))

    def print_norm(self, message, tag=None, bold=False, highlight=False, invert_color=False):
        """
        Prints a message to stdout in with black and wihte palette.

        Args:
            message (str): Message to print.
            tag (str): Prefix to print with the message. If `None` the default.
                tag for this kind of messages is used. An empty string will remove
                the tag for this print.
            bold (bool): `True` to use bright style to print the message (kind of bold font).
                By default `False`.
            highlight (bool): `True` to use the color on the background and a high contrast
                color for the message text.
            invert_color (bool): `True` to invert font color when highlight flag is on, this will
                switch between black and white. By default `False`. Hightlight font color white.
        """
        if tag is None:
            tag = self._norm_tag

        style = Style.BRIGHT if bold else Style.NORMAL
        if highlight:
            style += "{}{}".format(Back.WHITE, Fore.BLACK if not invert_color else Fore.WHITE)

        else:
            style += Fore.WHITE

        print("{}{}{}{}".format(style, tag, message, Style.RESET_ALL))

    @property
    def error_tag(self):
        """
        Default error messages tag
        """
        return self._error_tag

    @error_tag.setter
    def error_tag(self, new_tag):
        self._error_tag = str(new_tag)

    @property
    def warn_tag(self):
        """
        Default warning messages tag
        """
        return self._warn_tag

    @warn_tag.setter
    def warn_tag(self, new_tag):
        self._warn_tag = str(new_tag)

    @property
    def info_tag(self):
        """
        Default info messages tag
        """
        return self._info_tag

    @info_tag.setter
    def info_tag(self, new_tag):
        self._info_tag = str(new_tag)

    @property
    def confirm_tag(self):
        """
        Default confirmation messages tag
        """
        return self._confirm_tag

    @confirm_tag.setter
    def confirm_tag(self, new_tag):
        self._confirm_tag = str(new_tag)

    @property
    def norm_tag(self):
        """
        Default standard messages tag
        """
        return self._norm_tag

    @norm_tag.setter
    def norm_tag(self, new_tag):
        self._norm_tag = str(new_tag)
