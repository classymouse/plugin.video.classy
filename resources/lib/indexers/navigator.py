# -*- coding: utf-8 -*-

'''
********************************************************cm*
* Classy Add-on
*
* @file navigator.py
* @package plugin.video.classy
*
* @copyright (c) 2025, Classy Mouse
* @license GNU General Public License, version 3 (GPL-3.0)
*
********************************************************cm*
'''

import sys
import os

import xbmc

from ..modules.classy import c
from ..modules import utilities


sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])



class navigator:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def deinit(self):
        pass

    def root(self):
        self.addDirectoryItem('Developers', 'navDevs', 'developers', 'developers.png')
        self.addDirectoryItem('Movies', 'navMovies', 'icon.png', 'icon.png')
        self.addDirectoryItem('TVShows', 'navTVShows', 'icon.png', 'icon.png')
        self.addDirectoryItem('Settings', 'opensettings&query=0.0', 'settings', 'settings.png')


        self.endDirectory()


    def navMovies(self):
        self.addDirectoryItem('Trakt', 'traktmovies', 'icon.png', 'icon.png')


        self.endDirectory()


    def navTVShows(self):
        self.addDirectoryItem('Trakt', 'traktshows', 'icon.png', 'icon.png')


        self.endDirectory()

    def navDevs(self):
        self.addDirectoryItem('Classy Mouse', 'classymouse', 'classymouse', 'classymouse.png')
        self.addDirectoryItem('Classy Add-on', 'classyaddon', 'classyaddon', 'classyaddon.png')
        self.addDirectoryItem('Classy API', 'classyapi', 'classyapi', 'classyapi.png')
        self.addDirectoryItem('Classy API (Legacy)', 'classyapi_legacy', 'classyapi_legacy', 'classyapi_legacy.png')


        self.endDirectory()

    def addDirectoryItem(self, name, query, thumb, icon, fanart = c.fanart, isFolder=True, isAction=True, infolabels=None, context=None):
        try:
            if isinstance(name, int):
                name = c.lang(name)


            url = f'{sysaddon}?action={query}' if isAction is True else query

            thumb = os.path.join(c.art_path, thumb) if c.art_path is not None else icon

            if infolabels is None:
                infolabels = {}

            cm = []
            #if queue is True:
                #cm.append((queueMenu, f'RunPlugin({sysaddon}?action=queueItem)'))

            if context is not None:
                if isinstance(context, list):
                    context = context[0]

                #cm.append((c.lang(context[0]),f'RunPlugin({sysaddon}?action={context[1]})',))

            item = utilities.item(label=name, offscreen=True)
            #item.addContextMenuItems(cm)

            item.setArt({'icon': thumb, 'thumb': thumb})


            if fanart is not None:
                item.setProperty('fanart_image', fanart)
            elif c.addon_fanart is not None:
                item.setProperty('fanart', c.addon_fanart)

            if thumb is not None:
                item.setArt({'thumb': thumb})
            elif c.addon_fanart is not None:
                item.setArt({'thumb': c.addon_fanart})

            utilities.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
        except Exception as e:
            import traceback
            failure = traceback.format_exc()
            c.log(f'[CM Debug @ 112 in navigator.py]Traceback:: {failure}')
            c.log(f'[CM Debug @ 112 in navigator.py]Exception raised. Error = {e}')
            pass


    def endDirectory(self, cacheToDisc=True):
        utilities.content(syshandle, 'addons')
        utilities.directory(syshandle, cacheToDisc)


n = navigator()