**Board**
============

Summary
---------------

The Board file of chess-analytica contains the Board class, which 
is used by the ChessDotCom class to represent a board/chess game.  This class is built off of 
the chess library, which allowed for the easy implementation of the board and game logic.

All of the methods in ChessDotCom that involve the board are built off of this class and return objects of the Board class, so 
methods in the Board class will be needed to interpret results from ChessDotCom.

This board class can also be used on its own, without the ChessDotCom class, to represent a board and game.

To import the Board class alone, you can use the following code:

.. code-block:: python

   from chess_analytica import Board

Attributes
-------------
Below I've provided all useful attributes of the Board classalong with a use case for each.  For more information on each attribute, please refer to the docstrings in the code.

**Note:** There are some attributes that I don't include in this list, such as the PGN attribute (which is the unformatted PGN scraped directly from chess.com), as they are not meant to be used by the user, and are only meant to be used by the other more important attributes and methods.

* date
* white_player
* black_player
* white_elo
* black_eli
* time_control
* termination
* start_time
* end_time
* link
* time_length
* board
* moves_left
* final_state
* winner

Example usage:

.. code-block:: python

   profile = ChessDotCom.Profile("aronfrish", True)
   
   game = profile.games[0]
   
   print(game.date) #2023.05.11
   
   print(game.white_player) #aronfrish
   
   print(game.black_player) #8ak34
   
   print(game.white_elo) #590
   
   print(game.black_elo) #746
   
   print(game.time_control) #600
   
   print(game.termination) #8ak34 won by resignation
   
   print(game.start_time) #8:34:58
   
   print(game.end_time) #8:36:15
   
   print(game.link) #https://www.chess.com/game/live/77569257661
   
   print(game.time_length) #77
   
   print(game.board)
   # r n b q k b n r
   # p p p p p p p p
   # . . . . . . . .
   # . . . . . . . .
   # . . . . . . . .
   # . . . . . . . .
   # P P P P P P P P
   # R N B Q K B N R
   
   print(game.moves_left) #[Move.from_uci('e2e4'), Move.from_uci('e7e5'), Move.from_uci('g1f3'), Move.from_uci('g8f6'), Move.from_uci('f3e5'), Move.from_uci('d8e7'), Move.from_uci('e5g4'), Move.from_uci('f6e4'), Move.from_uci('d2d3'), Move.from_uci('e4c3'), Move.from_uci('e1d2'), Move.from_uci('c3d1')]
   
   print(game.final_state)
   # r n b . k b . r
   # p p p p q p p p
   # . . . . . . . .
   # . . . . . . . .
   # . . . . . . N .
   # . . . P . . . .
   # P P P K . P P P
   # R N B n . B . R

   print(game.winner) #8ak34
   #Note: this returns "draw" in the case of a draw

Methods
----------------
Below I've provided all useful methods of the Board class, along with a brief description and example usage of each.  For more information on each method, please refer to the docstrings in the code.

Note: There are some methods that I don't include in this list, such as the calculate_time_length method (which is used to calculate the length of chess games), as they are not meant to be used by the user, and are only meant to be used by the other more important methods.

__init__
--------------------
Parameters: PGN (str)

Constructor for the Board class.  Takes in the PGN of the game (in the format provided by the Chess.com API) and sets the attributes of the board object, 
including the board object, date, white player, black elo, time control, etc... (all of which can be retrieved)

Example usage:

.. code-block:: python

   board = Board(game.PGN) #Note: assuming game.PGN is formatted correctly
   
   print(board.date) #2023.05.11

__str__
-------------
Parameters: None

Returns the string representation of the board, which is a visual representation of the board in its current state

Example usage:

.. code-block:: python

   board = Board(game.PGN) #Note: assuming game.PGN is formatted correctly
   
   print(board)
   # r n b q k b n r
   # p p p p p p p p
   # . . . . . . . .
   # . . . . . . . .
   # . . . . . . . .
   # . . . . . . . .
   # P P P P P P P P
   # R N B Q K B N R

move
----------
Parameters: None

Simulates a move on the board.  This will pop the first element in moves_left, and push it to the board.  If there are no moves left, an exception will be raised.

Example usage:

.. code-block:: python

   board = Board(game.PGN) #Note: assuming game.PGN is formatted correctly
   
   print(board)
   # r n b q k b n r
   # p p p p p p p p
   # . . . . . . . .
   # . . . . . . . .
   # . . . . . . . .
   # . . . . . . . .
   # P P P P P P P P
   # R N B Q K B N R

   board.move() #Note: in this example the next move is e2e4

   print(board)
   # r n b q k b n r
   # p p p p p p p p
   # . . . . . . . .
   # . . . . . . . .
   # . . . . P . . .
   # . . . . . . . .
   # P P P P . P P P
   # R N B Q K B N R

get_FEN
------------
Parameters: None

Returns the FEN (Forsyth–Edwards Notation) of the board, in its current state

Example usage:

.. code-block:: python

   board = Board(game.PGN) #Note: assuming game.PGN is formatted correctly

   board.move() #Note: in this example the next move is e2e4
   
   print(board.get_FEN()) #rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR

has_move
------------
Parameters: None

Returns whether there are moves left in the game

Example usage:

.. code-block:: python

   board = Board(game.PGN) #Note: assuming game.PGN is formatted correctly

   print(board.has_move()) #True

   board.move() #Note: in this example the next move is e2e4.  We also assume that the opponent resigns after the first move for this example

   print(board.has_move()) #False

reset
---------
Parameters: None

Resets the board to the beginning of the game.  This will reset the board to a new state, and reset moves_left to be full of all of the moves of the game again.

Example usage:

.. code-block:: python

   board = Board(game.PGN) #Note: assuming game.PGN is formatted correctly

   board.move() #Note: in this example the next move is e2e4

   print(board)
   # r n b q k b n r
   # p p p p p p p p
   # . . . . . . . .
   # . . . . . . . .
   # . . . . P . . .
   # . . . . . . . .
   # P P P P . P P P
   # R N B Q K B N R

   board.reset()

   print(board)
   # r n b q k b n r
   # p p p p p p p p
   # . . . . . . . .
   # . . . . . . . .
   # . . . . . . . .
   # . . . . . . . .
   # P P P P P P P P
   # R N B Q K B N R

contains_FEN
----------------
Parameters: FEN (str)

Simulates the board through all moves, checking after each move is made to see if the current FEN of the board matches the given FEN.  If it does, the method returns True.  Otherwise, it returns False.  This method is used to check if the state of the game ever matches a given FEN.

Example usage:

.. code-block:: python

   board = Board(game.PGN) #Note: assuming game.PGN is formatted correctly

   board.move()

   print(board)
   # r n b q k b n r
   # p p p p p p p p
   # . . . . . . . .
   # . . . . . . . .
   # . . . . P . . .
   # . . . . . . . .
   # P P P P . P P P
   # R N B Q K B N R

   print(board.contains_FEN("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR")) #True Note: this is the FEN after e2e4

   print(board.contains_FEN("rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR")) #False Note: this is the FEN after a2a4 at the start, which does not occur in this game

get_next_move
-----------------
Parameters: None

Returns the next move in the game

Example usage:

.. code-block:: python

   board = Board(game.PGN) #Note: assuming game.PGN is formatted correctly

   print(board.get_next_move()) #Move.from_uci('e2e4')