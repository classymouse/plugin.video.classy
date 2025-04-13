# -*- coding: utf-8 -*-

'''
***********************************************************
* Classy Add-on
*
* @file default.py
* @package plugin.video.classy
*
* @copyright (c) 2025, Classy Mouse
* @license GNU General Public License, version 3 (GPL-3.0)
*
********************************************************cm*
'''


from sys import argv
from urllib.parse import parse_qsl
from resources.lib.modules import router

from resources.lib.modules.classy import c

if __name__ == "__main__":
    params = dict(parse_qsl(argv[2].replace('?', '')))
    c.log(f"Starting {c.name} with parameters: {params}")
    router.router(params)
