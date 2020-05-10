from collections import deque


class Puzzle:

    def __init__(self, width, height, order):
        self.width = width
        self.height = height
        self.order = order
        self.values = []
        self.template = []
        self.moves = []
        # BFS
        self.fifo = deque()
        # lista stanów już odwiedzonych
        self.closed_list = []

    # wczytujemy dane z pliku txt, przechowywane
    # są w postaci 2 wymiarowej tablicy int'ów
    def read_from_file(self, file_name):
        NUMBER_OF_LINES = 5
        content = []
        f = open(f"{file_name}.txt", "r")
        for i in range(NUMBER_OF_LINES):
            single_line = f.readline()
            single_line = single_line.translate({ord('\n'): None})
            single_line = [int(s) for s in single_line.split(' ')]
            content.append(single_line)
        return content

    # wczytane dane dotyczące zadanej układanki
    # ustawiamy jako atrybuty klasy
    def read_values(self, file_name):
        content = self.read_from_file(file_name)
        self.width = content[0][0]
        self.height = content[0][1]
        content.pop(0)
        self.set_values(content)

    # wczytujemy dane wzorca rozwiązania
    def read_template(self, template_name):
        content = self.read_from_file(template_name)
        content.pop(0)
        self.template = content

    def save_to_file(self, file_name, content):
        file = open(f"{file_name}.txt", "w")
        file.write(content)
        file.close()

    # funkcja pomocnicza do wyświetlania układanki
    def print_values(self, array):
        for i in range(len(array)):
            printed_string = ''
            for j in range(len(array[0])):
                printed_string += f'{array[i][j]} \t'
            print(printed_string)

    def set_values(self, new_values):
        self.values = new_values

    # sprawdzamy, czy rozwiązywana układanka
    # osiągnęła postać wzorca
    def compare_arrays(self, array):
        return(array == self.template)

    def switch_values(self, array, value1_position, value2_position):
        copy_value = array[value1_position[0]][value1_position[1]]
        array[value1_position[0]][value1_position[1]] = array[value2_position[0]][value2_position[1]]
        array[value2_position[0]][value2_position[1]] = copy_value
        return array

    # znajdujemy pozycje zera w naszej układance
    def get_zero(self, array):
        for i in range(len(array)):
            for j in range(len(array[0])):
                if array[i][j] == 0:
                    return [i, j]

    def check_up(self, array):
        if self.get_zero(array)[0] > 0:
            return True
        else:
            return False

    def check_down(self, array):
        if self.get_zero(array)[0] < 3:
            return True
        else:
            return False

    def check_left(self, array):
        if self.get_zero(array)[1] > 0:
            return True
        else:
            return False

    def check_right(self, array):
        if self.get_zero(array)[1] < 3:
            return True
        else:
            return False

    def check_moves(self, array):
        moves = ""
        if self.check_up(array):
            moves = moves + "U"
        if self.check_down(array):
            moves = moves + "D"
        if self.check_right(array):
            moves = moves + "R"
        if self.check_left(array):
            moves = moves + "L"
        return moves

    def compare_moves(self, array):
        allowed_moves = self.check_moves(array)
        moves = ""
        for i in range(len(self.order)):
            if self.order[i] in allowed_moves:
                moves = moves + self.order[i]
        return moves

    def move_node(self, array, move):
        if move == "U":
            move_params = self.get_zero(array)
            move_params[0] = move_params[0] - 1
            array = self.switch_values(
                array, self.get_zero(array), move_params)
        if move == "D":
            move_params = self.get_zero(array)
            move_params[0] = move_params[0] + 1
            array = self.switch_values(
                array, self.get_zero(array), move_params)
        if move == "R":
            move_params = self.get_zero(array)
            move_params[1] = move_params[1] + 1
            array = self.switch_values(
                array, self.get_zero(array), move_params)
        elif move == "L":
            move_params = self.get_zero(array)
            move_params[1] = move_params[1] - 1
            array = self.switch_values(
                array, self.get_zero(array), move_params)
        return array

    def is_visited(self, array):
        if len(self.closed_list) == 0:
            return False
        for i in range(len(self.closed_list)):
            if self.closed_list[i] == array:
                return True
        return False

    def bfs(self):
        # Przeglądanie grafu zaczynamy od wybranego wierzchołka v - stan początkowy układanki
        self.fifo.append(self.values)
        # Dodajemy go do listy stanów odwiedzonych
        # self.closed_list.append(self.values)
        iter = 0
        # while len(self.fifo) != 0:

        while iter < 20:

            # Pobieramy wierzchołek z kolejki
            v = self.fifo.popleft()
            print(v)
            ifGo = False
            while ifGo == False:
                if self.is_visited(v):
                    print("WIELKI CHUJ")
                    ifGo = True
                    #v = self.fifo.popleft()
                else:
                    ifGo = False
            
            # Sprawdzamy, czy stanowi on rozwiązanie - jeśli tak to zwracamy plansze
            if self.compare_arrays(v):
                return v
            self.closed_list.append(v.copy())
            # Sprawdzamy, jakie ruchy możemy wykonać i porównujemy je z parametrami wywołania
            allowed_moves = self.compare_moves(v)
            for i in range(len(allowed_moves)):
                board_copy = v.copy()
                board = self.move_node(board_copy, allowed_moves[i])
                print(f"RUCH: {allowed_moves[i]}")
                print(board)
                self.fifo.append(board)

            print("===============================")
            print(iter)
            print(len(self.fifo))
            print(len(self.closed_list))
            print("-------------------------------")
            self.print_values(v)
            print("===============================")

            #self.move_node(v, "U")
            # self.print_values(v)

            iter = iter + 1

        # q.append('a')
        # q.popleft())

    """
    def dfs(self):

    def a_star(self):
    """
