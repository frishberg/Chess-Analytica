import chess.pgn
import io

def retrieve_info(PGN: str) :
    """
    Function that takes in the PGN (in the format provided by the Chess.com API) and extracts info about the game including the date, white player, black elo, time control, etc...

    Parameters
    ----------
    PGN : str
        the PGN (in the format provided by the Chess.com API) of the game, which includes info about the game
    
    Returns
    -------
    date : str
        the date of the game
    white_player : str
        the white player of the game
    black_player : str
        the black player of the game
    white_elo : str
        the elo of the white player
    black_elo : str
        the elo of the black player
    time_control : str
        the time restriction of the game (ex. 10 minute rapid game or 600 seconds)
    termination : str
        how the game ended (ex. aronfrish won by resignation)
    start_time : str
        the UTC start time of the game (ex. 8:34:58)
    end_time : str
        the UTC end time of the game (ex. 8:36:15)
    link : str
        the link to the game on chess.com
    time_length : int
        the length of the game in seconds
        
    """
    PGN = PGN[PGN.index("Date")+6:]
    date = PGN[:PGN.index('"')]
    PGN = PGN[PGN.index("White")+7:]
    white_player = PGN[:PGN.index('"')]
    PGN = PGN[PGN.index("Black")+7:]
    black_player = PGN[:PGN.index('"')]
    PGN = PGN[PGN.index("WhiteElo")+10:]
    white_elo = int(PGN[:PGN.index('"')])
    PGN = PGN[PGN.index("BlackElo")+10:]
    black_elo = int(PGN[:PGN.index('"')])
    PGN = PGN[PGN.index("TimeControl")+13:]
    time_control = PGN[:PGN.index('"')]
    PGN = PGN[PGN.index("Termination")+13:]
    termination = PGN[:PGN.index('"')]
    PGN = PGN[PGN.index("StartTime")+12:]
    start_time = PGN[:PGN.index('"')]
    PGN = PGN[PGN.index("EndTime")+10:]
    end_time = PGN[:PGN.index('"')]
    PGN = PGN[PGN.index("Link")+6:]
    link = PGN[:PGN.index('"')]
    time_length = calculate_time_length(start_time, end_time)
    return date, white_player, black_player, white_elo, black_elo, time_control, termination, start_time, end_time, link, time_length

def calculate_time_length(start_time: str, end_time: str) :
    """
    Function that takes in the start time and end time of a game and calculates the length of the game in seconds

    Parameters
    ----------
    start_time : str
        the UTC start time of the game (ex. 8:34:58)
    end_time : str
        the UTC end time of the game (ex. 8:36:15)
    
    Returns
    -------
    time_length : int
        the length of the game in seconds
    """
    start_time = start_time.split(":")
    end_time = end_time.split(":")
    start_time = [int(x) for x in start_time]
    end_time = [int(x) for x in end_time]
    time_length = (end_time[0]-start_time[0])*3600 + (end_time[1]-start_time[1])*60 + (end_time[2]-start_time[2])
    return time_length

def extract_winner(termination) :
    if "Game drawn" in termination :
        return "draw"
    return termination[:termination.index(" ")]

