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
import xbmcplugin
import xbmcgui

from ..modules.classy import c
from ..modules import kodiutils


sysaddon = sys.argv[0]
addon_handle = int(sys.argv[1])
syshandle = int(sys.argv[1])



class navigator:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def deinit(self):
        pass

    def root(self):
        self.addDirectoryItem(32002, 'navDevs', 'devs.png', 'devs.png')
        self.addDirectoryItem('Movies', 'navMovies', 'icon.png', 'icon.png')
        self.addDirectoryItem('TVShows', 'navTVShows', 'icon.png', 'icon.png')
        self.addDirectoryItem('Settings', 'opensettings&query=0.0', 'settings.png', 'settings.png')


        self.endDirectory()


    def navMovies(self):
        self.addDirectoryItem('Trakt', 'traktmovies', 'trakt.png', 'trakt.png')


        self.endDirectory()


    def navTVShows(self):
        self.addDirectoryItem('Trakt', 'traktshows', 'trakt.png', 'trakt.png')


        self.endDirectory()

    def navDevs(self):
        self.addDirectoryItem('Test 1', 'test1', 'classy.png', 'classy.png')
        self.addDirectoryItem('Test 2', 'test2', 'classy.png', 'classy.png')
        self.addDirectoryItem('Test 3', 'test3', 'classy.png', 'classy.png')
        self.addDirectoryItem('Test 4', 'test4', 'classy.png', 'classy.png')

        self.endDirectory()

    def traktMovies(self):
        self.addDirectoryItem('Trakt Movies', '', 'icon.png', 'icon.png', isFolder=False)

        self.endDirectory()

    def traktTVShows(self):
        self.addDirectoryItem('Trakt Movies', '', 'icon.png', 'icon.png', isFolder=False)

        self.endDirectory()

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):

        if isinstance(name, int):
            name = c.lang(name)

        url = f'{sysaddon}?action={query}' if isAction is True else query
        thumb = os.path.join(c.art_path, thumb) if c.art_path is not None else icon


        #li = kodiutils.item(label=name)
        #li = xbmcgui.ListItem('Folder Four', iconImage=thumb)
        li = xbmcgui.ListItem(label=name, offscreen=True)
        #li.addContextMenuItems(cm)
        li.setArt({'icon': icon, 'thumb': thumb})

        if c.fanart is not None:
            li.setProperty('fanart', c.fanart)

        #kodiutils.addItem(handle=syshandle, url=url, listitem=li, isFolder=isFolder)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)


    def addDirectoryItem2(self, name, query, thumb, icon, fanart = c.fanart, isFolder=True, isAction=True, infolabels=None, context=None):
        try:
            if isinstance(name, int):
                name = c.lang(name)


            url = f'{sysaddon}?action={query}' if isAction is True else query

            thumb = os.path.join(c.get_art_path(), thumb) if c.get_art_path() is not None else icon

            if infolabels is None:
                infolabels = {}

            cm = []
            #if queue is True:
                #cm.append((queueMenu, f'RunPlugin({sysaddon}?action=queueItem)'))

            if context is not None:
                if isinstance(context, list):
                    context = context[0]

                #cm.append((c.lang(context[0]),f'RunPlugin({sysaddon}?action={context[1]})',))

            item = kodiutils.item(label=name, offscreen=True)
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

            kodiutils.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
        except Exception as e:
            import traceback
            failure = traceback.format_exc()
            c.log(f'[CM Debug @ 112 in navigator.py]Traceback:: {failure}')
            c.log(f'[CM Debug @ 112 in navigator.py]Exception raised. Error = {e}')
            pass


    def endDirectory(self, cacheToDisc=True) -> None:
        try:
            #kodiutils.content(syshandle, 'addons')
            #kodiutils.directory(syshandle, cacheToDisc)
            #xbmcplugin.endOfDirectory(syshandle,cacheToDisc)#succeeded=True,updateListing=True,
            #XBMCAddon::xbmcplugin::endOfDirectory(syshandle,bool	succeeded,bool	updateListing,bool	cacheToDisc )
            #xbmcplugin.setContent(addon_handle, 'videos')
            xbmcplugin.endOfDirectory(addon_handle)

        except Exception as e:
            import traceback
            failure = traceback.format_exc()
            c.log(f'[CM Debug @ 124 in navigator.py]Traceback:: {failure}')
            c.log(f'[CM Debug @ 124 in navigator.py]Exception raised. Error = {e}')
            pass



n = navigator()