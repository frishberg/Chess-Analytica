from chess_analytica import Board, ChessDotCom

profile = ChessDotCom.Profile("AKumarforchess", True)
moves, f = profile.find_moves_after_FEN("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R", True)
print(str(f))