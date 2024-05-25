from util import potential_check, map_images_with_pieces
import random
from chess_piece import Piece

class Bot:
    def __init__(self, color) -> None:
        self.color = color
        self.score = 0
        self.piece_images = map_images_with_pieces()

    def apply_move(self, king_Pos, selected_move, board, row, col, piece, score):
        if piece.type == 10:
            tup = (selected_move[1], selected_move[0])
            king_Pos[1-piece.color] = tup
        exPiece = board[selected_move[1]][selected_move[0]]
        score += pow(-1, exPiece.color)*exPiece.type
        board[row][col] = Piece(0,-1,None)
        board[selected_move[1]][selected_move[0]] = piece
        if piece.type == 1 and selected_move[1]==7*(1-piece.color):
            board[selected_move[1]][selected_move[0]] = Piece(8, piece.color, self.piece_images['wQ' if piece.color==1 else 'bQ'])
        self.score = score
        return score
    def copy_board(self, board):
        score = 0
        temp_board = [[Piece(0,-1,None) for x in range(8)] for y in range(8)]
        for a in range(8):
            for b in range(8):
                temp_board[a][b] = board[a][b]
                score+=(-1)*pow(-1, board[a][b].color)*board[a][b].type
        return temp_board, score
    
    def get_pieces(self, board):
        pieces = []
        for a in range(8):
            for b in range(8):
                if board[a][b].color == self.color:
                    pieces.append((board[a][b], b, a))
        return pieces
    def pick_best_move(self, board, king_Pos, pieces): 
        best_move = None
        _, curScore = self.copy_board(board)
        best_pieces = []
        best_moves = []
        for index in range(len(pieces)):
            piece = pieces[index][0]
            potential_moves = piece.get_possible_valid_moves(pieces[index][1],pieces[index][2], board)
            final_moves = []
            for move in potential_moves:
                if not potential_check(move, self.color==1, board, king_Pos, pieces[index][2],pieces[index][1]):
                    final_moves.append(move)
            if len(final_moves)==0:
                continue
            temp_board, curScore = self.copy_board(board) 
            best_score = float('-inf') if piece.color == 1 else float('inf')
            best_move = final_moves[0]
            for move in final_moves:
                curScore = self.apply_move(king_Pos, move, temp_board, pieces[index][2], pieces[index][1], piece, curScore)
                if piece.color == 1:
                    if curScore > best_score:
                        best_score = curScore
                        best_moves.append(move)
                        best_pieces.append(pieces[index])
                    elif curScore==best_score:
                        best_pieces.append(pieces[index])
                        best_moves.append(move)
                else:
                    if curScore < best_score:
                        best_score = curScore
                        best_moves = []
                        best_pieces = []
                        best_moves.append(move)
                        best_pieces.append(pieces[index])
                    elif curScore==best_score:
                        best_pieces.append(pieces[index])
                        best_moves.append(move)
        
        if len(best_moves)!=0:
            print(len(best_pieces))
            ind = random.randint(0, len(best_moves)-1)
            self.apply_move(king_Pos, best_moves[ind], board, best_pieces[ind][2], best_pieces[ind][1], best_pieces[ind][0], curScore)
        return best_move
    
    def make_move(self, board, king_Pos):
        pieces = self.get_pieces(board)
        self.pick_best_move(board, king_Pos, pieces)         