"""
Return config on servers to start for syncthing

See https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
for more information.
"""
import os

def setup_syncthing():
    return {
        'command': ['syncthing'],
        'port': 8384,
        'environment': {},
        'launcher_entry': {
            'title': 'syncthing',
            'icon_url': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'syncthing.svg')
        }
    }
