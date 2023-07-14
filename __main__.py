from configparser import ConfigParser
import sys
import os
from datetime import datetime
import time
from getpass import getuser
import json
from loguru import logger

# Get username
USER: str = getuser()

LOG_FILE: str = f"/home/{USER}/.debug_styles.log"
CONFIG_FILE: str = f"/home/{USER}/.config/Styles/config.ini"

# Visual Studio Code
VSCODE_SETTINGS: str = f"/home/{USER}/.config/Code/User/settings.json"
VSCODE_LIGHT: str = "Default Light Modern"
VSCODE_DARK: str = "Visual Studio Dark"

# Sublime Text
SUBLIME_TEXT_SETTINGS: str = f"/home/{USER}/.config/sublime-text/Packages/User/Preferences.sublime-settings"

SUBLIME_TEXT_LIGHT: str = "Default.sublime-theme"
SUBLIME_TEXT_LIGHT_SYNTAX: str = "Breakers.sublime-color-scheme"

SUBLIME_TEXT_DARK: str = "Default Dark.sublime-theme"
SUBLIME_TEXT_DARK_SYNTAX: str = "Monokai.sublime-color-scheme"


class ChangingThemes:
    def __init__(self) -> None:
        # Logger init
        logger.add(LOG_FILE, rotation="1024 KB", compression="zip")

        logger.debug("Launching the application...")

        # Created file 'config.ini'
        try:
            os.mkdir(f"/home/{USER}/.config/Styles")
            with open(CONFIG_FILE, "w") as file:
                file.write("[settings]\ntime1=08:00:00.000000\ntime2=20:00:00.000000")
            logger.debug("File 'config.ini' created!\n")

        # File 'config.ini' not exists
        except FileExistsError as e:
            logger.error(str(e))

        # Config file
        self.config: ConfigParser = ConfigParser()
        self.config.read(CONFIG_FILE)

        time1: str = self.config["settings"]["time1"]
        time2: str = self.config["settings"]["time2"]

        self._set_themes(time1, time2)

    @logger.catch
    def _set_themes(self, time1, time2) -> None:
        """ Changing the theme """
        while True:
            # Today date
            date: str = str(datetime.today())
            date: list = date.split(" ")

            # Current theme
            theme: str = os.popen("gsettings get org.gnome.desktop.interface color-scheme").read().replace("'", "")

            # Set light theme
            if time1 < date[1] < time2:
                if theme == "prefer-dark\n":
                    # System
                    os.system("gsettings set org.gnome.desktop.interface color-scheme 'default'")

                    # Visual Studio Code
                    self._set_vscode_theme(theme=VSCODE_LIGHT)

                    # Sublime Text
                    self._set_sublime_text_theme(theme=SUBLIME_TEXT_DARK, theme_syntax=SUBLIME_TEXT_DARK_SYNTAX)

                    logger.debug("Theme: light\n")

            # Set dark theme
            if time1 >= date[1] or date[1] >= time2:
                if theme == "default\n":
                    # System
                    os.system("gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'")

                    # Visual Studio Code
                    self._set_vscode_theme(theme=VSCODE_DARK)

                    # Sublime Text
                    self._set_sublime_text_theme(theme=SUBLIME_TEXT_DARK, theme_syntax=SUBLIME_TEXT_DARK_SYNTAX)

                    logger.debug("Theme: dark\n")

            try:
                time.sleep(5)
            except KeyboardInterrupt:
                logger.info("Shutting down the application")
                sys.exit(0)

    @logger.catch
    def _set_vscode_theme(self, theme: str) -> None:
        """ Changing the theme in VSCode """

        # Does the file exist
        if os.path.isfile(VSCODE_SETTINGS):
            with open(file=VSCODE_SETTINGS, mode="w", encoding="UTF-8") as file:
                json.dump({"workbench.startupEditor": "none",
                           "security.workspace.trust.untrustedFiles": "open",
                           "editor.unicodeHighlight.nonBasicASCII": "false",
                           "editor.largeFileOptimizations": "false",
                           "editor.minimap.enabled": "false",
                           "workbench.colorTheme": theme
                           }, file)
            logger.debug("VSCode set theme: " + theme)
        else:
            logger.error(f"File {VSCODE_SETTINGS} not found!")

    @logger.catch
    def _set_sublime_text_theme(self, theme: str, theme_syntax) -> None:
        """ Changing the theme in Sublime Text """

        # Does the file exist
        if os.path.isfile(SUBLIME_TEXT_SETTINGS):
            with open(file=SUBLIME_TEXT_SETTINGS, mode="w", encoding="UTF-8") as file:
                json.dump({"class": "sidebar_label",
                           "font_face": "Liberation Mono",
                           "font.size": 14,
                           "color": [205, 92, 92, 255],
                           "theme": theme,
                           "color_scheme": theme_syntax,
                           "font_size": 10,
                           "ignored_packages":
                               [
                                   "Vintage",
                               ], }, file)
            logger.debug("Sublime Text set theme: " + theme)
            logger.debug("Sublime Text set theme_syntax: " + theme_syntax)
        else:
            logger.error(f"File {SUBLIME_TEXT_SETTINGS} not found!")


if __name__ == "__main__":
    style: ChangingThemes = ChangingThemes()
