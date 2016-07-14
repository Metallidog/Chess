class Square:
    def __init__(self, color, name, location):
        self.color = color
        self.name = name
        self.location = location
        self.occupant = None
        self.clear()
        
    def __repr__(self):
        return self.occupant.name if self.occupant else '|     {}    |'.format(self.name)

    def add_occupant(self, occupant):
        self.occupant = occupant

    def del_occupant(self, board_list):
        if self.occupant:
            board_list.remove(self.occupant)

    def clear(self):
        """
        After every move made on the board, these paramaters need to be
        cleared so that they me be re-evaluated with new piece locations.
        """
        self.looked_at_by = []
        self.occupant = None

class Board:
    def __init__(self):
        self.grid = []
        self.piece_list = []
        self.populate_board()
        
    def print_board(self):
        print ("\n\n\n\n")
        for row in self.grid:
            for square in row:
                print (square, end = '')
            print ('\n\n')

    def populate_board(self):
        """
        Creates and adds all the empty Square objects to the board grid
        """
        for row in range(8):
            self.grid.append([])
            for col in range(8):
                color = "White" if (col + row)%2==0 else "Black"
                name = str(8-row) + 'ABCDEFGH'[col]
                location = (row, col)
                self.grid[row].append(Square(color, name, location))       
        
    def populate_squares(self):
        """
        Iterates through boards piece_list and adds that piece to it's Square
        """
        for piece in self.piece_list:
            r, c = piece.square.location
            self.grid[r][c].add_occupant(piece)  
            
    def all_pieces_build_moves(self):
        for piece in self.piece_list:
            piece.build_moves(self)
            
    def clear_squares(self):
        for row in self.grid:
            for square in row:
                square.clear()

    def new_game(self):
        """
        Creates all the piece objects.
        Creates a board piece_list filled with all the pieces in starting positions.
        Calls populate_squares to put the pieces on the Square objects.
        Calls all_pieces_build_moves to get starting attributes for pieces
        """
        majors = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            self.piece_list.extend([majors[col](' Black', self.grid[0][col]),
                                    Pawn(' Black', self.grid[1][col]),
                                    Pawn(' White', self.grid[6][col]),
                                    majors[col](' White', self.grid[7][col])
                                    ])
        self.populate_squares()
        self.all_pieces_build_moves()
        
    def custom_game(self):
        pass

class Piece:
    def __init__(self, color, square):
        self.color = color
        self.square = square
        self.board_limits = [-1, -2, 8, 9]
        self.first_move = True
        self.clear()
        
    def clear(self):
        self.avail_moves = []
        self.attacking = []
        self.defending = []
        self.attacked_by = []
        self.defended_by = []

    def builder(self, move_type, direction, board):
        x = direction[0] + self.square.location[0]
        y = direction[1] + self.square.location[1]
        if move_type == 'slide':
            while True:
                if self.move_builder(x, y, board):
                    return
                x += direction[0]
                y += direction[1]
        else:
            self.move_builder(x, y, board)
            
    def move(self,  to_square, board):
        self.first_move = False
        to_square.del_occupant(board.piece_list)
        self.square = to_square
        board.clear_squares()
        board.populate_squares()       
        board.all_pieces_build_moves()
        
    def move_builder(self, x, y, board):
        if x in self.board_limits or y in self.board_limits:
            return 1
        board_square = board.grid[x][y]
        if board_square.occupant:
            if board_square.occupant.color == self.color:
                self.defending.append(board_square)
                board_square.occupant.defended_by.append(self)
                return 1
            else:
                self.attacking.append(board_square)
                board_square.occupant.attacked_by.append(self)
                self.avail_moves.append(board_square)
                return 1
        else:
            self.avail_moves.append(board_square)
            board.grid[x][y].looked_at_by.append(self)
            return 0

class Rook(Piece):
    DIRECTIONS = [(-1,0), (1,0), (0,1), (0,-1)]
    def __init__(self, *args):
        Piece.__init__(self, *args)
        self.name = self.color + ' Rook  '

    def build_moves(self, board):
        for direction in Rook.DIRECTIONS:
            self.builder('slide', direction, board)

class Bishop(Piece):
    DIRECTIONS = [(-1,-1), (1,-1), (1,1), (-1,1)]
    def __init__(self, *args):
        Piece.__init__(self, *args)
        self.name = self.color + ' Bishop'
        
    def build_moves(self, board):
        for direction in Bishop.DIRECTIONS:
            self.builder('slide', direction, board)

