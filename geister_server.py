
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

    WAIT_FOR_INITIALIZATION = 1
    WAIT_FOR_PLAYER0 = 2
    WAIT_FOR_PLAYER1 = 3
    GAME_END = 4
    
    def __init__(self):
        if(self.__initialized):
            return
        self.__initialized = True
        self.server_init()

    def server_init(self):
        self.player = [Player(), Player()]
        self.board = Board(self.player)
        self.set_done = [False, False]
        self.__status = GeisterServer.WAIT_FOR_INITIALIZATION
        self.__winner = 0

    def status(self):
        return self.__status
    
    def winner(self):
        return self.__winner

    __SET_COMMAND = re.compile('^SET:(\w*)')
    __MOV_COMMAND = re.compile('^MOV:(\w*),(\w*)')

    def command(self, mesg, pid):
        print("comamnd")
        print(mesg)
        flag = False
        if self.__status == GeisterServer.WAIT_FOR_INITIALIZATION:
            m = GeisterServer.__SET_COMMAND.match(mesg)
            if m and len(m.group(1)) == 4 and self.set_done[pid] == False:
                self.player[pid].set_items_color("ABCDEFGH", ItemColor.BLUE) # clear
                self.player[pid].set_items_color(m.group(1).upper(), ItemColor.RED)
                self.set_done[pid] = True
                if self.set_done[0] and self.set_done[1]:
                    self.__status = GeisterServer.WAIT_FOR_PLAYER0
                flag = True
            else:
                flag = False
            
        elif (self.__status == GeisterServer.WAIT_FOR_PLAYER0 and pid == 0) or (self.__status == GeisterServer.WAIT_FOR_PLAYER1 and pid == 1):
            m = GeisterServer.__MOV_COMMAND.match(mesg)
            if m :
                k = m.group(1).upper()
                d = Direction.dir(m.group(2).upper())
                if d != None and ord("A") <= ord(k) and ord(k) <= ord("H") :
                    flag = self.player[pid].move_item(k, d)
                    if flag:
                        j = self.judgement()
                        print("judge:", end=""); print(j)
                        if j:
                            self.__status = GeisterServer.GAME_END
                        else:
                            self.__status = GeisterServer.WAIT_FOR_PLAYER1 \
                                            if self.__status == GeisterServer.WAIT_FOR_PLAYER0 \
                                            else GeisterServer.WAIT_FOR_PLAYER0
                else:
                    flag = False
            else:
                flag = False

        else:
            flag = False
        print(flag)
        return flag

    def judgement(self):
        for pid in range(2):
            taken_blue = 0
            taken_red = 0
            for i in self.player[pid].items.values():
                if i.x == Board.ESCAPED_MARK:
                    self.__winner = pid
                    return True # exit
                elif i.x == Board.TAKEN_MARK:
                    if i.color == ItemColor.RED:
                        taken_red += 1
                    else:
                        taken_blue += 1
            if taken_blue == 4:
                self.__winner = 1 if pid == 0 else 1 # opposite player won
                return True
            elif taken_red == 4:
                self.__winner = pid
                return True
        return False

    def encode_board(self, pid):
        return self.board.encode_board(pid)

    def print_board(self):
        return self.board.print_board()

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

    def ordered_items(self, i):
        keys = [i for i in self.players[i].items.keys()]
        keys.sort()
        v = []
        for k in keys:
            v.append(self.players[i].items[k])
        return v

    def encode_item(self, item, mine):
        x = item.x
        y = item.y
        c = item.color
        s = ""
        if mine:
            if item.is_public():
                s = str(x) + str(y) + ItemColor.to_str(c).lower()
            else:
                s = str(x) + str(y) + ItemColor.to_str(c).upper()
        else:
            if item.is_public():
                # x and y should not be rotated, because they are TAKEN_MARK or ESCAPED_MARK.
                s = str(x) + str(y) + ItemColor.to_str(c).lower()
            else:
                s = str(5-x) + str(5-y) + "u"
        return s

    def encode_board(self, pid):
        """
        in secret: red/blue = R/B
        in public: red/blue/unknown = r/b/u
        ex. 14R24R34R44R15B25B35B45B41u31u21u11u40u30u20u10u
        """
        s = ""
        items = self.ordered_items(pid)
        for i in items:
            s += self.encode_item(i, True)
        items = self.ordered_items(1 if pid == 0 else 0)
        for i in items:
            s += self.encode_item(i, False)
        return s
            
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
        for i in self.ordered_items(0):
            print(i.name.lower() + ":" + ItemColor.to_str(i.color), end=" ")
        print("")
        print("2nd player's items: ", end="")
        for i in self.ordered_items(1):
            print(i.name + ":" + ItemColor.to_str(i.color), end=" ")
        print("")
        
        # print taken items
        print("taken 1st player's items: ", end="")
        lst = self.taken_items()
        for i in lst:
            if i != None and i.player == self.players[0]:
                print(i.name.lower() + ":" + ItemColor.to_str(i.color), end=" ")
        print("")
        print("taken 2nd player's items: ", end="")
        for i in lst:
            if i != None and i.player == self.players[1]:
                print(i.name + ":" + ItemColor.to_str(i.color), end=" ")
        print("")
        
        # print escaped items
        print("escaped 1st player's items: ", end="")
        lst = self.escaped_items()
        for i in lst:
            if i != None and i.player == self.players[0]:
                print(i.name.lower() + ":" + ItemColor.to_str(i.color), end=" ")
        print("")
        print("escaped 2nd player's items: ", end="")
        for i in lst:
            if i != None and i.player == self.players[1]:
                print(i.name + ":" + ItemColor.to_str(i.color), end=" ")
        print("")
        print("1st player's view:" + self.encode_board(0))
        print("2nd player's view:" + self.encode_board(1))
        print("")

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

    def dir(arg):
        d = None
        if arg == "NORTH":
            d = Direction.NORTH
        elif arg == "EAST":
            d = Direction.EAST
        elif arg == "WEST":
            d = Direction.WEST
        elif arg == "SOUTH":
            d = Direction.SOUTH
        return d

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
        
    def is_public(self):
        return self.x == Board.TAKEN_MARK or self.x == Board.ESCAPED_MARK

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
