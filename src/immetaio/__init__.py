"""
# immetaio: Image and Metadata I/O for Visual Media

**immetaio** (**im**age + **meta**data + **io**) is a Python library that provides saving and loading image arrays and their associated metadata. It is built for computer vision, graphics, and computational imaging workloads where every image paired with user-defined metadata.
"""

from . import meta
from . import json
from . import array
from . import array_nonblock
from . import array_meta
from . import array_meta_nonblock
from . import array_meta_dir
from . import array_meta_multi
from . import params
from .master import save, load
from .array_nonblock import wait_saves
