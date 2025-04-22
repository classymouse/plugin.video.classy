# -*- coding: utf-8 -*-

'''
********************************************************cm*
* Classy Add-on
*
* @file router.py
* @package plugin.video.classy
*
* @copyright (c) 2025, Classy Mouse
* @license GNU General Public License, version 3 (GPL-3.0)
*
********************************************************cm*
'''

import sys
from .classy import c

from ..indexers.navigator import n
from . import kodi




def router(params):
    c.log(f'Router called with params: {params}')



    action = params.get('action', '')
    query = params.get('query', '')

    if not action:
        n.root()
    elif action == 'navMovies':
        n.navMovies()
    elif action == 'navTVShows':
        n.navTVShows()
    elif action == 'navDevs':
        n.navDevs()
    elif action == 'traktmovies':
        n.traktMovies()
    elif action == 'traktshows':
        n.traktTVShows()
    elif action == 'opensettings':

        kodi.open_settings(query=query)


    ######### Dev actions #########

    elif action == 'test1':
        c.log('Test action triggered')
        kodi.notification('Test', 'Test action executed')
        from . import thread_test
        thread_test.get_max_threads(100)
        # Add your test action code here
    elif action == 'test2':
        c.log('Test2 action triggered')
        kodi.notification('Test2', 'Test2 action executed')
        # Add your test2 action code here
    elif action == 'test3':
        c.log('Test3 action triggered')
        kodi.notification('Test3', 'Test3 action executed')
        # Add your test3 action code here
    elif action == 'test4':
        c.log('Test4 action triggered')
        kodi.notification('Test4', 'Test4 action executed')

    ######## End Dev actions #########

    else:
        c.log(f'Unknown action: {action}')