**ChessDotCom**
=====================

Summary
---------------

ADD NOTE ABOUT attributes being for scraping and methods for analysis

The ChessDotCom file of chess-analytica contains the Profile class, which 
is the main class of the library.  It allows for the easy scraping of 
data from the chess.com API, filtering of data, analysis of data, and several other features through its various methods (all detailed below).

To import the Profile class, you can use the following code:

.. code-block:: python

   from chess-analytica import Board, ChessDotCom

It's important to import the Board file as well, as the ChessDotCom file is built on top of this code.

WRITE DESCRIPTION.  attributes are for scraping, methods are for analysis.

Attributes
-------------
Below I've provided all useful attributes of the Profile class, along with a brief description and example usage of each.  For more information on each attribute, please refer to the docstrings in the code.

**Note:** There are some attributes that I don't include in this list, such as the PGN attribute (which is the unformatted PGN scraped directly from chess.com), as they are not meant to be used by the user, and are only meant to be used by the other more important attributes and methods.

* username
* info
* stats
* current_games
* games

Example usage:

.. code-block:: python

   profile = ChessDotCom.Profile("aronfrish", True) #Note: will create a save file
   
   print(profile.username) #aronfrish
   
   print(profile.info)
   #{'avatar': 'https://images.chesscomfiles.com/uploads/v1/user/284524683.bd5b154a.200x200o.6803b80151dc.png', 'player_id': 284524683, '@id': 'https://api.chess.com/pub/player/aronfrish', 'url': 'https://www.chess.com/member/aronfrish', 'name': 'Aron Frishberg', 'username': 'aronfrish', 'followers': 14, 'country': 'https://api.chess.com/pub/country/US', 'last_online': 1693357812, 'joined': 1683830055, 'status': 'basic', 'is_streamer': False, 'verified': False, 'league': 'Champion'}
   
   print(profile.stats)
   #{'daily': {'rating': 1191, 'won': 1, 'lost': 0, 'drawn': 0, 'played': 1, 'pct-won': 100.0, 'pct-lost': 0.0, 'pct-drawn': 0.0}, 'rapid': {'rating': 920, 'won': 334, 'lost': 299, 'drawn': 56, 'played': 689, 'pct-won': 48.48, 'pct-lost': 43.4, 'pct-drawn': 8.13}, 'bullet': {'rating': 479, 'won': 55, 'lost': 50, 'drawn': 6, 'played': 111, 'pct-won': 49.55}, 'blitz': {'rating': 440, 'won': 0, 'lost': 3, 'drawn': 1, 'played': 4, 'pct-won': 0.0, 'pct-lost': 75.0, 'pct-drawn': 25.0}}
   
   print(len(profile.current_games)) #0 Note: this player doesn't have any current games right now
   
   print(profile.games[0].final_state)
   # r n b . k b . r
   # p p p p q p p p
   # . . . . . . . .
   # . . . . . . . .
   # . . . . . . N .
   # . . . P . . . .
   # P P P K . P P P
   # R N B n . B . R
   #Note: this is what the final state of this players first game looked like

Methods
----------------
Below I've provided all useful methods of the Profile class, along with a brief description and example usage of each.  For more information on each method, please refer to the docstrings in the code.

**Note:** There are some methods that I don't include in this list, such as the import_json_from_url method (which is used to scrape from the chess.com API), as they are not meant to be used by the user, and are only meant to be used by the other more important methods.

__init__ (username: str, save_mode: bool)
---------------------------------------------------------------------
This serves as the onstructor method for the Profile class.  It takes in the username of the player and uses class methods to scrape the chess.com API for the player's profile, stats, current games, and games, 
and then modifies the data to be more useful and accessible.  It also stores the games as Board objects, which can be used to get information about the games and play through the sequence of moves.

**Note:** If save_mode is True, then the constructor tries to call the load_info() method.  If the file exists, it sucessfully loads the data from the file and returns True.  If the file does not exist, it scrapes the data from the API and saves it for the next use.  If save_mode is False, then the constructor scrapes the data from the API and does not save it to a file.

Example usage:

.. code-block:: python

   profile = ChessDotCom.Profile("aronfrish", True) #Note: will create a save file
   
   print(profile.username) #aronfrish


