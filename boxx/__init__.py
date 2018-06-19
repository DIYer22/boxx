# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
Box-X is a develop-time Toolbox for Python.
Espacially for Scientific Computing and Computer Vision.
'''
__version__ = "0.9.0.3"
__short_description__ = "Tool-box for efficient build and debug in Python. Especially for Scientific Computing and Computer Vision."
__license__ = "MIT"
__author__ = "DIYer22"
__author_email__ = "ylxx@live.com"
__maintainer__ = "DIYer22"
__maintainer_email__ = "ylxx@live.com"
__github_username__ = "DIYer22"
__github_url__ = "https://github.com/DIYer22/boxx"
__support__ = "https://github.com/DIYer22/boxx/issues"
#import sys
#sys.modules['matplotlib.pyplot'] = 9
from . import ylsys
from . import ylcompat
from . import tool
from . import ylimg
from . import ylnp
from . import ylml
from . import yldb
from . import undetermined



from .tool import *
from .ylsys import *
from .ylcompat import *
from .ylimg import *
from .ylml import *
from .ylnp import *


if __name__ == '__main__':
    pass

