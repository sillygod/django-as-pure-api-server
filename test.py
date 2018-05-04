# from pygelf import GelfTcpHandler, GelfUdpHandler, GelfTlsHandler, GelfHttpHandler
# import logging


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger()
# logger.addHandler(GelfTcpHandler(host='127.0.0.1', port=9401))
# logger.addHandler(GelfTcpHandler(host='localhost', port=12201))

# logger.info('hello gelf wow')

import json
import datetime

obj = {
    "a": 1,
    "b": 2,
}

def smarter_repr(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return repr(obj)

string = json.dumps(obj, separators=",:", default=smarter_repr)
print(string)

# json part of source code ..
# you see it will use the default function if get unexpected type ..
# def _iterencode(o, _current_indent_level):
#     if isinstance(o, str):
#         yield _encoder(o)
#     elif o is None:
#         yield 'null'
#     elif o is True:
#         yield 'true'
#     elif o is False:
#         yield 'false'
#     elif isinstance(o, int):
#         # see comment for int/float in _make_iterencode
#         yield _intstr(o)
#     elif isinstance(o, float):
#         # see comment for int/float in _make_iterencode
#         yield _floatstr(o)
#     elif isinstance(o, (list, tuple)):
#         yield from _iterencode_list(o, _current_indent_level)
#     elif isinstance(o, dict):
#         yield from _iterencode_dict(o, _current_indent_level)
#     else:
#         if markers is not None:
#             markerid = id(o)
#             if markerid in markers:
#                 raise ValueError("Circular reference detected")
#             markers[markerid] = o
#         o = _default(o)
#         yield from _iterencode(o, _current_indent_level)
#         if markers is not None:
#             del markers[markerid]
# return _iterencode

