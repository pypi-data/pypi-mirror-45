import datetime
from os import path
from urllib.request import urlopen, urlretrieve
from xml.dom import minidom

import requests

from dwc.debug import print_download_status
from dwc.utils import save_image
from dwc.utils import set_wallpaper_permanent

# get today's date
date = str(datetime.date.today())


def picpath_bing(xmldoc, saveDir, SHOW_DEBUG):
    # Parsing the XML File
    for element in xmldoc.getElementsByTagName('url'):
        if SHOW_DEBUG:
            print('Getting URL for Bing')
        url = 'http://www.bing.com' + element.firstChild.nodeValue
        url = url.replace("1366x768", "1920x1200")
        url = url.replace("1920x1080", "1920x1200")
        if SHOW_DEBUG:
            print("Download from:", url)
        # Get Current Date as fileName for the downloaded Picture
        picPath = saveDir + 'bingwallpaper' + date + '.jpg'
        picPath = save_image(url, picPath, SHOW_DEBUG)

    return picPath


def get_usock_bing(SHOW_DEBUG):
    usock = urlopen(
     'http://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=en-IN')
    return usock


def change_wp(wp_bing, saveDir, SHOW_DEBUG):
    # if 0:
    if path.isfile(wp_bing) is True:
        if SHOW_DEBUG:
            print('Picture already found, updating that only')
        set_wallpaper_permanent(wp_bing, SHOW_DEBUG)
    else:
        if SHOW_DEBUG:
            print('Picture is not in the system, updating process starts ...')
        usock = get_usock_bing(SHOW_DEBUG)
        xmldoc = minidom.parse(usock)
        picPath_bing = picpath_bing(xmldoc, saveDir, SHOW_DEBUG)
        set_wallpaper_permanent(picPath_bing, SHOW_DEBUG)
