
import os
print(f"\n package_path :\n{os.path.abspath(__file__)}")
import sys
print(f"\n sys.modules[__name__].__file__ :\n{sys.modules[__name__].__file__}")
print(f"\n os.getcwd() :\n{os.getcwd()}")
PJT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = f"{PJT_PATH}/{sys.modules[__name__].__package__}/data"



from . import auth
from . import drive
