
from igoogle import *


def print_cursor_explain(cursor):
    """https://api.mongodb.com/python/current/api/pymongo/cursor.html"""
    cursor.explain()

def print_obj(object):
    #print(f"\n\n objectname : {object.__name__}")
    print(f"\n\n dir(object) :\n\n {dir(object)}")
    #print(f"\n\n object.__dir__() :\n\n {object.__dir__()}")

    print(f"\n\n object.__dict__ :\n")
    pp.pprint(object.__dict__)

    # __class__
    print(f"\n\n object.__class__ : {object.__class__}")
    print(f"\n\n object.__class__.__dict__ :\n")
    pp.pprint(object.__class__.__dict__)
    print(f"\n\n object.__class__.__name__ : {object.__class__.__name__}")
    print(f"\n\n object.__class__.__module__ : {object.__class__.__module__}")

    #print(f"\n\n object.objects : {object.objects}")

def print_frame(frame):
    # args
    print(f"\n\n inspect.getargvalues(frame).locals :\n")
    pp.pprint(inspect.getargvalues(frame).locals)