filter_game_type(type: str)
---------------------------
This method filters the games list to only contain games of a given type (ex. "rapid", "bullet", ...), allowing for more specific analysis (ex. analyzing only bullet games to see the player's most popular bullet openings).

Example usage:

.. code-block:: python

   profile = ChessDotCom.Profile("aronfrish", True)
   
   print(len(profile.games)) #855
   
   profile.filter_game_type("bullet")
   
   print(len(profile.games)) #113

find_games_with_FEN(FEN: str)
---------------------------------
Finds all of the games that contain a given FEN.  This goes through all of the board objects in games (potentially filtered by filter_game_type()) and checks if they contain the given FEN using their containsFEN() method.  This method simulates through the entire game and checks if the given FEN matches at any point throughout the game.

Example usage:

.. code-block:: python

   profile = ChessDotCom.Profile("aronfrish", True)
   
   print(len(profile.games)) #855
   
   found_games = profile.find_games_with_FEN("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R") #Note: this is the FEN for the 4 knights opening
   
   print(len(found_games)) #95 Note: this means that the player has played the 4 knights opening in 95 of their games
   
   print(len(found_games)/len(profile.games)) #0.1111111111111111 Note: this means that 11% of the player's games contained the 4 knights opening

find_games_with_FEN_and_Color(FEN: str, is_white: bool)
------------------------------------------------------------
Finds all of the games that contain a given FEN and where the player is white (if is_white bool is True) or black (if is_white bool is False) using the find_games_with_FEN() method.

Example usage:

.. code-block:: python

   profile = ChessDotCom.Profile("aronfrish", True)
   
   print(len(profile.games)) #855
   
   found_games = profile.find_games_with_FEN_and_Color("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R", True) #Note: this is the FEN for the 4 knights opening, and the True means that the player was white
   
   print(len(found_games)) #67 Note: this means that the player has played the 4 knights opening in 67 of their games as white

find_moves_after_FEN(FEN: str, is_white: bool)
------------------------------------------------
Goes through all games, where the player is white (if is_white bool is True) or black (if is_white bool is False), and finds their most common moves (with frequency) after that FEN.  This method uses the find_games_with_FEN_and_Color() method to find the games, and then uses the getNextMove() method from the Board class to find the next move in the game.  It then sorts the moves and frequencies by frequency using the sortMovesAndFrequencies() method.

Example usage:

.. code-block:: python

   profile = ChessDotCom.Profile("aronfrish", True)
   
   moves = find_moves_after_FEN("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R", True) #Note: this is the FEN for the 4 knights opening, and the True means that the player was white
   
   print(moves)
   #([Move.from_uci('c3d5'), Move.from_uci('f1d3'), Move.from_uci('f1c4'), Move.from_uci('d2d3'), Move.from_uci('a2a3'), Move.from_uci('d2d4')], 
   [27, 16, 15, 4, 3, 2])
   #Note: this means that in the four knights opening, the player's most common move as white was c3d5, which they played 27 times, their second most common move was f1d3, which they played 16 times, and so on

move_table(FEN: str, is_white: bool)
--------------------------------------------
Returns a printable table of the most frequent moves after a given FEN, where the player is white (if is_white bool is True) or black (if is_white bool is False).  This method uses the find_moves_after_FEN() method to find the moves and frequencies, and then formats them into a printable table.

Example usage:

.. code-block:: python

   profile = ChessDotCom.Profile("aronfrish", True)
   
   print(profile.move_table("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R", False)) #Note: this is the FEN for the 4 knights opening, and the True means that the player was black
   
   #f1c4: 11
   #d2d4: 5
   #f1b5: 5
   #f3e5: 3
   #a2a3: 1
   #b2b3: 1
   #g2g3: 1
   #f1e2: 1

   #Note: this means that in the four knights opening, the player's most common move as black was f1c4, which they played 11 times, their second most common move was d2d4, which they played 5 times, and so on

most_common_move(FEN: str, is_white: bool)
----------------------------------------------
Returns the most frequent move after a given FEN, where the player is white (if is_white bool is True) or black (if is_white bool is False).  This method uses the find_moves_after_FEN() method to find the moves and frequencies, and then returns the first move in the list of moves (which is the most frequent move).

Example usage:

.. code-block:: python

   profile = ChessDotCom.Profile("aronfrish", True)
   
   print(profile.most_common_move("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R", False)) #Note: this is the FEN for the 4 knights opening, and the True means that the player was black
   #f1c4
   #Note: this means that in the four knights opening, the player's most common move as black was f1c4