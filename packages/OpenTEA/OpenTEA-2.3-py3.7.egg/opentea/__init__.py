#!/usr/bin/env python
# pylint: disable=wrong-import-position,wrong-import-order
"""
OpenTEA scientific GUI library.
Documentation is hosted at: http://cerfacs.fr/opentea
"""



__author__ = "Antoine Dautpain"
__credits__ = ["Antoine Dautpain",
               "Guillaume Frichet",
               "Adrien Bonhomme",
               "Corentin Lapeyre",
               "Gregory Hannebique",
               "Franchine Ni",
               "Benjamin Farcy",
               "Luis Segui",
              ]
__license__ = "CeCILL-B"
__version__ = "3.0.0"
__shadate__ = "$Format:%h - %cD$"
__maintainer__ = "Antoine Dauptain"
__email__ = "coop@cerfacs.fr"
__status__ = "Development"

# Check python version
import sys
if sys.hexversion < 0x030000A0:
    raise Exception("Must be run with python version"
                    " at least 3.0.0, and not python 2\n"
                    "Your version is %i.%i.%i" % sys.version_info[:3])

# Constants and exceptions First
from .constants import COMMON, TEMP, RUN_CURRENT
from .exceptions import (XDRException, XDRnoNodeException,
                         XDRtooManyNodesException, XDRnoFileException,
                         XDRillFormed, XDRUnknownValue, XDRInterrupt,
                         OTException, OTNoNodeException,
                         OTTooManyNodesException, OTNoFileException,
                         OTIllFormed, OTUnknownValue, OTInterrupt)

# Simple logging
import logging
LOGGER = logging.getLogger()
LOGGER.setLevel("DEBUG")
LOG_LEVEL_FILE = "DEBUG"
LOG_LEVEL_STREAM = "DEBUG"

FILE_FORMAT = logging.Formatter("%(asctime)s %(name)s "
                                "%(levelname)s  %(message)s")
FILE_HANDLER = logging.FileHandler(__name__+'.log')
FILE_HANDLER.setFormatter(FILE_FORMAT)
FILE_HANDLER.setLevel(LOG_LEVEL_FILE)
LOGGER.addHandler(FILE_HANDLER)

STREAM_FORMAT = logging.Formatter("%(levelname)s  %(message)s")
STREAM_HANDLER = logging.StreamHandler(sys.stdout)
STREAM_HANDLER.setFormatter(STREAM_FORMAT)
STREAM_HANDLER.setLevel(LOG_LEVEL_STREAM)
LOGGER.addHandler(STREAM_HANDLER)

if sys.hexversion < 0x02070aF0:
    LOGGER.warning("Your version of python is at least 2 years old.")
    LOGGER.warning("It is unsupported and can cause errors (c.f. issue #27 of"
                   " AVSP)")

if "Format" in __shadate__:
    from os.path import dirname, abspath
    import subprocess
    import inspect
    opentea_dir = dirname(abspath(inspect.getfile(inspect.currentframe())))
    __shadate__ = subprocess.check_output(
        'cd {} ; git log -1 --format="%h - %cD"'.format(
            opentea_dir), shell=True, universal_newlines=True).strip()

LOGGER.info("Welcome to OpenTEA version " + __version__)
LOGGER.info("Exact version: " + __shadate__)
LOGGER.info("Python executable is: " + sys.executable)

from .startup import tcl_starter

# PathTools and Dataset only inherit from object
from .path_tools import PathTools
from .dataset import Dataset
from .lazy_methods import pairwise, replace_pattern_in_file, currentnext

# These guys rely heavily on the above
from .executor import Executor
from .mesh import Mesh
from .process import BaseProcess, CodeProcess, LibProcess
from .plugin import Plugin
from .wincanvas import WinCanvas
