from tkinter import *

tk = Tk()
canvas = Canvas(tk, width = 400, height = 400)
canvas.pack()


class Square:
     
    def __init__(self, row, col, name):
        self.range = (row*50, col*50, row*50+50, col*50+50)
        #self.text_position = (row+25,col+25)
        self.color = 'light goldenrod' if (col + row)%2==0 else 'orangered'   
        self.name = name
        
    def print_location(self, event):
        print ("square name = {}".format(self.name))
        
    def draw(self):
        self.rectangle = canvas.create_rectangle(self.range, fill=self.color, tags = self.name)
        canvas.tag_bind(self.rectangle, '<Button-1>', self.print_location)
        #canvas.create_text(self.text_position, text=self.name)        
        
class Board:

    def __init__(self):
        self.board_squares = []

    def draw_board(self):
        for hole in self.board_squares:
            hole.draw()

    def init_new_game(self):
        square_names = [c+r for c in 'hgfedcba' for r in '12345678']
        for col in range(0, 8):
            for row in range(0, 8):                
                square = Square(row, col, square_names[col*8+row])
                self.board_squares.append(square)
 
class Game:
    
    def start(self):
        newGame = Board()
        newGame.init_new_game()
        newGame.draw_board()

game = Game()
game.start()

mainloop()