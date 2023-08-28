ChessDotCom
============

Summary
---------------

The ChessDotCom file of chess-analytica contains the Profile class, which 
is the main class of the library.  It allows for the easy scraping of 
data from the chess.com API, filtering of data, analysis of data, and several other features through its various methods (all detailed below).

To import the Profile class, you can use the following code:

.. code-block:: console

   from chess-analytica import Board, ChessDotCom

It's important to import the Board file as well, as the ChessDotCom file is built on top of this code.

Methods
----------------
Note: There are some methods that I don't include in this list, such as the import_json_from_url method, as they are not meant to be used by the user, and are only meant to be used by the other more important methods.

.. automethod:: ChessDotCom.__init__
.. automethod:: ChessDotCom.get_player_data