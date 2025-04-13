# -*- coding: utf-8 -*-

'''
********************************************************cm*
* Classy Add-on
*
* @file utilities
* @package plugin.video.classy
*
* @copyright (c) 2025, Classy Mouse
* @license GNU General Public License, version 3 (GPL-3.0)
*
********************************************************cm*
'''

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

from .classy import c


execute = xbmc.executebuiltin
idle = execute('Dialog.Close(busydialognocancel)')

item = xbmcgui.ListItem
addItem = xbmcplugin.addDirectoryItem
addItems = xbmcplugin.addDirectoryItems
content = xbmcplugin.setContent
directory = xbmcplugin.endOfDirectory

setproperty = xbmcplugin.setProperty


def open_settings(query='', _id=c.addon_id):
    try:
        #idle()
        #execute('Addon.OpenSettings(%s)' % id)
        execute(f'Addon.OpenSettings({_id})')
        if not query:
            raise Exception()
        e, f = query.split('.')

        execute('SetFocus(%i)' % (int(e) - 100))
        execute('SetFocus(%i)' % (int(f) - 80))


    except Exception as e:
        import traceback
        failure = traceback.format_exc()
        c.log(f'[CM Debug @ 49 in utilities.py]Traceback:: {failure}')
        c.log(f'[CM Debug @ 49 in utilities.py]Exception raised. Error = {e}')

    #except Exception as e:
        #c.log(f"[CM Debug @ 38 in utilities] error = {e}")
        return

def notification(title, message, icon=None, time=3000):
    if title == 'default' or title is None:
        title = c.name
    if isinstance(title, int):
        title = c.lang(title)
    if icon is None:
        icon = c.icon
    xbmcgui.Dialog().notification(title, message, icon, time)
