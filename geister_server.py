
import re

class GeisterServer(object):
    """
    Server class for Geister.
    This is a singleton class.
    """
    
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GeisterServer,cls).__new__(cls)
            cls.__instance.__initialized = False
        return GeisterServer.__instance
    
    def __init__(self):
        if(self.__initialized):
            return
        self.__initialized = True
        self.player = [Player(), Player()]
        self.board = Board(self.player)

    def start(self):
        """
        - open socket for 2 clients
        - attach each player instance for each client
        """
        pass

    def turn(self):
        pass

    __SET_COMMAND = re.compile('^SET:(\w*)')
    __MOV_COMMAND = re.compile('^MOV:(\w*),(\w*)')

    def command(self, mesg, pid):
        print(mesg)
        m = GeisterServer.__SET_COMMAND.match(mesg)
        if m :
            self.player[pid].set_items_color(m.group(1), ItemColor.RED)
            return True
        
        m = GeisterServer.__MOV_COMMAND.match(mesg)
        if m :
            arg = m.group(2)
            d = None
            if arg == "NORTH":
                d = Direction.NORTH
            elif arg == "EAST":
                d = Direction.EAST
            elif arg == "WEST":
                d = Direction.WEST
            elif arg == "SOUTH":
                d = Direction.SOUTH
                
            if d != None:
                r = self.player[pid].move_item(m.group(1), d)
                return r
            else:
                return False
        
        else:
            return False

    def print_board(self):
        self.board.print_board()

class Board:
    SIZE = 6
    ESCAPED_MARK = 8
    TAKEN_MARK = 9
    
    def __init__(self, players):
        self.players = players
        players[0].set_board(self)
        players[1].set_board(self)

    def get_board(self, player):
        """
        player: viewing player
        """
        board = [None for i in range(Board.SIZE*Board.SIZE)]
        for p in self.players:
            for item in p.items.values():
                x = item.x
                y = item.y
                if x > 5:
                    continue # this item is not on board
                if p != player:
                    x = 5 - x
                    y = 5 - y
                board[y * Board.SIZE + x] = item
        return board

    def taken_items(self):
        lst = []
        for p in self.players:
            for item in p.items.values():
                if item.x == Board.TAKEN_MARK:
                    lst.append(item)
        return lst

    def escaped_items(self):
        lst = []
        for p in self.players:
            for item in p.items.values():
                if item.x == Board.ESCAPED_MARK:
                    lst.append(item)
        return lst

    def orderd_items(self, i):
        keys = [i for i in self.players[i].items.keys()]
        keys.sort()
        v = []
        for k in keys:
            v.append(self.players[i].items[k])
        return v

    def print_board(self):
        """
        print board information by 2nd player's viewing
          1st turn(0)
          0 1 2 3 4 5
        0   h g f e
        1   d c b a
        2
        3
        4   A B C D
        5   E F G H
          2nd turn(1)
        """
        # print board information
        board = self.get_board(self.players[1])
        print("  0 1 2 3 4 5")
        for y in range(0, 6):
            print(y, end=" ")
            for x in range(0, 6):
                item = board[y * Board.SIZE + x]
                s = " "
                if item != None:
                    s = item.name
                    if item.player == self.players[0]:
                        s = s.lower()
                print(s, end=" ")
            print("")
            
            
        # print all items
        print("1st player's items: ", end="")
        for i in self.orderd_items(0):
            print(i.name.lower() + ":" + ItemColor.to_str(i.color), end=" ")
        print ("")
        print("2nd player's items: ", end="")
        for i in self.orderd_items(1):
            print(i.name + ":" + ItemColor.to_str(i.color), end=" ")
        print ("")
        
        # print taken items
        print("taken 1st player's items: ", end="")
        lst = self.taken_items()
        for i in lst:
            if i != None and i.player == self.players[0]:
                print(i.name.lower() + ":" + ItemColor.to_str(i.color), end=" ")
        print ("")
        print("taken 2nd player's items: ", end="")
        for i in lst:
            if i != None and i.player == self.players[1]:
                print(i.name + ":" + ItemColor.to_str(i.color), end=" ")
        print ("")
        
        # print escaped items
        print("escaped 1st player's items: ", end="")
        lst = self.escaped_items()
        for i in lst:
            if i != None and i.player == self.players[0]:
                print(i.name.lower() + ":" + ItemColor.to_str(i.color), end=" ")
        print ("")
        print("escaped 2nd player's items: ", end="")
        for i in lst:
            if i != None and i.player == self.players[1]:
                print(i.name + ":" + ItemColor.to_str(i.color), end=" ")
        print ("")
        

    def get_item(self, player, x, y):
        """
        get an item on (x, y) of the player viewing
        player: viewing player
        """
        board = self.get_board(player)
        return board[y*Board.SIZE + x]

