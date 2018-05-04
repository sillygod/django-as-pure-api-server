import datetime
import sys
import logging
import json
import gzip
import traceback
import struct
import random
import socket
import math
from logging.handlers import DatagramHandler, SocketHandler

WAN_CHUNK, LAN_CHUNK = 1420, 8154 # what the fuck are these?

# https://github.com/severb/graypy/blob/master/graypy/handler.py

# http://docs.graylog.org/en/2.4/pages/gelf.html
# document describe the spec to implement gelf
# references

class GELFMixin:

    """
    """

    def makePickle(self, record):
        data = {}
        frame = gzip.compress(data) if self.compress else data
        # what is http frame
        return frame
    
# 似乎overwrite makePickle 是個方式，但是以程式設計而言，那個地方應該
# 不是推薦的方式... 必須再仔細思考一下！
# 創造新的logger似乎也沒很好？
# 目前感覺應該是要藉由客製handler沒錯
# 
# emit會call send, send會call makePickle

class GELFHandler(GELFMixin, DatagramHandler):

    """Graylog Extended Log Format UDP handler

    """

    def __init__(self, host, port, ):
        DatagramHandler.__init__()


class GELFTCPHandler(GELFMixin, SocketHandler):

    """
    """

    def __init__(self, host, port, ):
        SocketHandler.__init__()