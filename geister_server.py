class Server:
    """Server class for Geister"""

    def __init__(self):
        self.player = [Player() for i in range(2)]
        self.board = Board(player)

    def turn(self):
        pass

class Board:
    SIZE = 6
    
    """
      1st turn(0)
     0 1 2 3 4 5
    0  h g f e
    1  d c b a
    2
    3
    4  a b c d
    5  e f g h
      2nd turn(1)

    (-1,-1) = outside
    """
    def __init__(self):
        self.board = [None for i in range(Board.SIZE*Board.SIZE)]
        self.player = [None, None]

    def set_player(self, player, turn):
        """
        player
        turn: 0 or 1
        """
        for item in player.items.values():
            x = item.x
            y = item.y
            if turn == 0:
                x = 5 - x
                y = 5 - y
            self.board[y * Board.SIZE + x] = item
            self.player[turn] = player

    def print_board(self):
        print("  0 1 2 3 4 5")
        for y in range(0, 6):
            print(y, end=" ")
            for x in range(0, 6):
                item = self.board[y * Board.SIZE + x]
                s = " "
                if item != None:
                    s = item.name
                    if item.player == self.player[0]:
                        s = s.lower()
                print(s, end=" ")
            print("")

class Player:
    """ A base class of Geister player """
    
    def __init__(self):
        """
        initialize items for the player
         ABCD
         EFGH
        """
        self.items = {}
        for i in range(8):
            n = chr(ord("A")+i)
            x = i % 4 + 1
            y = i // 4 + 4
            self.items[n] = Item(self, n, x, y)

    def set_item_colors(self, lst, color):
        for i in lst:
            self.items[i].setColor(color)

    def move_item(self, n, d):
        """
        @n: target item name
        @d: move direction
        """
        self.items[n].move(d)

class Direction:
    NORTH = 0
    EAST = 1
    WEST = 2
    SOUTH = 3

class Item:
    """Definition of Item"""

    def __init__(self, player, name, x, y):
        self.player = player
        self.name = name
        self.x = x
        self.y = y
        self.color = ItemColor.BLUE
        self.get_items = []

    def move(self, d):
        """
        d: move direction
        """
        if self.x == 0 and self.y == 0 and (d == Direction.NORTH or d == Direction.WEST):
            self.x = -2
            self.y = -2
            return True
        elif self.x == 5 and self.y == 0 and (d == Direction.NORTH or d == Direction.EAST):
            self.x = -2
            self.y = -2
            return True
        elif direction == Direction.NORTH and self.y > 1:
            self.y = self.y - 1
            return True
        elif direction == Direction.EAST and self.x < 5:
            self.x = self.x + 1
            return True
        elif direction == Direction.WEST and self.x > 1:
            self.x = self.x - 1
            return True
        elif direction == Direction.SOUTH and self.y < 5:
            self.y = self.y + 1
            return True
        else:
            return False

    def setColor(self, color):
        self.color = color

    def color(self):
        self.color

class ItemColor:
    RED = 1
    BLUE = 2


