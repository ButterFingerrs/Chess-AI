from sys import exit    
from chess_piece import Piece
import pygame
width = 700
height = 700
brown = (185,222,87)
selected_color = (175,222,188)
piece_images = {}

def map_images_with_pieces():
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

def select_piece():
    global whiteChance, board, selected_tile
    final_moves = []
    if board[selected_tile[1]][selected_tile[0]].type!=0:
        if (whiteChance == True and board[selected_tile[1]][selected_tile[0]].color==1) or (whiteChance==False and board[selected_tile[1]][selected_tile[0]].color==0):
            draw_board()
            select_tile(selected_tile[1], selected_tile[0])
            potential_moves = board[selected_tile[1]][selected_tile[0]].get_possible_valid_moves(selected_tile[0],selected_tile[1], board)
            for move in potential_moves:
                if not potential_check(move, whiteChance, board, king_Pos, selected_tile[1],selected_tile[0]):
                    final_moves.append(move)
            draw_potential_moves(final_moves)
        return True, final_moves
    else:
        draw_board()
        return False, None

def make_move(final_moves, selected_move):
    global checkMate, whiteChance, king_Pos, selected_tile, board
    if selected_move in final_moves and board[selected_tile[1]][selected_tile[0]].color!= board[selected_move[1]][selected_move[0]].color:
        piece = board[selected_tile[1]][selected_tile[0]]
        if piece.type == 10:
            tup = (selected_move[1], selected_move[0])
            king_Pos[1-board[selected_tile[1]][selected_tile[0]].color] = tup
        board[selected_tile[1]][selected_tile[0]] = Piece(0,-1,None)
        board[selected_move[1]][selected_move[0]] = piece
        if piece.type == 1 and selected_move[1]==7*(1-piece.color):
            board[selected_move[1]][selected_move[0]] = Piece(8, piece.color, piece_images['wQ' if piece.color==1 else 'bQ'])
        draw_board()
        if isCheck(whiteChance, board, king_Pos):
            p = "white" if whiteChance else "black"
            print("Check caused by: " + p)
            if isCheckMate(not whiteChance, board, king_Pos):
                checkMate = 2 if whiteChance else 1
                print("Checkmate bro: " + p + " wins")
        whiteChance = not whiteChance
    return False, whiteChance 

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

def end_screen():
    global checkMate, board
    
    winner = 'Black' if checkMate==1 else 'White'
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Restart")
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
        winnerDisplay = largeFont.render(winner + ' Won the game!!', 1, (255, 255, 255))
        largeFont = pygame.font.SysFont('comicsans', 30)
        restart = largeFont.render('Press Enter to restart the game', 1, (255, 255, 255))
        screen.blit(winnerDisplay, (width/2-winnerDisplay.get_width()/2, 200))
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
pygame.init()
screen = pygame.display.set_mode((width,height))
black = (94,94,94)
clock = pygame.time.Clock()
selected_tile = ()
prev_tile = ()
tileSelected = False
potential_moves = []
whiteChance = True
draw_board()
king_Pos = [(7,4),(0,4)]
checkMate = 0
while True:
    if checkMate>0:
        end_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type ==pygame.MOUSEBUTTONDOWN:
            if tileSelected:
                selected_move = get_clicked_tile()
                tileSelected, whiteChance = make_move(final_moves, selected_move)
                prev_tile = selected_tile
            if len(prev_tile)==2:
                unselect_tile(prev_tile[1], prev_tile[0])
            selected_tile = get_clicked_tile()
            tileSelected, final_moves = select_piece()
    draw_pieces(board)
    pygame.display.update()
    clock.tick(60)