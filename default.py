import sys
import os

import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import xbmcaddon

ADDON = xbmcaddon.Addon(id="plugin.video.classy")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ID = ADDON.getAddonInfo("id")
ADDON_PATH = ADDON.getAddonInfo("path")


def log(msg):
    LOGPATH = xbmcvfs.translatePath('special://logpath/')
    FILENAME = 'daddylive.log'
    LOG_FILE = os.path.join(LOGPATH, FILENAME)
    try:
        if isinstance(msg, str):
                _msg = f'\n    {msg}'

        else:
            raise TypeError('log() msg not of type str!')

        if not os.path.exists(LOG_FILE):
            f = open(LOG_FILE, 'w', encoding='utf-8')
            f.close()
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            line = ('[{} {}]: {}').format(datetime.now().date(), str(datetime.now().time())[:8], _msg)
            f.write(line.rstrip('\r\n') + '\n')
    except (TypeError, Exception) as e:
        try:
            xbmc.log(f'[ Daddylive ] Logging Failure: {e}', 2)
        except:
            pass

# Main function that creates the menu
def create_menu():
    # Create a new list of items in the plugin menu
    # Tools menu
    add_directory_item("Tools", open_tools_menu)

    # Developers menu
    add_directory_item("Developers", open_developers_menu)

    # End the directory listing to display the menu
    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))

# Adds an item to the Kodi menu
def add_directory_item(name, action, is_folder=True, thumbnail=None):
    # Add a menu item with a custom function call
    list_item = xbmcgui.ListItem(name)
    list_item.setInfo(type="Video", infoLabels={"Title": name})
    list_item.setArt({'thumb': thumbnail})  # Optionally, set a thumbnail image
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url="plugin://{}?action={}".format(ADDON_ID, action), listitem=list_item, isFolder=is_folder)

# Tools Menu
def open_tools_menu():
    xbmc.executebuiltin("Addon.OpenSettings({})".format(ADDON_ID))

# Developers Menu
def open_developers_menu():
    xbmcgui.Dialog().notification("Developer", "This is the developer's menu", xbmcgui.NOTIFICATION_INFO, 3000)
    # Add more functionality here in the future

# Parse the parameters passed to the add-on
def router(param):
    if param == "tools":
        open_tools_menu()
    elif param == "developers":
        open_developers_menu()
    else:
        create_menu()

if __name__ == "__main__":
    param = sys.argv[2][1:] if len(sys.argv) > 2 else None
    log(f"Starting {ADDON_NAME} with parameters: {param}")
    router(param)
