Chess-Analytica: chess analytics made easy
================================================================================

.. image:: https://readthedocs.org/projects/python-chess/badge/?version=latest
    :target: https://python-chess.readthedocs.io/en/latest/
    :alt: Docs

.. image:: https://badge.fury.io/py/chess-analytica.svg
    :target: https://badge.fury.io/py/chess-analytica

Introduction
------------

**Chess-Analytica** is a chess library that allows for the simple scraping of data using the chess.com API, and subsequent 
analysis of that data.  Built on top of the python-chess library, Chess-Analytica allows for you to easily scrape 
all of a given player's past (or current) games, filter the games down, and then analyze them.

.. code:: python

    >>> from chess_analytica import Board, ChessDotCom

    >>> profile = ChessDotCom("aronfrish", False) #False means that it will not try to import the games from the "cache" folder

    >>> print(profile.games[0].white_player)
    #aronfrish

    >>> print(profile.games[0].final_state + " \n" + profile.games[0].link)
    #r n b . k b . r
    #p p p p q p p p
    #. . . . . . . .
    #. . . . . . . .
    #. . . . . . N .
    #. . . P . . . .
    #P P P K . P P P
    #R N B n . B . R
    #https://www.chess.com/game/live/77569257661

Installing
----------

Download and install the latest release:

::

    pip install chess-analytica


`Documentation <https://chess-analytica.readthedocs.io/en/latest/>`__
---------------------------------------------------------------------------------------------
* `Examples <https://chess-analytica.readthedocs.io/en/latest/usage.html>`_
* `ChessDotCom Class <https://chess-analytica.readthedocs.io/en/latest/chessdotcom.html>`_
* `Board Class <https://chess-analytica.readthedocs.io/en/latest/board.html>`_

Features
--------

* Scrape all game info from a given player's profile

* Simulate games and analyze them

* Filter games by time control

License
-------

Chess-Analytica is licensed under the MIT License.
Check out ``LICENSE.txt`` for the full text.