from collections import deque
import copy
import time


class Puzzle:

    def __init__(self, width, height, file_name, order, algo):
        self.width = width
        self.height = height
        self.order = order
        self.values = []
        self.template = []
        self.moves = []
        self.file_name = file_name
        self.read_values()
        if algo == "bfs":
            self.fifo = deque()
            # lista stanów już odwiedzonych
            self.closed_list = []
            self.processed_time = 0
            self.algo_return = 1

    # wczytujemy dane z pliku txt, przechowywane
    # są w postaci 2 wymiarowej tablicy int'ów
    def read_from_file(self, file_name):
        lines_number = 5
        content = []
        f = open(f"{file_name}.txt", "r")
        for i in range(lines_number):
            single_line = f.readline()
            single_line = single_line.translate({ord('\n'): None})
            single_line = [int(s) for s in single_line.split(' ')]
            content.append(single_line)
        return content

    # wczytane dane dotyczące zadanej układanki
    # ustawiamy jako atrybuty klasy
    def read_values(self):
        content = self.read_from_file(self.file_name)
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

    # zapisywanie pliku z rozwiązaniem
    def save_solution(self):
        if self.algo_return == 0:
            moves_string = "".join(self.moves)
            saved_string = f"{len(self.moves)}\n{moves_string}"
        elif self.algo_return == -1:
            moves_string = "-1"
        self.save_to_file(f"./files/solutions/{self.file_name[19:31]}_rozwiazanie", saved_string)

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
        return (array == self.template)

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

    # zwraca string ze wszystkimi ruchami, jakie 
    # możemy wykonać w danym momencie
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

    # uzyskujemy możliwe do wykonania w danym momencie
    # ruchy uwzględniające kolejność podaną przy wywołaniu
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
        if move == "L":
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
        start_time = time.time()
        # Przeglądanie grafu zaczynamy od wybranego wierzchołka v - stan początkowy układanki
        v_dict = {
            "values": self.values.copy(), 
            "moves": []
        }
        self.fifo.append(v_dict)

        solution_level = 0
        iter = 0
       
        while len(self.fifo) != 0:
        #while iter < 20:
            # Pobieramy wierzchołek z kolejki
            v = self.fifo.popleft()

            # Sprawdzamy, czy dany układ nie był wcześniej przetwarzany
            if self.is_visited(v["values"]) == True:
                while self.is_visited(v["values"]) == True:
                    v = self.fifo.popleft()
            
            # Sprawdzamy, czy stanowi on rozwiązanie - jeśli tak to zwracamy plansze
            if self.compare_arrays(v["values"]):
                self.moves = v["moves"].copy()
                self.algo_return = 0
                end_time = time.time()
                self.processed_time = int((end_time - start_time) * 1000)
                return v
            
            # Dodajemy go do listy stanów odwiedzonych
            values_copy = v["values"].copy()
            self.closed_list.append(values_copy)

            if solution_level < len(v["moves"]):
                solution_level = len(v["moves"])

            # Sprawdzamy, jakie ruchy możemy wykonać i porównujemy je z parametrami wywołania
            allowed_moves = self.compare_moves(values_copy)

            # Wykonujemy odpowiednie ruchy i w zachowanej kolejności dodajemy plansze do kolejki 
            for i in range(len(allowed_moves)):
                array_copy = []
                array_copy = copy.deepcopy(v) 
                array_copy["values"] = self.move_node(array_copy["values"], allowed_moves[i])
                array_copy["moves"] += allowed_moves[i] 
                self.fifo.append(array_copy)
            
            iter = iter + 1

            if solution_level == 15:
                self.algo_return = -1
                end_time = time.time()
                self.processed_time = int((end_time - start_time) * 1000)
                return -1 

    """
    def dfs(self):

    def a_star(self):
    """
