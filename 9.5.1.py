from random import randint
class BoardExeption(Exception):
    pass

class BoardOutException(BoardExeption):
    def __init__(self, message="Укажите координаты точки в пределах доски!"):
        super().__init__(message)

class DuplicateShotException(BoardExeption):
    def __init__(self, message="Выбери другие координаты для выстрела!"):
        super().__init__(message)

class ShipPlacementException(BoardExeption):
    pass

class Dot:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __eq__(self, other):
        return self.x==other.x and self.y==other.y

    def __repr__(self):
        return f'Dot({self.x},{self.y})'
class Ship:
    def __init__(self,lenght,bow_point,direction):
        self.lenght=lenght
        self.bow_point=bow_point
        self.direction=direction
        self.health=self.lenght
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.lenght):
            cur_x=self.bow_point.x
            cur_y=self.bow_point.y
            if self.direction==1:
                cur_x+=i
            else:
                cur_y += i
            ship_dots.append(Dot(cur_x,cur_y))
        return ship_dots
    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self,size=6,hid=0):
        self.size=size
        self.massive=[["o"] * size for i in range(size)]
        self.ship_list=[]
        self.hid=hid
        self.alive_ship_list=[]
        self.busy = []
        self.count = 0

    def __str__(self):
        lines = []
        lines.append("  | " + " | ".join(str(i + 1) for i in range(self.size)) + " |")
        lines.append("---" + "----" * self.size + "--")
        for i in range(self.size):
            row = " | ".join(self.massive[i])
            lines.append(f"{i + 1} | {row} |")
            lines.append("---" + "----" * self.size + "--")
        return "\n".join(lines)

    def out(self,d):
        return not((0 <= d.x < self.size and 0 <= d.y < self.size))

    def contour(self,ship,verb=False):
        near=[
            (-1,-1), (-1,0), (-1,1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur=Dot(d.x+dx,d.y+dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.massive[cur.x][cur.y]="•"
                    self.busy.append(cur)
    def add_ship(self,ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise ShipPlacementException()
        for d in ship.dots:
            self.massive[d.x][d.y]="◙"
            self.busy.append(d)

        self.ship_list.append(ship)
        self.contour(ship)

    def shot(self,d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise DuplicateShotException()
        self.busy.append(d)
        for ship in self.ship_list:
            if ship.shooten(d):
                ship.health -=1
                self.massive[d.x][d.y]="X"
                if ship.health == 0:
                    self.count+=1
                    self.contour(ship, verb=True)
                    print('Корабль уничтожен')
                    return True
                else:
                    print('Корабль ранен')
                    return True
        self.massive[d.x][d.y]="•"
        print("Мимо")
        return False
    def begin(self):
        self.busy=[]

    def defeat(self):
        return self.count==len(self.ship_list)

class Player:
    def __init__(self, my_board, enemy_board):
        self.my_board=my_board
        self.enemy_board=enemy_board
    def ask(self):
        raise NotImplementedError

    def move(self):
        while True:
            try:
                target=self.ask()
                repeat=self.enemy_board.shot(target)
                return repeat
            except BoardExeption as e:
                print(e)

class AI(Player):
    def ask(self):
        d=Dot(randint(0,5),randint(0,5))
        print (f"Ход компьютера: {d.x+1} {d.y+1}")
        return d
    pass


class User(Player):
    def ask(self):
        while True:
            cords = input('Ваш ход:').split()

            if len(cords) != 2:
                print('Введите только две координаты')
                continue
            x, y = cords


            if not(x.isdigit()) or not (y.isdigit()):
                print("Введите через пробел две координаты")
                print('x-номер строки, y-номер столбца')

                continue
            x,y= int(x), int(y)
            return Dot(x-1,y-1)

class Game:
    def __init__(self,size=6):
        self.size=size
        user_board=self.random_board()
        ai_board=self.random_board()
        ai_board.hid=None
        self.ai=AI(ai_board,user_board)
        self.user=User(user_board,ai_board)

    def try_board(self):
        lens=[3,2,2,1,1,1,1]
        board=Board(size=self.size)
        attempts=0
        for l in lens:
            while True:
                attempts+=1
                if attempts>2000:
                    return None
                ship=Ship(l, Dot(randint(0,self.size),randint(0,self.size)), randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except ShipPlacementException:
                    pass
        board.begin()
        return board
    def random_board(self):
        board= None
        while board is None:
            board=self.try_board()
        return board
    def greet(self):
        print("Добро пожаловать в игру: Морской бой")
        print('Чтобы сделать ход, укажи номер строки-x, номер столбца-y')

    def print_boards(self):
        user_board_lines = self.user.my_board.__str__().split('\n')
        enemy_board_lines = self.user.enemy_board.__str__().split('\n')
        print("------------------")
        print("Ваша доска:".ljust(40) + "Доска компьютера:")
        print("------------------")
        for user_line, enemy_line in zip(user_board_lines, enemy_board_lines):
            print(user_line.ljust(40) + enemy_line)
        print("------------------")

    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                repeat = self.user.move()
            else:
                repeat = self.ai.move()

            if not repeat:
                num += 1

            if self.ai.my_board.defeat():
                self.print_boards()
                print("------------------")
                print("Вы победили!")
                break
            if self.user.my_board.defeat():
                self.print_boards()
                print("------------------")
                print("Компьютер победил!")
                break

    def start(self):
        self.greet()
        self.loop()

g=Game()
g.start()
