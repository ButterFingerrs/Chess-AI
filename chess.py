from sys import exit    
from chess_piece import Piece
import pygame
from bot import Bot
from util import potential_check, isCheck, isCheckMate, map_images_with_pieces, isStaleMate
width = 700
height = 700
brown = (185,222,87)
selected_color = (175,222,188)
piece_images = map_images_with_pieces()
def draw_board():
    for row in range(8):
        for col in range(8):
            if (row%2!=0 and col%2==0) or (row%2==0 and col%2!=0):
                pygame.draw.rect(screen, brown, (col * width // 8, row * height // 8, width // 8, height // 8))
            else:
                pygame.draw.rect(screen, black, (col * width // 8, row * height // 8, width // 8, height // 8))
         
def select_tile(row, col):
    pygame.draw.rect(screen, selected_color, (col * width // 8, row * height // 8, width // 8, height // 8))

def unselect_tile(row, col):
    if (row%2!=0 and col%2==0) or (row%2==0 and col%2!=0):
      pygame.draw.rect(screen, brown, (col * width // 8, row * height // 8, width // 8, height // 8))
    else:
      pygame.draw.rect(screen, black, (col * width // 8, row * height // 8, width // 8, height // 8))
      
def draw_pieces(board):
  for row in range(8):
    for col in range(8):
      piece = board[row][col]
      if piece.type!=0:
        image = piece.image
        image = pygame.transform.scale(image, (width//12, height//12))
        screen.blit(image, (col * width // 8 +10, row * height // 8 +10))

def get_clicked_tile():
    mouse_position = pygame.mouse.get_pos()
    click_row = 0
    click_col = 0
    while click_row*height//8 <mouse_position[0]:
        click_row+=1
    while click_col*width//8 <mouse_position[1]:
        click_col+=1
    click_col-=1
    click_row-=1
    return (click_row, click_col)

def draw_potential_move(row, col):
    piece = board[row][col]
    image = piece_images["move"]
    image = pygame.transform.scale(image, (width//17, height//17))
    screen.blit(image, (col * width // 8 +10, row * height // 8 +10))

def draw_potential_moves(moves):
   for move in moves:
       draw_potential_move(move[1], move[0])

def select_piece(selected_tile):
    global whiteChance, board, tileSelected
    final_moves = []
    if board[selected_tile[1]][selected_tile[0]].type!=0:
        if (whiteChance == True and board[selected_tile[1]][selected_tile[0]].color==1) or (whiteChance==False and board[selected_tile[1]][selected_tile[0]].color==0):
            select_tile(selected_tile[1], selected_tile[0])
            potential_moves = board[selected_tile[1]][selected_tile[0]].get_possible_valid_moves(selected_tile[0],selected_tile[1], board)
            for move in potential_moves:
                if not potential_check(move, whiteChance, board, king_Pos, selected_tile[1],selected_tile[0]):
                    final_moves.append(move)
        tileSelected = True
        return final_moves
    else:
        tileSelected = False
        return []
    
def make_move(final_moves, selected_move):
    global checkMate, whiteChance, king_Pos, selected_tile, board, tileSelected
    if selected_move in final_moves and board[selected_tile[1]][selected_tile[0]].color!= board[selected_move[1]][selected_move[0]].color:
        piece = board[selected_tile[1]][selected_tile[0]]
        if piece.type == 10:
            tup = (selected_move[1], selected_move[0])
            king_Pos[1-board[selected_tile[1]][selected_tile[0]].color] = tup
        board[selected_tile[1]][selected_tile[0]] = Piece(0,-1,None)
        board[selected_move[1]][selected_move[0]] = piece
        if piece.type == 1 and selected_move[1]==7*(1-piece.color):
            board[selected_move[1]][selected_move[0]] = Piece(8, piece.color, piece_images['wQ' if piece.color==1 else 'bQ'])
        whiteChance = not whiteChance
    tileSelected = False
    return board
staleMate = False
def end_screen():
    global checkMate, board, staleMate
    winner = 'Black' if checkMate==1 else 'White'
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    board = [[Piece(5, 0, piece_images['bR']),Piece(3, 0, piece_images['bK']),
                        Piece(4, 0, piece_images['bB']),Piece(8, 0, piece_images['bQ']),
                        Piece(10, 0, piece_images['bKing']),Piece(4, 0, piece_images['bB']),
                        Piece(3, 0, piece_images['bK']),Piece(5, 0, piece_images['bR'])],
                        [Piece(1, 0, piece_images['bP']),Piece(1, 0, piece_images['bP']),
                        Piece(1, 0, piece_images['bP']),Piece(1, 0, piece_images['bP']),
                        Piece(1, 0, piece_images['bP']),Piece(1, 0, piece_images['bP']),
                        Piece(1, 0, piece_images['bP']),Piece(1, 0, piece_images['bP']),],
                        [Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None)],
                        [Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None)],
                        [Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None)],
                        [Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None),
                        Piece(0, -1, None),Piece(0, -1, None)],
                        [Piece(1, 1, piece_images['wP']),Piece(1, 1, piece_images['wP']),
                        Piece(1, 1, piece_images['wP']),Piece(1, 1, piece_images['wP']),
                        Piece(1, 1, piece_images['wP']),Piece(1, 1, piece_images['wP']),
                        Piece(1, 1, piece_images['wP']),Piece(1, 1, piece_images['wP']),],
                        [Piece(5, 1, piece_images['wR']),Piece(3, 1, piece_images['wK']),
                        Piece(4, 1, piece_images['wB']),Piece(8, 1, piece_images['wQ']),
                        Piece(10, 1, piece_images['wKing']),Piece(4, 1, piece_images['wB']),
                        Piece(3, 1, piece_images['wK']),Piece(5, 1, piece_images['wR'])]]
                    checkMate = 0
                    pygame.draw.rect(screen, black, (0, 0, width, height))
                    draw_board()
                    return
        largeFont = pygame.font.SysFont('comicsans', 40)
        color = (255, 255, 255) if winner=='White' else (0, 0, 0)
        if staleMate:
            drawDisplay = largeFont.render("Draw by stalemate", 1, (255,255,255))
            screen.blit(drawDisplay, (width/2-drawDisplay.get_width()/2, 200))
        else:
            winnerDisplay = largeFont.render(winner + ' Won the game!!', 1, color)
            screen.blit(winnerDisplay, (width/2-winnerDisplay.get_width()/2, 200))
        largeFont = pygame.font.SysFont('comicsans', 30)
        restart = largeFont.render('Press Enter to restart the game', 1, (255, 255, 255))
        screen.blit(restart, (width/2-restart.get_width()/2, 300))
        pygame.display.update()
        clock.tick(60)

map_images_with_pieces()
board = [[Piece(5, 0, piece_images['bR']),Piece(3, 0, piece_images['bK']),
          Piece(4, 0, piece_images['bB']),Piece(8, 0, piece_images['bQ']),
          Piece(10, 0, piece_images['bKing']),Piece(4, 0, piece_images['bB']),
          Piece(3, 0, piece_images['bK']),Piece(5, 0, piece_images['bR'])],
          [Piece(1, 0, piece_images['bP']),Piece(1, 0, piece_images['bP']),
           Piece(1, 0, piece_images['bP']),Piece(1, 0, piece_images['bP']),
           Piece(1, 0, piece_images['bP']),Piece(1, 0, piece_images['bP']),
           Piece(1, 0, piece_images['bP']),Piece(1, 0, piece_images['bP']),],
           [Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None)],
          [Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None)],
          [Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None)],
          [Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None),
           Piece(0, -1, None),Piece(0, -1, None)],
          [Piece(1, 1, piece_images['wP']),Piece(1, 1, piece_images['wP']),
           Piece(1, 1, piece_images['wP']),Piece(1, 1, piece_images['wP']),
           Piece(1, 1, piece_images['wP']),Piece(1, 1, piece_images['wP']),
           Piece(1, 1, piece_images['wP']),Piece(1, 1, piece_images['wP']),],
        [Piece(5, 1, piece_images['wR']),Piece(3, 1, piece_images['wK']),
          Piece(4, 1, piece_images['wB']),Piece(8, 1, piece_images['wQ']),
          Piece(10, 1, piece_images['wKing']),Piece(4, 1, piece_images['wB']),
          Piece(3, 1, piece_images['wK']),Piece(5, 1, piece_images['wR'])]]
black = (94,94,94)
selected_tile = ()
prev_tile = ()
tileSelected = False
potential_moves = []
whiteChance = True
king_Pos = [(7,4),(0,4)]
checkMate = 0
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((width,height))
draw_board()
black_bot = Bot(0)
white_bot = Bot(1)
number_of_moves = 0
while True:
    if checkMate>0:
        number_of_moves = 0
        end_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type ==pygame.MOUSEBUTTONDOWN:
            if tileSelected:
                selected_move = get_clicked_tile()
                make_move(final_moves, selected_move)
                if isCheck(not whiteChance, board, king_Pos):
                    if isCheckMate(whiteChance, board, king_Pos):
                        checkMate = 1 if whiteChance else 2
                draw_board()
                prev_tile = selected_tile
            if len(prev_tile)==2:
                unselect_tile(prev_tile[1], prev_tile[0])
            selected_tile = get_clicked_tile()
            final_moves = select_piece(selected_tile)
            draw_potential_moves(final_moves)
    if not whiteChance:
        black_bot.make_move(board, king_Pos)
        whiteChance = not whiteChance
        if isStaleMate(not whiteChance, board, king_Pos):
            staleMate = True
            end_screen()
        if isCheck(not whiteChance, board, king_Pos):
            if isCheckMate(whiteChance, board, king_Pos):
                checkMate = 1 if whiteChance else 2
        number_of_moves+=1
        draw_board()
    if whiteChance:
        white_bot.make_move(board, king_Pos)
        whiteChance = not whiteChance
        if isStaleMate(not whiteChance, board, king_Pos):
            staleMate = True
            end_screen()
        if isCheck(not whiteChance, board, king_Pos):
            if isCheckMate(whiteChance, board, king_Pos):
                checkMate = 1 if whiteChance else 2
        number_of_moves+=1
        draw_board()
    draw_pieces(board)
    pygame.display.update()
    clock.tick(60)