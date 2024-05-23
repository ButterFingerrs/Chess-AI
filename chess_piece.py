class Piece:
    def __init__(self, type, color, image):
        self.type = type
        self.color = color
        self.image = image

    def get_rook_moves(self, row, col, board):
        moves = []
        upLimit = col
        downLimit = 7-col
        leftLimit = row
        rightLimit = 7-row
        for i in range(1, downLimit+1):
            if board[col+i][row].color == self.color:
                break
            moves.append((row, col+i))
            if board[col+i][row].color!=-1:
                break
        for i in range(1, rightLimit+1):
            if board[col][row+i].color == self.color:
                break
            moves.append((row+i, col))
            if board[col][row+i].color!=-1:
                break
        for i in range(1, leftLimit+1):
            if board[col][row-i].color == self.color:
                break
            moves.append((row-i, col))
            if board[col][row-i].color!=-1:
                break
        for i in range(1, upLimit+1):
            if board[col-i][row].color == self.color:
                break
            moves.append((row, col-i))
            if board[col-i][row].color!=-1:
                break
        return moves
    
    def get_bishop_moves(self, row, col, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves = []
        bishop_color = board[col][row].color  # 'w' for white, 'b' for black

        for direction in directions:
            r, c = row, col
            while True:
                r += direction[0]
                c += direction[1]
                if 0 <= r < 8 and 0 <= c < 8:  # Stay within the board
                    if board[c][r].color == -1:
                        moves.append((r, c))
                    elif board[c][r].color == 1-bishop_color:  # Capture opponent piece
                        moves.append((r, c))
                        break
                    else:
                       break  # Same color piece blocks the way
                else:
                    break  # Out of bounds
                
        return moves
    
    def get_queen_moves(self, row, col, board):
        moves = []
        moves += self.get_bishop_moves(row, col, board) + self.get_rook_moves(row, col, board)
        return moves
    
    def get_king_moves(self, row, col, board):
        moves = []
        directions = [(-1,1), (-1,-1), (1,1), (1,-1), (0,1),(0, -1), (1, 0), (-1, 0)]
        for direction in directions:
            rowsInbound = row+direction[0]>=0 and row+direction[0]<8
            colsInbound = col+direction[1]>=0 and col+direction[1]<8
            if rowsInbound and colsInbound:
                if board[col+direction[1]][row+direction[0]].color!=self.color:
                    move = (row+direction[0], col+direction[1])
                    moves.append(move)
        return moves
    
    def get_pawn_moves(self, row, col, board):
        moves = []
        if col==7*(1-self.color):
            return []
        diagonal_left_opponent = False
        if row>0 and board[col+pow(-1, self.color)][row-1].color== 1 - self.color:
            diagonal_left_opponent = True
        diagonal_right_opponent = False
        if row<7 and board[col+pow(-1, self.color)][row+1].color== 1 - self.color:
            diagonal_right_opponent = True
        if (col==6 and self.color==1 and board[4][row].color<0 and board[5][row].color<0) or (self.color==0 and col==1 and board[3][row].color<0 and board[2][row].color<0):
            moves.append((row, col+(pow(-1, self.color))*2))
        if board[col+pow(-1, self.color)][row].color<0:
            moves.append((row, max(0, col+(pow(-1, self.color)))))
        if diagonal_left_opponent:
            moves.append((max(0, row-1), max(0, col+(pow(-1, self.color)))))
        if diagonal_right_opponent:
            moves.append((min(7, row+1), max(0, col+(pow(-1, self.color)))))
       #print("Nascar" + str(moves))
        return moves
    
    def get_knight_moves(self, row, col, board):
        moves = []
        directions = [(-2,1), (-2,-1), (2,1), (2,-1), (-1,2),(-1, -2), (1, 2), (1, -2)]
        for direction in directions:
            rowsInbound = row+direction[0]>=0 and row+direction[0]<8
            colsInbound = col+direction[1]>=0 and col+direction[1]<8
            if rowsInbound and colsInbound:
                if board[col+direction[1]][row+direction[0]].color!=self.color:
                    move = (row+direction[0], col+direction[1])
                    moves.append(move)
        return moves
    
    def get_possible_valid_moves(self, row, col, board):
        moves = []
        if self.type==5:
            moves = self.get_rook_moves(row, col, board)
        if self.type ==4:
            moves = self.get_bishop_moves(row, col, board)
        if self.type==3:
            moves = self.get_knight_moves(row, col,board)
        if self.type ==1:
            moves = self.get_pawn_moves(row, col, board)
        if self.type==8:
            moves = self.get_queen_moves(row, col, board)
        if self.type ==10:
            moves = self.get_king_moves(row, col, board)
        return moves