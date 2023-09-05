Chess-Analytica: chess analytics made easy
================================================================================

.. image:: https://img.shields.io/pypi/v/chess-analytica
    :target: https://pypi.org/project/chess-analytica/
    :alt: PyPI

.. image:: https://static.pepy.tech/badge/chess-analytica
    :target: https://pepy.tech/project/chess-analytica
    :alt: Downloads

.. image:: https://readthedocs.org/projects/python-chess/badge/?version=latest
    :target: https://python-chess.readthedocs.io/en/latest/
    :alt: Docs

.. image:: https://img.shields.io/pypi/l/chess-analytica
    :target: https://pypi.org/project/chess-analytica/
    :alt: License

.. image:: https://img.shields.io/pypi/status/chess-analytica
    :target: https://pypi.org/project/chess-analytica/
    :alt: Status

Introduction
------------

**Chess-Analytica** is a chess library that allows for the simple scraping of data using the chess.com API, and subsequent 
analysis of that data.  Built on top of the python-chess library, Chess-Analytica allows for you to easily scrape 
all of a given player's past (or current) games, filter the games down, and then analyze them.

.. code:: python

    from chess_analytica import Board, ChessDotCom

    profile = ChessDotCom.Profile("aronfrish", False)

    profile.filterGameType("rapid")

    print(len(profile.games)) #720

    n = 0
    for game in profile.games : #Note: this is still filtered to rapid
    if ("resignation" in game.termination) :
        n += 1
    print(n) #Note: this will print the number of the player's rapid games that ended in resignation
    #334

    italian_games = profile.find_games_with_FEN_and_Color("r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R", True) #Note: this FEN is the italian game and the target player color is white (because is_white is set to True)
    print(len(italian_games)/len(profile.white_games)) #Note: this will print the percentage of rapid games (where the player is white) that the player has played the italian game
    #0.013888888888888888

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