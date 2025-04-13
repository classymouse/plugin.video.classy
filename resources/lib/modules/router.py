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
from . import utilities




def router(params):
    c.log('\n------------------------------------------------------------------------\n')
    c.log(f'Router called with params: {params}')
    c.log('\n------------------------------------------------------------------------\n')



    action = params.get('action')

    if action is None:
        n.root()
    elif action == 'navMovies':
        n.navMovies()
    elif action == 'navTVShows':
        n.navTVShows()
    elif action == 'navDevs':
        n.navDevs()

    elif action == 'traktmovies':
        c.log('Opening Trakt Movies...')
        #n.traktMovies()
    elif action == 'traktshows':
        c.log('Opening Trakt TV Shows...')
        #n.traktTVShows()
    elif action == 'opensettings':
        c.log('Opening settings...')
        query = params.get('query', '0.0')
        utilities.open_settings(query=query)
    else:
        c.log(f'Unknown action: {action}')