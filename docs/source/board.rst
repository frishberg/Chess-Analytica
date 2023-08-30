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

   from chess-analytica import Board

Attributes
-------------
WRITE DESCRIPTION.  attributes are for scraping, methods are for analysis.

add attribute listings here

Methods
----------------
Below I've provided all useful methods of the Board class, along with a brief description and example usage of each.  For more information on each method, please refer to the docstrings in the code.

Note: There are some methods that I don't include in this list, such as the calculate_time_length method (which is used to calculate the length of chess games), as they are not meant to be used by the user, and are only meant to be used by the other more important methods.

__init__(PGN: str)
--------------------

__str__()
-------------

move()
----------

get_board()
---------------

get_FEN()
------------

has_move()
------------

reset()
---------

more methods to come
---------------------