class Queen(Piece):
    DIRECTIONS = Bishop.DIRECTIONS + Rook.DIRECTIONS
    def __init__(self, *args):
        Piece.__init__(self, *args)
        self.name = self.color + ' Queen '    
        
    def build_moves(self, board):
        for direction in Queen.DIRECTIONS:
            self.builder('slide', direction, board)

class Knight(Piece):
    DIRECTIONS = [(-1, -2), (-1, 2), (-2, 1), (-2, -1),
                  (1, -2), (1, 2), (2, 1), (2, -1)]
    def __init__(self, *args):
        Piece.__init__(self, *args)
        self.name = self.color + ' Knight'
    
    def build_moves(self, board):
        for direction in Knight.DIRECTIONS:
            self.builder('step', direction, board)        

class King(Piece):
    DIRECTIONS = Queen.DIRECTIONS
    def __init__(self, *args):
        Piece.__init__(self, *args)
        self.name = self.color + ' King  '
        self.castle = False
        
    def build_moves(self, board):
        for direction in King.DIRECTIONS:
            self.builder('step', direction, board)
            
        if self.first_move:
            pass
            #x = self.square.location[0]
            #if board.grid[x][0].occupant.first_move:
            #    if not board.grid[x][1].occupant and not board.grid[x][2].occupant \
            #                                     and not board.grid[x][3].occupant:
            #        self.avail_moves.append(board.grid[x][2])
                    
class Pawn(Piece):
    def __init__(self, *args):
        Piece.__init__(self, *args)
        self.name = self.color + ' Pawn  '
        self.en_passant = False
        self.direction = 1 if self.color==' Black' else -1
        
    def build_moves(self, board):
        x, y = self.square.location[0], self.square.location[1]
        forward = x+self.direction
        attack_locations = [(forward, y+1), (forward, y-1)]
        
        if self.first_move and not self.check_square((forward, y), board)\
            and not self.check_square((forward+self.direction, y), board):
            self.avail_moves = [board.grid[forward][y], 
                                board.grid[forward+self.direction][y]]
                                
        elif not self.check_square((forward, y), board):
            self.avail_moves.append(board.grid[forward][y])
                
        for look in attack_locations:
            if look[0] not in self.board_limits and look[1] not in self.board_limits:
                square_occupant = self.check_square(look, board)
                if square_occupant == 'enemy':
                    self.attacking.append(board.grid[look[0]][look[1]])
                    self.avail_moves.append(board.grid[look[0]][look[1]])
                    board.grid[look[0]][look[1]].occupant.attacked_by.append(self)
                elif square_occupant == 'ally':
                    self.defending.append(board.grid[look[0]][look[1]])
                    board.grid[look[0]][look[1]].occupant.defended_by.append(self)
                else:
                    board.grid[look[0]][look[1]].looked_at_by.append(self)
        
    def check_square(self, location, board):
        oc = board.grid[location[0]][location[1]].occupant
        if oc:
            if oc.color == self.color:
                return 'ally'
            else:
                return 'enemy'
        else:
            return None
 
##########################################################################

board = Board()
board.new_game()
 
def get_input():
    fromx, fromy = (x for x in input("from "))
    fromx = 8 - int(fromx)
    fromy = 'ABCDEFGH'.index(fromy.upper())
    print (fromx, fromy)
    tox, toy = (x for x in input("to "))
    tox = 8 - int(tox)
    toy = 'ABCDEFGH'.index(toy.upper())                
    print (tox, toy)    
    return fromx, fromy, tox, toy    
    
while True:
    board.print_board()          
    #for piece in board.piece_list:
     #   piece.build_moves(board)            
    input("pause")
    for r in range(8):
        for c in range(8):
            if board.grid[r][c].occupant:
                print (board.grid[r][c].name, "avail moves", *(o.name for o in board.grid[r][c].occupant.avail_moves))
                print (board.grid[r][c].name, "defending", *(o.name for o in board.grid[r][c].occupant.defending))
                print (board.grid[r][c].name, "attacking", *(o.name for o in board.grid[r][c].occupant.attacking))                
                print (board.grid[r][c].name, "defended by", *(o.square.name for o in board.grid[r][c].occupant.defended_by))
                print (board.grid[r][c].name, "attacked by", *(o.square.name for o in board.grid[r][c].occupant.attacked_by))
    fromx, fromy, tox, toy = get_input()            
    
    for r in range(8):
        for c in range(8):
            if board.grid[r][c].occupant:
                board.grid[r][c].occupant.clear()
            else:
                board.grid[r][c].clear()
    board.grid[fromx][fromy].occupant.move(board.grid[tox][toy], board)  
    

    
