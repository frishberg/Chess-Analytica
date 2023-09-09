import unittest
import math
from chess_analytica import Board, ChessDotCom


class ProfileTesting(unittest.TestCase):

    def setUp(self):
        self.profile = ChessDotCom.Profile("aronfrishb", False) #aronfrishb was an old account of mine that is inactive, so the results will be consistent

    def test_user_info(self) :
        self.assertEqual(self.profile.username, "aronfrishb")
        self.assertEqual(self.profile.stats["rapid"]["rating"], 719)
        self.assertEqual(len(self.profile.games), 16)
    
    def test_filter_game_type(self) :
        self.profile.filter_game_type("rapid")
        self.assertEqual(len(self.profile.games), 15)
        self.profile.filter_game_type("all") #resetting filter

    def test_find_games_with_FEN(self) :
        self.assertEqual(len(self.profile.find_games_with_FEN("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R")), 1) #looking for 4 knights game

    def test_find_games_with_FEN_and_Color(self) :
        self.assertEqual(len(self.profile.find_games_with_FEN_and_Color("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R", True)), 1) #looking for 4 knights game as white
        self.assertEqual(len(self.profile.find_games_with_FEN_and_Color("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R", False)), 0) #looking for 4 knights game as black
    
    def find_moves_after_FEN(self) :
        self.assertEqual(len(self.profile.find_moves_after_FEN("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R")), 1)
    
    def test_most_common_move(self) :
        self.assertEqual(self.profile.most_common_move("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R", True), "d2d4")

if __name__ == '__main__':
    unittest.main()