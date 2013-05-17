import requests
import re
import os
import sys
import json

ORIGINAL_MAXUI_IMAGES_FOLDER = '/maxui-dev/img'
DEFAULT_MAXUI_IMAGES_FOLDER = '/maxui/img'
DEFAULT_MAXUI_GITHUB_URL = 'https://github.com/UPCnet/max.ui.js'
DEFAULT_MAXUI_BRANCH = 'conversations'
DEFAULT_MAXUI_JS = './max.ui.js'
DEFAULT_MAXUI_CSS = './max.ui.css'


def saveConfiguration(config):
    dump = json.dumps(config, indent=4)
    open('.maxui_setup', 'w').write(dump)


def getConfiguration():
    if not os.path.exists('.maxui_setup'):
        default = {
            'github_url': DEFAULT_MAXUI_GITHUB_URL,
            'branch': DEFAULT_MAXUI_BRANCH,
        }
        saveConfiguration(default)
    data = open('.maxui_setup').read()
    config = json.loads(data)
    return config


def downloadFile(config, filename):
    params = dict(config)
    params['filename'] = filename
    response = requests.get('{github_url}/raw/{branch}/{filename}'.format(**params), verify=False)
    if response.status_code != 200:
        return False
    return response.content


config = getConfiguration()

if 'images_url' not in config:
    images_url = raw_input("Images base_url ['{}']: ".format(DEFAULT_MAXUI_IMAGES_FOLDER))
    images_url = images_url.strip()
    images_url = images_url.rstrip('/')
    config['images_url'] = images_url if images_url else DEFAULT_MAXUI_IMAGES_FOLDER

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

js = downloadFile(config, 'build/max.ui-{}.js'.format(version))
if not js:
    print 'MAX UI Version {} build not found'.format(version)
    sys.exit(1)

js = re.sub(r'src="{}'.format(ORIGINAL_MAXUI_IMAGES_FOLDER), r'src="{images_url}'.format(**config), js)
open(config['js_location'], 'w').write(js)

css = downloadFile(config, 'css/max.ui.css'.format(version))
css = re.sub(r"url\('{}".format(ORIGINAL_MAXUI_IMAGES_FOLDER), r"url('{images_url}".format(**config), css)
open(config['css_location'], 'w').write(css)

print 'MAX UI {} setup finished'.format(version)