class Player:
    """ A base class of Geister player """
    
    def __init__(self):
        """
        initialize items for the player
         ABCD
         EFGH
        """
        self.items = {}
        self.board = None
        for i in range(8):
            n = chr(ord("A")+i)
            x = i % 4 + 1
            y = i // 4 + 4
            self.items[n] = Item(self, n, x, y)

    def set_board(self, board):
        self.board = board

    def set_items_color(self, lst, color):
        print("set_items_color:" + lst)
        for i in lst:
            self.items[i].set_color(color)

    def move_item(self, n, d):
        """
        @n: target item name
        @d: move direction
        """
        print("move_item:" + n)
        return self.items[n].move(d)

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

    def be_taken(self):
        self.x = Board.TAKEN_MARK
        self.y = Board.TAKEN_MARK

    def move(self, d):
        """
        d: move direction
        return value: True=success to move/False=failure to move
        """

        # escape from the board
        if self.x == 0 and self.y == 0 and (d == Direction.NORTH or d == Direction.WEST) and self.color == ItemColor.BLUE:
            self.x = Board.ESCAPED_MARK
            self.y = Board.ESCAPED_MARK
            return True
        elif self.x == 5 and self.y == 0 and (d == Direction.NORTH or d == Direction.EAST) and self.color == ItemColorBLUE:
            self.x = Board.ESCAPED_MARK
            self.y = Board.ESCAPED_MARK
            return True

        x = self.x
        y = self.y

        # move in inter-board
        if d == Direction.NORTH and self.y > 0:
            y = y - 1
        elif d == Direction.EAST and self.x < 5:
            x = x + 1
        elif d == Direction.WEST and self.x > 0:
            x = x - 1
        elif d == Direction.SOUTH and self.y < 5:
            y = y + 1
        else:
            return False

        print(str(self.x) + "," + str(self.y) + " -> " + str(x) + "," + str(y))

        item = self.player.board.get_item(self.player, x, y)
        if item != None:
            if item.player == self.player:
                return False
            else:
                item.be_taken()

        self.x = x
        self.y = y
        return True

    def set_color(self, color):
        self.color = color

    def color(self):
        self.color

class ItemColor:
    RED = 1
    BLUE = 2

    def to_str(c):
        s = "U"
        if c == ItemColor.RED:
            s = "R"
        elif c == ItemColor.BLUE:
            s = "B"
        return s
            
def test():
    p0 = Player()
    p1 = Player()
    b = Board([p0, p1])
    p0.set_items_color("BCDE", ItemColor.RED)
    p1.set_items_color("ACEG", ItemColor.RED)
    b.print_board()
    flag = p0.move_item("A", Direction.NORTH)
    print(flag)
    b.print_board()
    flag = p1.move_item("A", Direction.NORTH)
    print(flag)
    b.print_board()
    flag = p0.move_item("A", Direction.EAST)
    print(flag)
    b.print_board()
    flag = p1.move_item("A", Direction.NORTH)
    print(flag)
    b.print_board()
    flag = p0.move_item("B", Direction.NORTH)
    print(flag)
    b.print_board()
    flag = p1.move_item("A", Direction.NORTH)
    print(flag)
    b.print_board()
    flag = p0.move_item("A", Direction.NORTH)
    print(flag)
    b.print_board()
    flag = p1.move_item("A", Direction.NORTH)
    print(flag)
    b.print_board()
    flag = p0.move_item("A", Direction.NORTH)
    print(flag)
    b.print_board()
    flag = p1.move_item("A", Direction.WEST)
    print(flag)
    b.print_board()
    flag = p0.move_item("A", Direction.NORTH)
    print(flag)
    b.print_board()
    flag = p1.move_item("A", Direction.WEST)
    print(flag)
    b.print_board()
    flag = p0.move_item("A", Direction.WEST)
    print(flag)
    b.print_board()
    flag = p0.move_item("A", Direction.WEST)
    print(flag)
    b.print_board()
    flag = p0.move_item("A", Direction.WEST)
    print(flag)
    b.print_board()
