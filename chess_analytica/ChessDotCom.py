import urllib.request
import json
import os
from .Board import Board

def import_json_from_url(url: str) :
    """
    Imports a JSON from a given URL

    Parameters
    ----------
    url : str
        the given URL to import the JSON from
    
    Returns
    -------
    dict
        the JSON from the given URL
    """
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        return data

def sort_moves_and_frequencies(moves: list, frequencies: list) :
    """
    Sorts a list of moves and frequencies (whose indexes correspond) by frequency.  This is used to check the most frequent moves in a game, and is thus used for the move_table() and most_common_move() methods.
    
    Example: 
    [Move.from_uci('g1f3'), Move.from_uci('d2d4'), Move.from_uci('d1h5')], [158, 26, 27] -> [Move.from_uci('g1f3'), Move.from_uci('d1h5'), Move.from_uci('d2d4')], [158, 27, 26]
    
    Parameters
    ----------
    moves : list
        the list of moves to sort (by frequency)
    frequencies : list
        the list of frequencies to sort

    Returns
    -------
    list
        the sorted list of moves (by frequency)
    list
        the sorted list of frequencies
    """
    for i in range(len(frequencies)) :
        for j in range(i+1, len(frequencies)) :
            if (frequencies[i] < frequencies[j]) :
                temp = frequencies[i]
                frequencies[i] = frequencies[j]
                frequencies[j] = temp
                temp = moves[i]
                moves[i] = moves[j]
                moves[j] = temp
    return moves, frequencies

