ChessDotCom
============

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

Attributes
-------------
WRITE DESCRIPTION.  attributes are for scraping, methods are for analysis.

add attribute listings here

Methods
----------------
Below I've provided all useful methods of the Profile class, along with a brief description and example usage of each.  For more information on each method, please refer to the docstrings in the code.

Note: There are some methods that I don't include in this list, such as the import_json_from_url method (which is used to scrape from the chess.com API), as they are not meant to be used by the user, and are only meant to be used by the other more important methods.

__init__ (username: str, import_save: bool)
---------------------------------------------------------------------

filter_game_type(type: str)
---------------------------

find_games_with_FEN(FEN: str)
---------------------------------

find_games_with_FEN_and_Color(FEN: str, is_white: bool)
------------------------------------------------------------

find_moves_after_FEN(FEN: str, is_white: bool)
------------------------------------------------

move_table(FEN: str, is_white: bool)
--------------------------------------------

most_common_move(FEN: str, is_white: bool)
----------------------------------------------