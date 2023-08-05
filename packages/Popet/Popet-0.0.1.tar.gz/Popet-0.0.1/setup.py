"""
The Useless Easy Tool to Handle Pope's Data
===========================================
Powered by [Yamato Nagata](https://twitter.com/514YJ)

Data by [Tako](https://twitter.com/TLE_Maker)

[GitHub](https://github.com/delta114514/Popet)

[ReadTheDocs](https://popet.readthedocs.io/en/latest/)


```python
from datetime import date

from popet import Popet

pope = Popet.who(date(1970, 5, 1))

print(pope)
    # <Pope: Servant of God Paul VI, 21/06/1963-06/08/1978>
print(vars(pope))
    # {'start': datetime.date(1963, 6, 21), 'end': datetime.date(1978, 8, 6), 'english_name': 'Servant of God Paul VI', 'regnal_name': 'PAULUS Sextus', 'personal_name': 'Giovanni Battista Enrico Antonio Maria Montini'}

```
"""

from setuptools import setup
from os import path

about = {}
with open("popet/__about__.py") as f:
    exec(f.read(), about)

here = path.abspath(path.dirname(__file__))

setup(name=about["__title__"],
      version=about["__version__"],
      url=about["__url__"],
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      description=about["__description__"],
      long_description=__doc__,
      packages=["popet"],
      zip_safe=False,
      platforms="any",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ])
