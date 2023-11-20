**Usage**
============

.. _installation:

Installation
---------------

To use Chess-Analytica, first install it using pip:

.. code-block:: python

   pip install chess-analytica

Examples
----------------

**Note: I have detailed examples and explanations of each method in both ChessDotCom and Board.  Below are some general examples to display the libraries capabilities**

To retrieve all of a player's games, you create an instance of the ``Profile`` class in ChessDotCom.

By calling the constructor, it will automatically retrieve all available information about the player (games archive, name, rating, ...).

.. code:: python

   from chess_analytica import Board, ChessDotCom

   profile = ChessDotCom.Profile("aronfrish", False)

   print(len(profiles.games)) #846

The constructor also allows for the option of using a save file or not.  If you set the "import-save" parameter to True, it will attempt to load the profile from a save file.  If the save file does not exist, it will scrape the data and create one.

Because of this implementation, it's recommended that you leave this on True for the most part, unless you need to use data that is fully up to date.  Otherwise, the save file will make the program run a lot quicker, as it won't have to scrape the data each time.

There is also a filter option implemented into this library, that can be used as such:

.. code:: python

   from chess_analytica import Board, ChessDotCom

   profile = ChessDotCom.Profile("aronfrish", False)

   profile.filter_game_type("rapid")

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


This feature allows for more exact analytics, as you're able to filter out games that you don't want to include in your analysis.  For example, the average accuracy of 
a blitz game is far lower than the average accuracy of a classical game, so you may want to filter out blitz games if you want to determine the true skill of a player.

This library also includes many analytical methods, such as ``mostCommonMove()`` and ``moveTable()``.  These methods can be used as such:

.. code:: python

   from chess_analytica import Board, ChessDotCom

   profile = ChessDotCom.Profile("aronfrish", False)

   print(profile.most_common_move("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R", True)) #Note: given this FEN, which is the four knights opening, and setting "white" to True (meaning that we'll be looking at all of the times the given player has been white in this position), it will tell us their most common move
   #c3d5

   print(profile.move_table("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R", True)) #Note: using the same parameters as above, but this produces a visual table containing all of their moves in the given position and their frequencies (in descending order to show most popular first)

   # c3d5: 27
   # f1d3: 16
   # f1c4: 15
   # d2d3: 4
   # a2a3: 3
   # d2d4: 2