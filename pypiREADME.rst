Chess-Analytica: Simplifying Chess Analytics
============================================

Introduction
------------
**Chess-Analytica** is a powerful chess library designed for effortless data scraping and analysis. Utilizing the chess.com API, it builds upon the robust `python-chess` library, enabling users to scrape and analyze past or current games of any player with ease.

Key Features:
- Easy scraping of game data from chess.com profiles.
- Advanced game filtering options.
- Comprehensive analysis of game patterns and styles.

Quick Start
-----------
Here's a glimpse of what you can do with Chess-Analytica:

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

Installation
------------
Easily install Chess-Analytica using pip:

    pip install chess-analytica

Documentation and Resources
---------------------------
Explore detailed documentation and examples to get the most out of Chess-Analytica:

- **Documentation**: `Full Documentation <https://chess-analytica.readthedocs.io/en/latest/>`_
- **Usage Examples**: `Examples <https://chess-analytica.readthedocs.io/en/latest/usage.html>`_
- **API Reference**: `ChessDotCom Class <https://chess-analytica.readthedocs.io/en/latest/chessdotcom.html>`_ | `Board Class <https://chess-analytica.readthedocs.io/en/latest/board.html>`_

License
-------
Chess-Analytica is open-sourced and available under the MIT License. For more details, see `LICENSE.txt`.
