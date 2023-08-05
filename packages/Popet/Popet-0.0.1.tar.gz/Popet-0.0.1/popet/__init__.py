"""
    Popet
    -----------

    The Useless Easy Tool to Handle Pope's Data

    Powered by [Yamato Nagata](https://twitter.com/514YJ)

    Data by [Tako](https://twitter.com/TLE_Maker)

    [GitHub](https://github.com/delta114514/Popet)

    [ReadTheDocs](https://popet.readthedocs.io/en/latest/)

    :copyright: (c) 2019 by Yamato Nagata.
    :license: MIT.
"""

# [ReadTheDocs](https://popet.readthedocs.io/en/latest/)

from .__about__ import __version__
from .popet import (Pope, Popet)


__all__ = [
    __version__,
    "Popet",
    "Pope"
]