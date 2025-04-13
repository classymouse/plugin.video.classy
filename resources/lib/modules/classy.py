# -*- coding: utf-8 -*-

'''
 ***********************************************************
 * Classy Add-on
 *
 *
 * @file classy.py
 * @package plugin.video.classy
 *
 * @copyright (c) 2025, The Crew
 * @license GNU General Public License, version 3 (GPL-3.0)
 *
 ********************************************************cm*
'''


import sys
import os
import re
import json
import platform
import base64
import datetime

import xbmc
import xbmcvfs
import xbmcaddon
import xbmcgui
import xbmcplugin

from io import open
from inspect import getframeinfo, stack


class Classy:
    def __init__(self):
        #super.__init__(self)
        self.init_vars()



    def init_vars(self):
        '''
        Initialize variables
        '''
        self.addon = xbmcaddon.Addon
        self.language = xbmcaddon.Addon().getLocalizedString
        self.addon_info = self.addon().getAddonInfo
        self.addon_id = self.addon().getAddonInfo("id")
        self.version = self.addon().getAddonInfo("version")
        self.name = self.addon().getAddonInfo('name')
        #self.name = self.strip_tags(self.name).title()
        self.path = self.addon().getAddonInfo('path')

        self.theme = self.appearance()

        self.art_path = self.get_art_path()

        self.platform = self._get_current_platform()

        self.kodiversion = self._get_kodi_version(as_string=True, as_full=True)
        self.int_kodiversion = self._get_kodi_version(as_string=False, as_full=False)

        self.icon = self.addon_icon()
        self.fanart = self.addon_fanart()

        self.devmode = self.get_setting('dev_pw') == self.ensure_text(base64.b64decode(b'Y2xhc3N5'))

        self.name = self.get_addon_name()
        self.plugfinversion = self.get_addon_version()


        self.check_vars()


    def check_vars(self):
        xbmc.log(f"[CM Debug @ 47 in classy.py] {self.name} | {self.plugfinversion} | {self.path} | {self.theme} | {self.icon} | {self.fanart} | {self.devmode}", xbmc.LOGDEBUG)




    def __del__(self):
        '''
        Destructor to clean up resources
        '''
        # Clean up resources if needed
        pass


    def lang(self, id):
        try:
            return self.language(id)
        except:
            return id

    def _get_current_platform(self):

        platform_name = platform.uname()
        _system = platform_name[0]
        # _sysname = platform_name[1]
        # _sysrelease = platform_name[2]
        _sysversion = platform_name[3]
        # _sysmachine = platform_name[4]
        # _sysprocessor = platform_name[5]
        is_64bits = sys.maxsize > 2**32
        # pf = platform.python_version() # pylint disable=snake-case

        _64bits = '64bits' if is_64bits else '32bits'

        return f"{_system} {_sysversion} ({_64bits})"

    def _get_kodi_version(self, as_string=False, as_full=False):
        version_raw = xbmc.getInfoLabel("System.BuildVersion").split(" ")

        v_temp = version_raw[0]

        if as_full is False:
            version = v_temp.split(".")[0]
            fversion = ''
        else:
            v_major = v_temp.split(".")[0]
            v_minor = v_temp.split(".")[1]
            fversion = f"{v_major}.{v_minor}"
            version = ''

        if as_string is True:
            return version if as_full is False else fversion

        return int(version)

    def log(self, msg, trace=0):
        '''
        General new log messages
        '''
        #logdebug = xbmc.LOGDEBUG
        begincolor = begininfocolor = endcolor = ''
        debug_prefix = f' DEBUG {begincolor}[{self.name} | v.{self.version}]{endcolor}' # | {self.kodiversion} | {self.platform}
        info_prefix = f' INFO {begininfocolor}[{self.name} v.{self.version}]{endcolor}'

        log_path = xbmcvfs.translatePath('special://logpath')
        filename = 'classy.log'
        log_file = os.path.join(log_path, filename)
        debug_enabled = self.get_setting('addon_debug')
        debug_enabled = 1


        if not debug_enabled:
            return
        try:
            if not isinstance(msg, str):
                raise Exception('c.log() msg not of type str!')

            if trace == 1:
                caller = getframeinfo(stack()[1][0])

                head = debug_prefix
                _msg = f'\n     {msg}:\n    \n--> called from file {caller.filename} @ {caller.lineno}'
            else:
                head = info_prefix
                _msg = f'\n    {msg}'


            #xbmc.log(f"\n\n--> addon name @ 147 = {self.name} | {self.pluginversion} | {self.moduleversion}  \n\n")

            if not os.path.exists(log_file):
                _file = open(log_file, 'w', encoding="utf8")
                line = '=======================================================\nClassy started this file\n=======================================================\n\n'
                _file.write(line, encoding="utf8")
            with open(log_file, 'a', encoding="utf8") as _file:
                now = datetime.datetime.now()
                _dt = now.strftime("%Y-%m-%d %H:%M:%S")

                line = f'{_dt} {head}: {msg}'
                _file.write(line.rstrip('\r\n') + '\n')

        except Exception as exc:
            xbmc.log(f'[ {self.name} ] Logging Failure: {exc}', 1)

    def scraper_error(self, msg, scraper, trace=0):
        msg = f'ERROR Scraper: {scraper} | {msg}'
        self.log(msg, trace)


    def ensure_str(self, s, encoding='utf-8', errors='strict') -> str:
        try:
            # Als de invoer een bytes-object is, decodeer het naar een string
            if isinstance(s, bytes):
                return s.decode(encoding, errors)
            # Als de invoer al een string is, geef het terug
            elif isinstance(s, str):
                return s
            # Voor andere typen, converteer naar string met str()
            else:
                return str(s)
        except UnicodeDecodeError as e:
            # Handle the case where decoding fails
            if errors == 'strict':
                raise
            elif errors == 'ignore':
                return ''  # Return empty on ignore
            elif errors == 'replace':
                return s.decode(encoding, 'replace')
            else:
                raise ValueError(f"Unknown error handling option: {errors}") from e
        except ValueError as e:
            log(f'[CM Debug @ 318 in crewruntime.py]ValueError: {e}')
        except Exception as e:
            raise ValueError(f"Failed to ensure string: {e}")

    def ensure_text(self, input_value, errors='strict') -> str:
    # Check if the input is already a string
        if isinstance(input_value, str):
            return input_value  # Already a string, so return it

        # Check if the input is bytes
        elif isinstance(input_value, bytes):
            try:
                # Decode bytes to string using UTF-8 and specified error handling
                return input_value.decode('utf-8', errors)
            except UnicodeDecodeError as e:
                # Handle the case where decoding fails
                if errors == 'strict':
                    raise
                elif errors == 'ignore':
                    return ''  # Return empty on ignore
                elif errors == 'replace':
                    return input_value.decode('utf-8', 'replace')
                else:
                    raise ValueError(f"Unknown error handling option: {errors}") from e

        # If the input is neither a string nor bytes, typeconvert to string
        return str(input_value)

    def encode(self,s, encoding='utf-8') -> bytes:
        # Check if the input is a string
        if isinstance(s, str):
            # In Python 3, 'str' is already Unicode, so we encode it.
            return s.encode(encoding)

        if isinstance(s, bytes):
            # If it's already bytes, just return it as is (Python 3)
            return s

        # If it's neither a string nor bytes, raise an error
        raise TypeError("Input must be a string or bytes, not '{}'".format(type(s).__name__))


    def decode(self,data, encoding='utf-8') -> str:
        if not isinstance(data, (str, bytes)):
            data = data.encode(encoding).strip()

        if isinstance(data, str):
            return data

        # Check if the input data is of type bytes
        if not isinstance(data, bytes):
            raise Exception("Input data must be a byte string.")

        try:
            # Try to decode the byte string
            return data.decode(encoding)
        except UnicodeDecodeError as e:
            import traceback
            failure = traceback.format_exc()
            self.log(f'[CM Debug @ 404 in crewruntime.py]Traceback:: {failure}')
            self.log(f'[CM Debug @ 405 in crewruntime.py]Exception raised. Error = {e}')

            raise UnicodeDecodeError(f"Decoding failed: {e}") from e

    def strip_tags(self, text) -> str:
        clean = re.compile(r'\[.*?\]')
        return re.sub(clean, '', text)


    def in_addon(self) -> bool:
        return xbmc.getInfoLabel('Container.PluginName') == "plugin.video.classy"

    def get_setting(self, setting) -> str:
        return xbmcaddon.Addon().getSetting(id=setting)

    def set_setting(self, setting, val) -> None:
        return xbmcaddon.Addon().setSetting(id=setting, value=val)


    def get_addon_info(self, info_id):
        if self.addon_info is None:
            return None
        return self.addon_info.get(info_id, None)


    def get_addon_data(self, data_id):
        if self.addon_data is None:
            return None
        return self.addon_data.get(data_id, None)


    def get_addon_version(self):
        return self.version


    def get_addon_path(self):
        return self.path


    def get_addon_name(self):
        return self.addon_id


    def get_addon_id(self):
        return self.addon_id


    def get_addon(self):
        return self.addon


    def get_addon_settings(self):
        return self.addon_settings

    def set_addon_settings(self, settings):
        self.addon_settings = settings
        return True

    def addon_icon(self) -> str:
        if self.art_path is not None and self.theme.lower() not in ['classy']:
            return os.path.join(self.art_path, 'icon.png')
        return xbmcaddon.Addon().getAddonInfo('icon')

    def addon_thumb(self) -> str:
        if self.art_path is not None and self.theme.lower() not in ['classy']:
            return os.path.join(self.art_path, 'thumb.jpg')
        return ''

    def addon_poster(self) -> str:
        if self.art_path is not None and self.theme.lower() not in ['classy']:
            return os.path.join(self.art_path, 'poster.png')
        return 'DefaultVideo.png'

    def addon_banner(self) -> str:
        if self.art_path is not None and self.theme.lower() not in ['classy']:
            return os.path.join(self.art_path, 'banner.png')
        return 'DefaultVideo.png'

    def addon_fanart(self) -> str:
        if self.art_path is not None and self.theme.lower() not in ['classy']:
            fanart = os.path.join(self.art, 'fanart.jpg')
            if isinstance(fanart, tuple):
                return fanart[0]
            return fanart
        return xbmcaddon.Addon().getAddonInfo('fanart')

    def addon_clearart(self) -> str:
        if self.art_path is not None and self.theme.lower() not in ['classy']:
            return os.path.join(self.art_path, 'clearart.png')
        return ''

    def addon_discart(self) -> str:
        if self.art_path is not None and self.theme.lower() not in ['classy']:
            return os.path.join(self.art_path, 'discart.png')
        return ''

    def addon_clearlogo(self) -> str:
        if self.art_path is not None and self.theme.lower() not in ['classy']:
            return os.path.join(self.art_path, 'clearlogo.png')
        return ''

    def addon_next(self) -> str:
        if self.art_path is not None and self.theme.lower() not in ['classy']:
            return os.path.join(self.art_path, 'next.png')
        return 'DefaultVideo.png'
    def get_art_path(self) -> str:
        if self.theme.lower() in ['classy']:
            self.log(f"[CM Debug @ 363 in classy.py]path = {os.path.join(self.path, 'resources', 'lib', 'artwork', str(self.theme))}")
            return os.path.join(self.path, 'resources', 'lib', 'artwork', str(self.theme))

    def appearance(self):
        self.log(f"[CM Debug @ 367 in classy.py] appearance = {self.get_setting('theme')}")
        return (self.get_setting('theme').lower())


    def artwork(self) -> None:
        xbmc.executebuiltin('RunPlugin(plugin://script.thecrew.artwork)')










c = Classy()