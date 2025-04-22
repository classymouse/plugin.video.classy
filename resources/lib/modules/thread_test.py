# -*- coding: utf-8 -*-

"""
********************************************************cm*
* Classy Add-on
********************************************************cm*
"""

import os
import concurrent.futures
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


def open_settings(query: str = '', _id: str = c.addon_id) -> None:
    try:
        idle
        execute(f'Addon.OpenSettings({_id})')

        if not query:
            raise ValueError("No query string provided for focus targeting.")
        e, f = query.split('.')

        execute(f'SetFocus({int(e) - 100})')
        execute(f'SetFocus({int(f) - 80})')
    except Exception as e:
        c.log(f"[kodi.py] Failed to open settings: {e}", level="error")


def notification(title, message, icon=None, time=3000) -> None:
    if not title or title == 'default':
        title = c.name
    if isinstance(title, int):
        title = c.lang(title)
    if icon is None:
        icon = c.icon
    xbmcgui.Dialog().notification(title, message, icon, time)


def get_max_threads(total_items: int, default_cap: int = 50) -> int:
    """Determine an appropriate number of threads for concurrent tasks."""
    try:
        addon = xbmcaddon.Addon()
        user_defined = int(addon.getSetting('max_threads') or 0)
    except Exception:
        user_defined = 0

    cpu_cores = os.cpu_count() or 1
    c.log(f"[CM Debug @ 63 in thread_test.py] cpu_cores: {cpu_cores}")
    c.log(f"[CM Debug @ 64 in thread_test.py] user_defined: {user_defined}")
    thread_count = user_defined if user_defined > 0 else cpu_cores * 2
    thread_count = min(thread_count, default_cap, total_items)
    c.log(f"[CM Debug @ 67 in thread_test.py] thread_count: {thread_count}")
    return max(5, thread_count)