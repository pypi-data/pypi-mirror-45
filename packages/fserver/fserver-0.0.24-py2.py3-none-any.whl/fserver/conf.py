# -*- coding: utf-8 -*-

VERSION = '0.0.24'
BUILD_TIME = '2019/05/02'

DEBUG = False

UPLOAD_OVERRIDE_MODE = False
UPLOAD = False

VIDEO_SUFFIX = ['mp4', 'flv', 'hls', 'dash', 'mkv']
VIDEO_CDN_JS = {
    'flv': '/static/flv.min.js',
    'hls': '/static/hls.js@latest',
    'dash': '/static/dash.all.min.js',
    'mp4': '',
    'mkv': ''
}

BIND_IP = '0.0.0.0'
BIND_PORT = 2000

BLACK_LIST = set()
WHITE_LIST = set()
WHITE_LIST_PARENTS = set()
_ROOT = '.'
ROOT = '.'
STRING = None
SORT = True


def display():
    msg = u"""   debug                 =             {}
   ip                    =             {}
   port                  =             {}
   nosort                =             {}
   upload                =             {}
   upload_override       =             {}
   root                  =             {}
   string                =             {}
   white_list            =             """.format(DEBUG, BIND_IP, BIND_PORT, not SORT, UPLOAD, UPLOAD_OVERRIDE_MODE,
                                                  _ROOT, STRING)

    if len(WHITE_LIST) == 0:
        msg += 'turn off '
    else:
        for ind, v in enumerate(WHITE_LIST):
            if ind == 0:
                msg += v + ','
            else:
                msg += '\n' + ' ' * 39 + v + ','

    msg += '\b\n   black_list            =             '
    if len(BLACK_LIST) == 0:
        msg += 'turn off '
    else:
        for ind, v in enumerate(BLACK_LIST):
            if ind == 0:
                msg += v + ','
            else:
                msg += '\n' + ' ' * 39 + v + ','

    max_len = 0
    for i in msg.split('\n'):
        if len(i) > max_len:
            max_len = len(i)
    line = '=' * (max_len + 3)
    msg = line + '\n' + msg + '\b\n' + line
    print(msg)
