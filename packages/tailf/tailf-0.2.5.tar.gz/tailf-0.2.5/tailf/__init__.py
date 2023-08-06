from .const import *

if __import__("sys").version_info < (3, 6):
    from .basic import Tail
else:
    from .basic_async import Tail
