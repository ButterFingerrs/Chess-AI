from chess_piece import Piece
import pygame

def map_images_with_pieces():
    piece_images = {}
    piece_images["wP"] = pygame.image.load("assets/white_pawn.png")
    piece_images["bP"] = pygame.image.load("assets/black_pawn.png")
    piece_images["wR"] = pygame.image.load("assets/white_rook.png")
    piece_images["bR"] = pygame.image.load("assets/black_rook.png")
    piece_images["wB"] = pygame.image.load("assets/white_bishop.png")
    piece_images["bB"] = pygame.image.load("assets/black_bishop.png")
    piece_images["wK"] = pygame.image.load("assets/white_knight.png")
    piece_images["bK"] = pygame.image.load("assets/black_knight.png")
    piece_images["wKing"] = pygame.image.load("assets/white_king.png")
    piece_images["bKing"] = pygame.image.load("assets/black_king.png")
    piece_images["wQ"] = pygame.image.load("assets/white_queen.png")
    piece_images["bQ"] = pygame.image.load("assets/black_queen.png")
    piece_images["move"] = pygame.image.load("assets/move.png")
    return piece_images
def potential_check(move, whiteChance, board, king_pos, i, j):
    temp_board = [[Piece(0,-1,None) for x in range(8)] for y in range(8)]
    for a in range(8):
       for b in range(8):
          temp_board[a][b] = board[a][b]
    temp_board[move[1]][move[0]] = temp_board[i][j]
    temp_king_pos = [king_pos[o] for o in range(2)]
    if temp_board[i][j].type == 10:
       tup = (move[1], move[0])
       temp_king_pos[1-temp_board[i][j].color] = tup
    temp_board[i][j] = Piece(0,-1,None)
    if isCheck( not whiteChance, temp_board, temp_king_pos):
       return True
    return False

def isCheck(whiteChance, board, king_pos):
    color = 0
    pos = king_pos[0]
    if whiteChance:
        color = 1
        pos = king_pos[1]
    for i  in range(8):
        for j in range(8):
            if board[i][j].color==color:
               moves = board[i][j].get_possible_valid_moves(j, i, board)
               for move in moves:
                  if move[0]==pos[1] and pos[0]==move[1]:
                    return True
    return False

def isStaleMate(whiteChance, board, king_pos):
    color = 0
    pos = king_pos[0]
    if whiteChance:
        color = 1
        pos = king_pos[1]
    for i  in range(8):
        for j in range(8):
            if board[i][j].color==color:
               moves = board[i][j].get_possible_valid_moves(j, i, board)
               if len(moves)!=0:
                   return False
    return True

def isCheckMate(whiteChance, board, king_pos):
    color = 0
    pos = king_pos[0]
    if whiteChance:
        color = 1
        pos = king_pos[1]
    for i  in range(8):
        for j in range(8):
            if board[i][j].color==color:
               moves = board[i][j].get_possible_valid_moves(j, i, board)
               for move in moves:
                    temp_board = [[Piece(0,-1,None) for x in range(8)] for y in range(8)]
                    for a in range(8):
                        for b in range(8):
                            temp_board[a][b] = board[a][b]
                    temp_board[move[1]][move[0]] = temp_board[i][j]
                    temp_king_pos = [king_pos[o] for o in range(2)]
                    if temp_board[i][j].type == 10:
                        tup = (move[1], move[0])
                        temp_king_pos[1-temp_board[i][j].color] = tup
                    temp_board[i][j] = Piece(0,-1,None)
                    if not isCheck( not whiteChance, temp_board, temp_king_pos):
                        return False
    return True
