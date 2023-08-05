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
Instllation
===========

Install with pip
```
   $ pip install popet
```
How to Use
==========

You can use `Popet`, `Pope` (Awful naming).

```python
from datetime import date

from popet import Popet, Pope

pope = Popet.who(date(1970, 5, 1))

popes_who_has_god_in_english_name = \
    Popet.pope_match("god", cmp=lambda pope, value: value in pope.english_name.lower())

print(popes_who_has_god_in_english_name) #[<Pope: Servant of God Paul VI, 21/06/1963-06/08/1978>, <Pope: Servant of God John Paul I, 26/08/1978-28/09/1978>]

print(pope)                     # <Pope: Servant of God Paul VI, 21/06/1963-06/08/1978>
print(pope.english_name)        # Servant of God Paul VI
print(pope.personal_name)       # Giovanni Battista Enrico Antonio Maria Montini
print(pope.regnal_name)         # PAULUS Sextus
print(pope.start)               # 1963-06-21
print(pope.end)                 # 1978-08-06
print(pope.in_inauguration(date(1964, 1, 1))) # True

```
Documentation
=============

`Popet`
=======
vars
----
- `popes` - `list`: stores all `Popet.pope`

methods
-------
- `Popet.who(dt)`
- `Popet.pope_match(value, key=lambda pope: pope, cmp=lambda pope, value: pope.in_inauguration(value), error="warn")`

`Popet.who(dt)`
---------------
- `dt`: instance of `datetime.date` or `datetime.datetime`. Return first pope which return `Pope.in_inaugration(dt)`


`Popet.pope_match(value, key=lambda pope: pope, cmp=lambda pope, value: pope.in_inauguration(value), error="warn")`
-------------------------------------------------------------------------------------------------------------------------
 - `value`: any
 - `key`: callable with one argument
 - `cmp`: callable with two arguments
 - `error` - `str`: setting of how to handle errors. 
 
 Return all `popet.Pope` objects stored in `cls.popes` which `cmp(key(Pope), value)` is `True`.
if `key` is not provided, `key` is `lambda pope: pope`
if `cmp` is not provided, `cmp` is `lambda pope, value: pope.in_inauguration(value)`

`error` sets error level

- `"ignore"`: ignore all errors occurred while running compare
- `"warn"`: just warn error - default
- `"raise"`: raise any errors

Default, this will return all `Pope` which in inauguration at given `value`(which must be `datetime.date`).

`Pope`
======
vars
----
- `start` - `datetime.date`: The date The pope inaugurated 
- `end` - `datetime.date`: The date The pope left his position 
- `english_name` - `str`: His English name
- `regnal_name` - `str`: His Regnal name in latin
- `personal_name` - `str`: His Personal name

`Pope.in_inauguration(dt)`
--------------------------

- `dt`: instance of `datetime.date` or `datetime.datetime`.

Return if he is in inauguration at `dt`.

`Pope` will be return `True` if `dt` is in between `Pope.start`(from very first of the day) and `Pope.end`(until very end of the day).


In End
======
Sorry for my poor English, And that I made useless library.
I want **you** to join us and send many pull requests about Doc, code, features and more!!
