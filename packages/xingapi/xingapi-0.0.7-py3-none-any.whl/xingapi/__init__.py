import sys
if sys.platform != 'win32':
    raise Exception('xingapi requires 32bit working environment')

import win32com.client
from xingapi.api.xabase import XASession, XAQuery, XAReal