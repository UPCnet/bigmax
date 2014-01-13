# -*- coding: utf-8 -*-
import requests
import re
import os
import sys
import json
from urllib2 import unquote


ORIGINAL_MAXUI_IMAGES_URL = '/maxui-dev/img'
ORIGINAL_MAXUI_FONT_URL = '../font'
DEFAULT_MAXUI_IMAGES_URL = '/maxui/img'
DEFAULT_MAXUI_IMAGES_FOLDER = './maxui/img'
DEFAULT_MAXUI_FONTS_URL = '/maxui/font'
DEFAULT_MAXUI_FONTS_FOLDER = './maxui/font'
DEFAULT_MAXUI_GITHUB_URL = 'https://github.com/UPCnet/max.ui.js'
DEFAULT_MAXUI_BRANCH = 'develop'
DEFAULT_MAXUI_JS = './max.ui.js'
DEFAULT_MAXUI_CSS = './max.ui.css'


def saveConfiguration(config):
    """
        Loads stored configuration from .maxui_setup
    """
    dump = json.dumps(config, indent=4)
    open('.maxui_setup', 'w').write(dump)


def getConfiguration():
    """
        Gests current configuration stored on .maxui_setup
    """
    if not os.path.exists('.maxui_setup'):
        default = {
            'github_url': DEFAULT_MAXUI_GITHUB_URL,
            'branch': DEFAULT_MAXUI_BRANCH,
        }
        saveConfiguration(default)
    data = open('.maxui_setup').read()
    config = json.loads(data)
    return config


def downloadFile(config, filename, raw=True):
    """
        Downloads a file from the repo and branch specified in the configuration
        If raw is False, will download the github page html instead of the raw file
    """
    params = dict(config)
    params['filename'] = filename
    params['tree'] = 'raw' if raw else 'tree'
    url = '{github_url}/{tree}/{branch}/{filename}'.format(**params)
    sys.stdout.write(" Downloading {} ".format(url))
    sys.stdout.flush()
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        return False
    sys.stdout.write("✓\n")
    sys.stdout.flush()
    return response.content


def main():
    # Setup configuration parameters
    # User will be asked if not setted

    print
    config = getConfiguration()

    if 'images_url' not in config:
        images_url = raw_input("Images base_url ['{}']: ".format(DEFAULT_MAXUI_IMAGES_URL))
        images_url = images_url.strip()
        images_url = images_url.rstrip('/')
        config['images_url'] = images_url if images_url else DEFAULT_MAXUI_IMAGES_URL

    if 'images_location' not in config:
        images_url = raw_input("Image files location ['{}']: ".format(DEFAULT_MAXUI_IMAGES_FOLDER))
        images_url = images_url.strip()
        images_url = images_url.rstrip('/')
        config['images_location'] = images_url if images_url else DEFAULT_MAXUI_IMAGES_FOLDER

    if 'fonts_url' not in config:
        fonts_url = raw_input("Fonts base_url ['{}']: ".format(DEFAULT_MAXUI_FONTS_URL))
        fonts_url = fonts_url.strip()
        fonts_url = fonts_url.rstrip('/')
        config['fonts_url'] = fonts_url if fonts_url else DEFAULT_MAXUI_FONTS_URL

    if 'fonts_location' not in config:
        fonts_url = raw_input("Font files location ['{}']: ".format(DEFAULT_MAXUI_FONTS_FOLDER))
        fonts_url = fonts_url.strip()
        fonts_url = fonts_url.rstrip('/')
        config['fonts_location'] = fonts_url if fonts_url else DEFAULT_MAXUI_FONTS_FOLDER

    if 'js_location' not in config:
        js_location = raw_input("Javascript file location ['{}']: ".format(DEFAULT_MAXUI_JS))
        js_location = js_location.strip()
        config['js_location'] = js_location if js_location else DEFAULT_MAXUI_JS

    if 'css_location' not in config:
        css_location = raw_input("Stylesheet file location ['{}']: ".format(DEFAULT_MAXUI_CSS))
        css_location = css_location.strip()
        config['css_location'] = css_location if css_location else DEFAULT_MAXUI_CSS

    saveConfiguration(config)

    version = downloadFile(config, 'version').rstrip('\n')

    js = downloadFile(config, 'build/js/max.ui-{}.js'.format(version))
    if not js:
        print ' MAX UI Version {} build not found'.format(version)
        sys.exit(1)
    #Download and modify JS
    open(config['js_location'], 'w').write(js)

    js = downloadFile(config, 'build/debug/max.ui-{}-debug.js'.format(version))
    if not js:
        print ' MAX UI DEBUG Version {} build not found'.format(version)
        sys.exit(1)
    #Download and modify JS
    fname = config['js_location'].split('.js')[0]
    open('{}-debug.js'.format(fname), 'w').write(js)

    #Download and modify CSS
    css = downloadFile(config, 'build/css/max.ui-{}.css'.format(version))
    sys.stdout.write(" Modifying image links ")
    sys.stdout.flush()
    css = re.sub(r"(url\(['\"]?){}(['\"]?)".format(ORIGINAL_MAXUI_IMAGES_URL), r"\1{images_url}\2".format(**config), css)
    css = re.sub(r"(url\(['\"]?){}(['\"]?)".format(ORIGINAL_MAXUI_FONT_URL), r"\1{fonts_url}\2".format(**config), css)
    open(config['css_location'], 'w').write(css)
    sys.stdout.write("✓\n")
    sys.stdout.flush()

    #Download fonts
    extensions = ['eot', 'svg', 'ttf', 'woff']
    for extension in extensions:
        fontbytes = downloadFile(config, 'font/maxicons.' + extension)
        open(config['fonts_location'] + '/maxicons.' + extension, 'w').write(fontbytes)

    #Download images
    images = downloadFile(config, 'img', raw=False)
    image_urls = re.findall(r'href=".*?/%s/img/(.*?)"' % (config['branch']), images)
    for image in image_urls:
        imagebytes = downloadFile(config, 'img/' + image)
        open(config['images_location'] + '/' + unquote(image), 'w').write(imagebytes)

    print '\n MAX UI {} setup finished\n'.format(version)

if __name__ == "__main__":
    main()
