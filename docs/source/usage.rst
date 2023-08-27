Usage
=====

.. _installation:

Installation
---------------

To use chess-analytica, first install it using pip:

.. code-block:: console

   pip install chess-analytica

Examples
----------------

To retrieve all of a player's games, you create an instance of the ``Profile`` class in ChessDotCom.

By calling the constructor, it will automatically retrieve all available information about the player (games archive, name, rating, ...).

.. code:: python

   from chess_analytica import Board, ChessDotCom

   profile = ChessDotCom.Profile("aronfrish", False)

   print(len(profiles.games))

   # 846

The constructor also allows for the option of using a save file or not.  If you set the "import-save" parameter to True, it will attempt to load the profile from a save file.  If the save file does not exist, it will scrape the data and create one.

Because of this implementation, it's recommended that you leave this on True for the most part, unless you want to use data that is fully up to date.  Otherwise, the save file will make the program run a lot quicker, as it won't have to scrape the data each time.