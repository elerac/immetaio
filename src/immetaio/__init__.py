"""
# immetaio: Image and Metadata I/O for Visual Media

**immetaio** (**im**age + **meta**data + **io**) is a Python library that provides saving and loading image arrays and their associated metadata. It is built for computer vision, graphics, and computational imaging workloads where every image paired with user-defined metadata.
"""

from .array_nonblock import wait_saves
from .master import save, load