class Board :
    """
    Board class that represents a chess.com game.  Each object contains data, such start time, end time, the white player, the elo of the black playey, and so on.
    The board also has several methods to help with the analysis of boards.  This includes the move method, which simulates a move 
    of the board, as well as the reset method, which resets the board to its original state.  The FEN (Forsyth–Edwards Notation) and next move can be retrieved at any time as well.

    Paramters
    ----------
    PGN : str
        the PGN of the game (in the format provided by the Chess.com API) of the game, which includes info about the game

    Attributes
    ----------
    PGN : str
        the PGN of the game (in the format provided by the Chess.com API) of the game, which includes info about the game
    date : str
        the date of the game
    white_player : str
        the white player of the game
    black_player : str
        the black player of the game
    white_elo : str
        the elo of the white player
    black_elo : str
        the elo of the black player
    time_control : str
        the time restriction of the game (ex. 10 minute rapid game or 600 seconds)
    termination : str
        how the game ended (ex. aronfrish won by resignation)
    start_time : str
        the UTC start time of the game (ex. 8:34:58)
    end_time : str
        the UTC end time of the game (ex. 8:36:15)
    link : str
        the link to the game on chess.com
    time_length : int
        the length of the game in seconds
    pgn : io.StringIO
        the PGN of the game, converted to be usable by chess.pgn
    game : chess.pgn.Game
        the game object, created by chess.pgn.read_game
    board : chess.Board
        the board object, using the chess.pgn library
    moves_left : list
        a list of the moves left in the game (length will be reduced as move method is called, but can be reset with reset method)
    final_state : str
        a visual representation of the final state of the board, after all moves have been made
    winner : str
        the winner of the game (ex. aronfrish or draw)
    
    Methods
    -------
    move()
        Simulates a move on the board.  This will pop the first element in moves_left, and push it to the board.  If there are no moves left, an exception will be raised.
    get_board()
        Returns the board object
    get_FEN()
        Returns the FEN of the board, in its current state
    has_move()
        Returns whether there are moves left in the game
    reset()
        Resets the board to the beginning of the game
    contains_FEN(FEN: str)
        Simulates the board through all moves, checking after each move is made to see if the current FEN of the board matches the given FEN.  If it does, the method returns True.  Otherwise, it returns False.  This method is used to check if the state of the game ever matches a given FEN.
    get_next_move()
        Returns the next move in the game
    get_final_state()
        Returns a visual representation of the final state of the board, after all moves have been made
    """

    def __init__(self, PGN: str) :
        """
        Constructor for the Board class.  Takes in the PGN of the game (in the format provided by the Chess.com API) and sets the attributes of the board object, 
        including the board object, PGN, date, white player, black elo, time control, etc... (all of which can be retrieved)
        """
        self.PGN = PGN #storing original PGN
        self.date, self.white_player, self.black_player, self.white_elo, self.black_elo, self.time_control, self.termination, self.start_time, self.end_time, self.link, self.time_length = retrieve_info(PGN)
        self.pgn = io.StringIO(PGN) #converting to be usable by chess.pgn
        self.game = chess.pgn.read_game(self.pgn) #creating game object
        self.board = self.game.board() #creating board object
        self.moves_left = list(self.game.mainline_moves()) #moves left in the game (length will be reduced as move method is called, but can be reset with reset method)
        self.final_state = self.get_final_state() #visual representation of the final state of the board, after all moves have been made
        self.winner = extract_winner(self.termination) #winner of the game (ex. aronfrish or draw)

    def __str__(self) :
        """
        Returns the string representation of the board, which is a visual representation of the board in its current state
        """
        return str(self.board)
    
    def move(self) :
        """
        Simulates a move on the board.  This will pop the first element in moves_left, and push it to the board.  If there are no moves left, an exception will be raised.
        """
        if (len(self.moves_left)<=0) :
            raise Exception("Move method called but no moves left in the game")
        move = self.moves_left.pop(0)
        self.board.push(move)

    def get_board(self) :
        """
        Returns the board object
        """
        return self.board
    
    def get_FEN(self) :
        """
        Returns the FEN (Forsyth–Edwards Notation) of the board, in its current state
        """
        fen = self.board.fen()
        fen = fen[:fen.index(" ")]
        return fen
    
    def has_move(self) :
        """
        Returns whether there are moves left in the game
        """
        return (len(self.moves_left)>0)
    
    def reset(self) :
        """
        Resets the board to the beginning of the game.  This will reset the board to a new state, and reset moves_left to be full of all of the moves of the game again.
        """
        self = self.__init__(self.PGN)

    def contains_FEN(self, FEN: str) :
        """
        Simulates the board through all moves, checking after each move is made to see if the current FEN of the board matches the given FEN.  If it does, the method returns True.  Otherwise, it returns False.  This method is used to check if the state of the game ever matches a given FEN.

        Parameters
        ----------
        FEN : str
            the given FEN to check if the board ever matches

        Returns
        -------
        bool
            True if the board ever matches the given FEN, False otherwise
        """
        self.reset()
        while(self.has_move()) :
            self.move()
            if self.get_FEN()==FEN :
                return True
        return False
    
    def get_next_move(self) :
        """
        Returns the next move in the game
        """
        return self.moves_left[0]
    
    def get_final_state(self) :
        """
        Returns a visual representation of the final state of the board, after all moves have been made 
        """
        temp_board = self.board.copy() #creating temp board. This is necessary because if you simulate all the moves and then reset the board, it will cause an infinite loop, as it will calculate the final state, reinitialize itself, and then calculate the final state again, and so on.
        for move in self.moves_left : #for each move in current board object
            temp_board.push(move) #push the move to the temp board
        final_state = str(temp_board) #get the string representation of the temp board
        return final_state