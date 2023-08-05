
#============================================================
"""복사-붙여넣기로 사용해라.
사용 후 모듈에선 삭제해라."""
#============================================================

import os
os.getcwd()
import sys
sys.modules[__name__].__package__
sys.path.append("/Users/sambong/pjts/libs/igoogle")
sys.path.append("/Users/sambong/pjts/libs/igoogle/env/lib/python3.7/site-packages")
%env GOOGLE_AUTH_PATH=/Users/sambong/pjts/libs/igoogle/igoogle-auth.json
import pprint
pp = pprint.PrettyPrinter(indent=2)
