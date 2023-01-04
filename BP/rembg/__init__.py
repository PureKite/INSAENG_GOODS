from . import _version

__version__ = _version.get_versions()["version"]

from .bg import remove
from .bg import remove1
from .bg import remove2
from .session_factory import new_session
