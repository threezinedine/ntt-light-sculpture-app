import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "Engine"))
try:
    from .Engine import *
except:
    from .Engine.Engine import *
