chess-analytica: making chess analytics easy.
========================================

.. image:: https://readthedocs.org/projects/chess-analytica/badge/?version=latest
    :target: https://python-chess.readthedocs.io/en/latest/
    :alt: Docs

Introduction
------------

chess-analytica is a chess library that allows for the simple scraping of data using the chess.com API, and subsequent 
analysis of that data.  Built on top of the python-chess library, chess-analytica allows for you to easily scrape 
all of a given player's past (or current) games, filter the games down, and then analyze them.

.. code:: python

    >>> from chess_analytica import Board, ChessDotCom

    >>> profile = ChessDotCom("aronfrish", False) #False means that it will not try to import the games from the "cache" folder

    >>> print(profile.games[0].info) #
