"""
"""
import sys
from .base_class import DynamicRobotApiClass
from .utils import SalabsUtils

PY2 = sys.version_info < (3,)
PY3 = sys.version_info > (2,)

__all__ = [DynamicRobotApiClass, SalabsUtils, PY2, PY3]