class Profile :
    """
    Class for a chess.com profile.  Upon creation of an object, it scrapes the chess.com API for the profile, stats, current games, and games of a given player, and modifies 
    some of the data to be more useful and accessible.  It also stores the games as Board objects, which can be used to get information about the games and play through the sequence of moves.
    This class also contains the save_info() and load_info() methods which allow for the data to be saved to a "cache" folder, so that the data does not have to be scraped from the API every time, making it much faster.
    
    Parameters
    ----------
    username : str
        the given username of the player
    save_mode : bool
        whether to import the data from a file in the "cache" folder (True) or scrape the data from the API (False)
    
    Attributes
    ----------
    username : str
        the given username of the player
    info : dict
        the player's profile, scraped from the chess.com API (including avatar url, player_id, url, name, followers, country, joined and some other basic info)
    stats : dict
        the player's stats, which are scraped from the chess.com API, but then modified in the retrieve_player_stats() method to be more useful and accessible.  The stats include ratings, percentage of games won, lost, and drawn for all game types (daily, rapid, ...)
    current_games_data : list
        the player's current ongoing games, scraped directly from the chess.com API
    games_data : list
        the archived player's games, scraped directly from the chess.com API
    all_games : list
        all of the player's games, stored as Board objects  This is not filtered, and contains all of the player's games, regardless of game type (ex. rapid, bullet, ...)
    current_games : list
        the player's current ongoing games, stored as Board objects
    games : list
        the player's games, stored as Board objects.  This contains a filtered version of the all_games list, filtered by the filter_game_type() method.  By default, this list contains all of the player's games, but can be filtered to only contain rapid games, bullet games, etc. to allow for more specific analysis (ex. analyzing only bullet games to see the player's most popular bullet openings)
    white_games : list
        the subset of the games list that contains only games where the player is white.  This list might be filtered, as it is a subset of the games list
    black_games : list
        the subset of the games list that contains only games where the player is black.  This list might be filtered, as it is a subset of the games list
    
    Methods
    -------
    filter_game_type(type: str)
        filters the games list to only contain games of a given type (ex. "rapid", "bullet", ...), allowing for more specific analysis (ex. analyzing only bullet games to see the player's most popular bullet openings)
    retrieve_player_profile()
        scrapes the chess.com API for the player's profile (which includes avatar url, player_id, url, name, followers, country, joined and some other basic info) and returns it in an accessible JSON format
    calc_pct(numerator: int, denominator: int)
        this method calculates the percentage of an event (ex. bullet games lost) given the numerator and denominator (ex. 2 losses out of 5 games: calc_pct(2, 5) -> 40.0)
    retrieve_player_stats()
        scrapes the player's stats directly from the chess.com API, but then modifies the data and stores it in a dictionary so that the data is more useful and accessible.  This method calculates the win, loss and draw percentages of all game types.  The final stats include ratings, percentage of games won, lost, and drawn for all game types (daily, rapid, ...)
    retrieve_current_games()
        scrapes the player's current ongoing game data directly from the chess.com API.  This data will be used to create the board objects for the current_games_data attribute
    retrieve_player_games()
        scrapes the player's archived game data directly from the chess.com API.  This data will be used to create the board objects for the games_data attribute
    save_info()
        saves the player's profile, stats, current games, and games to a file in the "cache" folder
    load_info()
        loads the player's profile, stats, current games, and games from a file in the "cache" folder.  If the file does not exist, it raises an exception
    find_games_with_FEN(FEN: str)
        finds all of the games that contain a given FEN.  This goes through all of the board objects in games (potentially filtered by filter_game_type()) and checks if they contain the given FEN using their contains_FEN() method.  This method simulates through the entire game and checks if the given FEN matches at any point throughout the game.
    find_games_with_FEN_and_Color(FEN: str, is_white: bool)
        finds all of the games that contain a given FEN and where the player is white (if is_white bool is True) or black (if is_white bool is False) using the find_games_with_FEN() method.
    find_moves_after_FEN(FEN: str, is_white: bool)
        goes through all games, where the player is white (if white bool is True) or black (if is_white bool is False), and finds their most common moves (with frequency) after that FEN.  This method uses the find_games_with_FEN_and_Color() method to find the games, and then uses the getNextMove() method from the Board class to find the next move in the game.  It then sorts the moves and frequencies by frequency using the sortMovesAndFrequencies() method.
    move_table(FEN: str, is_white: bool)
        returns a printable table of the most frequent moves after a given FEN, where the player is white (if is_white bool is True) or black (if is_white bool is False).  This method uses the find_moves_after_FEN() method to find the moves and frequencies, and then formats them into a printable table.
    most_common_move(FEN: str, is_white: bool)
        returns the most frequent move after a given FEN, where the player is white (if is_white bool is True) or black (if is_white bool is False).  This method uses the find_moves_after_FEN() method to find the moves and frequencies, and then returns the first move in the list of moves (which is the most frequent move).
    get_white_games()
        returns a list of all of the games where the player is white (using the games list, which might be filtered)
    get_black_games()
        returns a list of all of the games where the player is black (using the games list, which might be filtered)
    """
    def __init__(self, username: str, save_mode: bool = False) :
        """
        Constructor method for the Profile class.  Takes in the username of the player and uses class methods to scrape the chess.com API for the player's profile, stats, current games, and games, 
        and then modifies the data to be more useful and accessible.  It also stores the games as Board objects, which can be used to get information about the games and play through the sequence of moves.
        If save_mode is True, then the constructor tries to call the load_info() method.  If the file exists, it sucessfully loads the data from the file and returns True.  If the file does not exist, it scrapes the data from the API and saves it for the next use.  If save_mode is False, then the constructor scrapes the data from the API and does not save it to a file.
        """
        self.username = username
        if (save_mode and self.load_info()) : #if save_mode is True, then it tries to call the load_info() method.  If the file exists, it sucessfully loads the data from the file and returns True.  If the file does not exist, it returns False, thus sending the constructor to the else statement, where it scrapes the data from the API
            pass
        if (save_mode) :
            self.info = self.retrieve_player_profile()
            self.stats = self.retrieve_player_stats()
            self.current_games_data = self.retrieve_current_games() #contains current game data, scraped directly from chess.com API
            self.games_data = self.retrieve_player_games() #contains all archived game data, scraped directly from chess.com API
            self.save_info() #saves the data to a file in the "cache" folder
        else :
            self.info = self.retrieve_player_profile()
            self.stats = self.retrieve_player_stats()
            self.current_games_data = self.retrieve_current_games() #contains current game data, scraped directly from chess.com API
            self.games_data = self.retrieve_player_games() #contains all archived game data, scraped directly from chess.com API
        self.all_games = [] #contains all archived games, stored as Board objects
        self.current_games = [] #contains all current games, stored as Board objects
        for game in self.games_data : #converts all games to Board objects and adds them to the all_games list
            self.all_games.append(Board(game['pgn']))
        for game in self.current_games : #converts all current games to Board objects and adds them to the current_games list
            self.current_games.append(Board(game['pgn']))
        self.games = self.all_games #self.games is the list of games that is used for analysis.  By default, it is all of the player's games, but it can be filtered by the filter_game_type() method to only contain games of a given type (ex. rapid, bullet, ...)
        self.white_games = self.get_white_games() #contains all games where the player is white, stored as Board objects
        self.black_games = self.get_black_games() #contains all games where the player is black, stored as Board objects
    
    def filter_game_type(self, type: str) :
        """
        This method filters the games list to only contain games of a given type (ex. "rapid", "bullet", ...), allowing for more specific analysis (ex. analyzing only bullet games to see the player's most popular bullet openings)

        Parameters
        ----------
        type : str
            the type of game to filter the games list to.  This can be a number in seconds (ex. 600, 60+1, ...) or a string (ex. "rapid", "bullet", ...)
        """
        self.games = [] #clears the games list
        self.white_games = [] #clears the white_games list
        self.black_games = [] #clears the black_games list
        if ("0" in type) : #if the type was given as a number in seconds (ex. 600, 60+1, ...)
            for game in self.all_games :
                if (game.time_control == type) : #finds all games with the given time control
                    self.games.append(game) #adds them to the games list
        else :
            type = type.lower() #ex. Rapid -> rapid
            if (type=="all") : #if the type is all, then the games list is all of the player's games
                self.games = self.all_games
            elif (type=="rapid") : #if the type is rapid, then the games list is all of the player's rapid games
                for game in self.all_games :
                    if (game.time_control=="600" or game.time_control=="900+10" or game.time_control=="1800") :
                        self.games.append(game)
            elif (type=="bullet") : #if the type is bullet, then the games list is all of the player's bullet games
                for game in self.all_games :
                    if (game.time_control=="60" or game.time_control=="60+1" or game.time_control=="120+0") :
                        self.games.append(game)
            elif (type=="blitz") :
                for game in self.all_games :
                    if (game.time_control=="180" or game.time_control=="180+2" or game.time_control=="300") :
                        self.games.append(game)
            elif (type=="daily") :
                for game in self.all_games :
                    if (game.time_control=="86400") :
                        self.games.append(game)
        self.white_games = self.get_white_games() #updates the white_games list
        self.black_games = self.get_black_games() #updates the black_games list

    def retrieve_player_profile(self) :
        """
        Retrieves the player's profile from the chess.com API, including avatar url, player_id, url, name, followers, country, joined and some other basic info, and returns it in an accessible JSON format

        Returns
        -------
        dict
            the player's profile (in JSON format), including all the player's basic info
        """
        url = "https://api.chess.com/pub/player/" + self.username
        result = import_json_from_url(url)
        return result
    
    def calc_pct(self, numerator: int, denominator: int) :
        """
        Calculates the percentage of an event (ex. bullet games lost) given the numerator and denominator (ex. 2 losses out of 5 games: calc_pct(2, 5) -> 40.0)
        
        Parameters
        ----------
        numerator : int
            the number of events that occurred (ex. 2 losses)
        denominator : int
            the total number of events (ex. 5 games)

        Returns
        -------
        float
            the percentage of the event (ex. 40.0)
        """
        if (denominator == 0) :
            return 0
        return round((numerator / denominator) * 100, 2)

    def retrieve_player_stats(self) :
        """
        Retrieves the player's stats from the chess.com API, but then modifies the data and stores it in a dictionary so that the data is more useful and accessible.  This method calculates the win, loss and draw percentages of all game types.  The final stats include ratings, percentage of games won, lost, and drawn for all game types (daily, rapid, ...)

        Returns
        -------
        dict
            a dictionary containing the player's stats, including ratings, percentage of games won, lost, and drawn for all game types (daily, rapid, ...)
        """
        stats_dict = {}
        stats_dict["daily"] = {}
        stats_dict["rapid"] = {}
        stats_dict["bullet"] = {}
        stats_dict["blitz"] = {}
        url = "https://api.chess.com/pub/player/" + self.username + "/stats"
        result = import_json_from_url(url)
        try :
            stats_dict["daily"]["rating"] = result["chess_daily"]["last"]["rating"]
            stats_dict["daily"]["won"] = result["chess_daily"]["record"]["win"]
            stats_dict["daily"]["lost"] = result["chess_daily"]["record"]["loss"]
            stats_dict["daily"]["drawn"] = result["chess_daily"]["record"]["draw"]
            stats_dict["daily"]["played"] = stats_dict["daily"]["won"] + stats_dict["daily"]["lost"] + stats_dict["daily"]["drawn"]
            stats_dict["daily"]["pct-won"] = self.calc_pct(stats_dict["daily"]["won"], stats_dict["daily"]["played"])
            stats_dict["daily"]["pct-lost"] = self.calc_pct(stats_dict["daily"]["lost"], stats_dict["daily"]["played"])
            stats_dict["daily"]["pct-drawn"] = self.calc_pct(stats_dict["daily"]["drawn"], stats_dict["daily"]["played"])
        except : #in the case the player has no daily games
            stats_dict["daily"]["rating"], stats_dict["daily"]["won"], stats_dict["daily"]["lost"], stats_dict["daily"]["drawn"], stats_dict["daily"]["played"], stats_dict["daily"]["pct-won"], stats_dict["daily"]["pct-lost"], stats_dict["daily"]["pct-drawn"] = 0, 0, 0, 0, 0, 0, 0, 0
        try :
            stats_dict["rapid"]["rating"] = result["chess_rapid"]["last"]["rating"]
            stats_dict["rapid"]["won"] = result["chess_rapid"]["record"]["win"]
            stats_dict["rapid"]["lost"] = result["chess_rapid"]["record"]["loss"]
            stats_dict["rapid"]["drawn"] = result["chess_rapid"]["record"]["draw"]
            stats_dict["rapid"]["played"] = stats_dict["rapid"]["won"] + stats_dict["rapid"]["lost"] + stats_dict["rapid"]["drawn"]
            stats_dict["rapid"]["pct-won"] = self.calc_pct(stats_dict["rapid"]["won"], stats_dict["rapid"]["played"])
            stats_dict["rapid"]["pct-lost"] = self.calc_pct(stats_dict["rapid"]["lost"], stats_dict["rapid"]["played"])
            stats_dict["rapid"]["pct-drawn"] = self.calc_pct(stats_dict["rapid"]["drawn"], stats_dict["rapid"]["played"])
        except : #in the case the player has no rapid games
            stats_dict["rapid"]["rating"], stats_dict["rapid"]["won"], stats_dict["rapid"]["lost"], stats_dict["rapid"]["drawn"], stats_dict["rapid"]["played"], stats_dict["rapid"]["pct-won"], stats_dict["rapid"]["pct-lost"], stats_dict["rapid"]["pct-drawn"] = 0, 0, 0, 0, 0, 0, 0, 0
        try :
            stats_dict["bullet"]["rating"] = result["chess_bullet"]["last"]["rating"]
            stats_dict["bullet"]["won"] = result["chess_bullet"]["record"]["win"]
            stats_dict["bullet"]["lost"] = result["chess_bullet"]["record"]["loss"]
            stats_dict["bullet"]["drawn"] = result["chess_bullet"]["record"]["draw"]
            stats_dict["bullet"]["played"] = stats_dict["bullet"]["won"] + stats_dict["bullet"]["lost"] + stats_dict["bullet"]["drawn"]
            stats_dict["bullet"]["pct-won"] = self.calc_pct(stats_dict["bullet"]["won"], stats_dict["bullet"]["played"])
            stats_dict["bullet"]["pct-lost"] = self.calc_pct(stats_dict["bullet"]["lost"], stats_dict["bullet"]["played"])
            stats_dict["bullet"]["pct-drawn"] = self.calc_pct(stats_dict["bullet"]["drawn"], stats_dict["bullet"]["played"])
        except : #in the case the player has no bullet games
            stats_dict["bullet"]["rating"], stats_dict["bullet"]["won"], stats_dict["bullet"]["lost"], stats_dict["bullet"]["drawn"], stats_dict["bullet"]["played"], stats_dict["bullet"]["pct-won"], stats_dict["bullet"]["pct-lost"], stats_dict["bullet"]["pct-drawn"] = 0, 0, 0, 0, 0, 0, 0, 0
        try :
            stats_dict["blitz"]["rating"] = result["chess_blitz"]["last"]["rating"]
            stats_dict["blitz"]["won"] = result["chess_blitz"]["record"]["win"]
            stats_dict["blitz"]["lost"] = result["chess_blitz"]["record"]["loss"]
            stats_dict["blitz"]["drawn"] = result["chess_blitz"]["record"]["draw"]
            stats_dict["blitz"]["played"] = stats_dict["blitz"]["won"] + stats_dict["blitz"]["lost"] + stats_dict["blitz"]["drawn"]
            stats_dict["blitz"]["pct-won"] = self.calc_pct(stats_dict["blitz"]["won"], stats_dict["blitz"]["played"])
            stats_dict["blitz"]["pct-lost"] = self.calc_pct(stats_dict["blitz"]["lost"], stats_dict["blitz"]["played"])
            stats_dict["blitz"]["pct-drawn"] = self.calc_pct(stats_dict["blitz"]["drawn"], stats_dict["blitz"]["played"])
        except : #in the case the player has no blitz games
            stats_dict["blitz"]["rating"], stats_dict["blitz"]["won"], stats_dict["blitz"]["lost"], stats_dict["blitz"]["drawn"], stats_dict["blitz"]["played"], stats_dict["blitz"]["pct-won"], stats_dict["blitz"]["pct-lost"], stats_dict["blitz"]["pct-drawn"] = 0, 0, 0, 0, 0, 0, 0, 0
        return stats_dict
    
    def retrieve_current_games(self) :
        """
        Retrieves the player's current ongoing game data from the chess.com API

        Returns
        -------
        list
            the player's current ongoing game data, pulled directly from the chess.com API
        """
        all_games = []
        url = "https://api.chess.com/pub/player/" + self.username + "/games"
        result = import_json_from_url(url)
        for game in result['games'] :
            all_games.append(game)
        return all_games
    
    def retrieve_player_games(self) :
        """
        Retrieves the player's archived game data from the chess.com API

        Returns
        -------
        list
            the player's archived game data, pulled directly from the chess.com API
        """
        all_games = []
        url = "https://api.chess.com/pub/player/" + self.username + "/games/archives"
        result = import_json_from_url(url)
        for month in result["archives"] :
            cur = import_json_from_url(month)
            for game in cur['games'] :
                all_games.append(game)
        return all_games

    def save_info(self) :
        """
        Saves the player's profile, stats, current games, and games to a file in the "cache" folder.  If the "cache" folder does not exist, it creates it (prevents FileNotFoundError)
        """
        if (not os.path.exists("cache")) :
            os.mkdir("cache")
        f = open("cache/" + self.username + ".json", "w")
        f.write(json.dumps(self.info) + "\n")
        f.write(json.dumps(self.stats)  + "\n")
        f.write(json.dumps(self.current_games_data) + "\n")
        f.write(json.dumps(self.games_data)  + "\n")
        f.close()
    
    def load_info(self) :
        """
        Loads the player's profile, stats, current games, and games from a file in the "cache" folder.  If the file does not exist, it prints and error message and returns False, resulting in the contructor scraping the data from the API instead.
        """
        if (not os.path.exists("cache/" + self.username + ".json")) :
            print("Attempted to load info from cache for " + self.username + ", but no cache file exists.  Scraping from API instead.")
            return False
        f = open("cache/" + self.username + ".json", "r")
        self.info = json.loads(f.readline())
        self.stats = json.loads(f.readline())
        self.current_games_data = json.loads(f.readline())
        self.games_data = json.loads(f.readline())
        f.close()
    
    def find_games_with_FEN(self, FEN: str) :
        """
        Finds all of the games that contain a given FEN.  This goes through all of the board objects in games (potentially filtered by filter_game_type()) and checks if they contain the given FEN using their contains_FEN() method.  This method simulates through the entire game and checks if the given FEN matches at any point throughout the game.

        Parameters
        ----------
        FEN : str
            the given FEN to search for
        
        Returns
        -------
        list
            the games that "contain" (refer to the contains_FEN() method in the Board class) the given FEN
        """
        games = []
        for board in self.games :
            if (board.contains_FEN(FEN)) :
                games.append(board)
        return games
    
    def find_games_with_FEN_and_Color(self, FEN: str, is_white: bool) :
        """
        Finds all of the games that contain a given FEN and where the player is white (if is_white bool is True) or black (if is_white bool is False) using the find_games_with_FEN() method.

        Parameters
        ----------
        FEN : str
            the given FEN to search for
        is_white : bool
            whether the player is white or black
        
        Returns
        -------
        list
            the games that "contain" (refer to the contains_FEN() method in the Board class) the given FEN and where the player is (color)
        """
        games = []
        for board in self.games :
            if (board.contains_FEN(FEN) and ((board.white_player == self.username) == (is_white == True))) :
                games.append(board)
        return games
    
    #goes through all games, where the player is (color), and finds their most common moves (with frequency) after that FEN
    def find_moves_after_FEN(self, FEN: str, is_white: bool) :
        """
        Goes through all games, where the player is white (if is_white bool is True) or black (if is_white bool is False), and finds their most common moves (with frequency) after that FEN.  This method uses the find_games_with_FEN_and_Color() method to find the games, and then uses the getNextMove() method from the Board class to find the next move in the game.  It then sorts the moves and frequencies by frequency using the sortMovesAndFrequencies() method.

        Parameters
        ----------
        FEN : str
            the given FEN to search for
        is_white : bool
            whether the player is white or black

        Returns
        -------
        list
            the list of moves (sorted by frequency) after the given FEN
        list
            the list of frequencies (sorted by frequency)
        """
        moves = []
        frequencies = []
        games = self.find_games_with_FEN(FEN)
        for game in games :
            if ((game.white_player == self.username) == (is_white == True)) : #game matches
                next_move = game.get_next_move().uci() #gets next move from game and uses .uci() to convert it to a readable string (ex. Move.from_uci('b1c3') -> b1c3)
                if (next_move in moves) :
                    frequencies[moves.index(next_move)] += 1
                else :
                    moves.append(next_move)
                    frequencies.append(1)
        return sort_moves_and_frequencies(moves, frequencies)
    
    def move_table(self, FEN: str, is_white: bool) :
        """
        Returns a printable table of the most frequent moves after a given FEN, where the player is white (if is_white bool is True) or black (if is_white bool is False).  This method uses the find_moves_after_FEN() method to find the moves and frequencies, and then formats them into a printable table.  Ex:
        g1f3: 158
        d1h5: 27
        d2d4: 26
        
        Parameters
        ----------
        FEN : str
            the given FEN to search for
        is_white : bool
            whether the player is white or black

        Returns
        -------
        str
            the printable table of the most frequent moves after the given FEN, where the player is white (if is_white bool is True) or black (if is_white bool is False)
        """
        moves, frequencies = self.find_moves_after_FEN(FEN, is_white)
        s = ""
        for i in range(len(moves)) :
            s += (str(moves[i]) + ": " + str(frequencies[i])) + "\n"
        return s[-1]
    
    def most_common_move(self, FEN: str, is_white: bool) :
        """
        Returns the most frequent move after a given FEN, where the player is white (if is_white bool is True) or black (if is_white bool is False).  This method uses the find_moves_after_FEN() method to find the moves and frequencies, and then returns the first move in the list of moves (which is the most frequent move).

        Parameters
        ----------
        FEN : str
            the given FEN to search for
        is_white : bool
            whether the player is white or black

        Returns
        -------
        Move
            the most frequent move after the given FEN, where the player is white (if is_white bool is True) or black (if is_white bool is False)
        """
        moves, _ = self.find_moves_after_FEN(FEN, is_white)
        return moves[0]
    
    def get_white_games(self) :
        """
        Returns a list of all of the games where the player is white (using the games list, which might be filtered)
        """
        temp = []
        for game in self.games :
            if (game.white_player == self.username) :
                temp.append(game)
        return temp
        
    
    def get_black_games(self) :
        """
        Returns a list of all of the games where the player is black (using the games list, which might be filtered)
        """
        temp = []
        for game in self.games :
            if (game.black_player == self.username) :
                temp.append(game)
        return temp