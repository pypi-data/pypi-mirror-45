.. -*- mode: rst -*-

|license|_ |pypi|_

.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
.. _license: https://opensource.org/licenses/MIT

.. |pypi| image:: https://badge.fury.io/py/temprint.svg
.. _pypi: https://pypi.org/project/temprint/

temprint
========

    *temprint* is an acronym for *temporary print*

This package provides an easy way to output temporary prints intended to be
overwritten by other messages. Use it if you want to avoid flooding your terminal
with old prints.

Usage
-----

1. Install it with ``$ pip install temprint``

2. Now you can use the ``temprint`` function, as in:

.. code:: python

    from time import sleep
    from temprint import temprint

    msgs = [
        'a short message',
        'a slightly longer message',
        'a tiny msg',
        'a very big message. it is so big that it cannot fit in your ' +
        'terminal width and temprint will behave as a regular print',
        'now a short message again',
        'and a shorter message'
    ]

    for msg in msgs:
        temprint(msg)
        sleep(2)

You should see the messages being printed and then erased iteratively.

.. note:: If the message is longer than your terminal width, ``temprint`` will
    behave as the regular built-in ``print`` function.

The ``temprint`` function
-------------------------

The ``temprint`` function can receive a series of objects to be printed and a
separator.

>>> temprint('first', 'second', 'third', sep='/')
first/second/third
