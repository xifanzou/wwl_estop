import os
import pandas as pd
from .process import run

import warnings
warnings.filterwarnings("ignore")

def __set_dir__():
    curpath = os.path.abspath(__file__)
    dirpath = os.path.dirname(os.path.dirname(curpath))
    os.chdir(dirpath)

    return 

__set_dir__()