from collections import deque
import copy
import time
from math import ceil


class Puzzle:

    def __init__(self, algo, order, file_name, sol_name, stats_name, strategy, state, parent, path_cost):
        self.width = 0                  # szerokość układanki
        self.height = 0                 # wysokość układanki             
        self.order = order              # kolejność przeszukiwania sąsiedztwa (np. RDUL)
        self.values = []                # wczytane wartości układanki do rozwiązania
        self.template = []              # wczytana plansza wzorcowa (rozwiązana)
        self.moves = []                 # lista ruchów wykonanych przy rozwiązywaniu układanki
        self.file_name = file_name      # nazwa pliku, z którego ma zostać wczytana układanka
        self.sol_name = sol_name        # nazwa pliku, do którego ma zostać zapisane rozwiązanie
        self.stats_name = stats_name    # nazwa pliku, do którego mają zostać zapisane dodatkowe informacje
        self.processed_time = 0         # długość wykonywanych obliczeń [ms]
        self.algo_return = 0            # status wykonanego algorytmu (-1 brak rozwiązania, 1 rozwiązanie)
        self.algo = algo                # obecnie przetwarzany algorytm
        self.max_level = 20             # maksymalny dopuszczalny poziom rekurencji 
        self.open_list = []             # lista stanów już odwiedzonych
        self.processed = 0              # liczba stanów przetworzonych
        self.recursion_level = 0
        self.read_values()
        self.read_template("./files/template")
        if self.algo == "bfs":
            self.fifo = deque()         # kolejka wykorzystywana przy algorytmie bfs
        elif self.algo == "dfs":
            self.prev_move = ""         # informacja o poprzednim wykonanym ruchu
        elif self.algo == "astr":
            self.strategy = strategy    # manh/hamm
            self.state = state
            self.parent = parent
            self.path_cost = path_cost
            self.last_move = order
            self.open_list_length = 0

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
        content = self.read_from_file(f"./files/puzzle_gen/{self.file_name}")
        self.width = content[0][0]
        self.height = content[0][1]
        content.pop(0)
        self.values = content

    # wczytujemy dane wzorca rozwiązania
    def read_template(self, template_name):
        content = self.read_from_file(template_name)
        content.pop(0)
        self.template = content

    # uniwersalna funkcja do zapisywania danych do pliku
    def save_to_file(self, file_name, content):
        file = open(f"{file_name}.txt", "w")
        file.write(content)
        file.close()

    # zapisywanie pliku z rozwiązaniem
    def save_solution(self):
        param = ""
        if self.algo_return == 1:
            moves_string = "".join(self.moves)
            saved_string = f"{len(self.moves)}\n{moves_string}"
        elif self.algo_return == -1 or self.algo_return == None:
            saved_string = "-1"
        if self.algo == "astr":
            param = self.strategy
        else:
            param = self.order
        file_path = self.file_name
        file_path = file_path.translate({ord('\n'): None})
        self.save_to_file(
            f"./files/solutions/{file_path}_{self.algo}_{param}_sol", saved_string)

    # zapisywanie pliku z dodatkowymi informacjami
    def save_stats(self):
        param = ""
        if self.algo_return == 1:
            if self.algo != "astr":
                saved_string = f"{len(self.moves)}\n{len(self.open_list)}\n{self.processed}\n{self.recursion_level}\n{format(self.processed_time, '.3f')}"
                param = self.order
            else:
                saved_string = f"{len(self.moves)}\n{self.open_list_length}\n{self.processed}\n{self.recursion_level}\n{format(self.processed_time, '.3f')}"
                param = self.strategy
        elif self.algo_return == -1 or self.algo_return == None:
            saved_string = "-1"
        file_path = self.file_name
        file_path = file_path.translate({ord('\n'): None})
        self.save_to_file(
            f"./files/stats/{file_path}_{self.algo}_{param}_stats", saved_string)

    # funkcja pomocnicza do wyświetlania układanki
    def print_values(self, array):
        for i in range(len(array)):
            printed_string = ''
            for j in range(len(array[0])):
                printed_string += f'{array[i][j]} \t'
            print(printed_string)

    # sprawdzamy, czy rozwiązywana układanka
    # osiągnęła postać wzorca
    def compare_arrays(self, array):
        return (array == self.template)

    # funkcja do zamieniami miejscami 2 pól tablicy 2-wymiarowej
    def switch_values(self, array, value1_position, value2_position):
        copy_value = array[value1_position[0]][value1_position[1]]
        array[value1_position[0]][value1_position[1]
                                  ] = array[value2_position[0]][value2_position[1]]
        array[value2_position[0]][value2_position[1]] = copy_value
        return array

    # znajdujemy pozycje zera w naszej układance
    def get_zero(self, array):
        for i in range(len(array)):
            for j in range(len(array[0])):
                if array[i][j] == 0:
                    return [i, j]

    # sprawdzamy, czy możemy wykonać ruch do góry
    # oraz w poniższych funkcjach odpowiednio w
    # pozostałych kierunkach
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

    # ta funkcja również zwraca możliwe do wykonania ruchy, lecz
    # w postaci tablicy z wartościami 0/1 (gdzie 1 to możliwość ruchu 
    # w danym kierunku) zawsze z zachowaniem określonej kolejności
    # ruchów (UDRL) - funkcja na potrzeby algorytmu dfs 
    def check_all_moves(self, array):
        moves = [0] * len(self.order)
        allowed_moves = self.check_moves(array)
        all_moves = ["U", "D", "R", "L"]
        for i in range(len(moves)):
            for j in range(len(all_moves)):
                if self.order[i] == all_moves[j] and all_moves[j] in allowed_moves:
                    moves[i] = 1
        return moves

    # funkcja poruszająca pustym polem w zadanym kierunku
    def move_node(self, array, move):
        if self.algo == "astr":
            array = copy.deepcopy(array)
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

    # sprawdzamy, czy dany układ piętnastki znajduje się na liście odwiedzonych
    def is_visited(self, array):
        if len(self.open_list) == 0:
            return False
        for i in range(len(self.open_list)):
            if self.open_list[i] == array:
                return True
        return False

    # algorytm bfs - zwraca rozwiązaną plansze lub -1
    def bfs(self):
        # rozpoczynamy liczenie czasu obliczeniowego
        start_time = time.time()
        # przeglądanie grafu zaczynamy od wybranego wierzchołka v - stan początkowy układanki
        v_dict = {
            "values": self.values.copy(),
            "moves": []
        }
        # umieszczamy wierzchołek v w kolejce fifo
        self.fifo.append(v_dict)
        # ustawiamy początkowy poziom rozwiązania
        solution_level = 0
        # rozpoczynamy obliczenia (dopóki kolejka nie jest pusta)
        while len(self.fifo) != 0:
            # pobieramy wierzchołek z kolejki
            v = self.fifo.popleft()
            # dodajemy go do listy stanów odwiedzonych
            values_copy = v["values"].copy()
            self.open_list.append(values_copy)

            # sprawdzamy, czy stanowi on rozwiązanie - jeśli tak to zwracamy plansze
            if self.compare_arrays(v["values"]):
                # ustawiamy wartości atrybutów potrzebnych do statystyk
                self.moves = v["moves"].copy()
                self.algo_return = 1
                self.recursion_level = len(self.moves)
                # kończymy obliczanie czasu i wyznaczamy długość trwania obliczeń 
                end_time = time.time()
                self.processed_time = float((end_time - start_time) * 1000)
                return v

            # aktualizujemy poziom rozwiązania jeśli wzrósł 
            if solution_level < len(v["moves"]):
                solution_level = len(v["moves"])

            # sprawdzamy, jakie ruchy możemy wykonać i porównujemy je z parametrami wywołania 
            # (w tym przypadku kolejność ruchów nie ma znaczenia)
            allowed_moves = self.compare_moves(values_copy)

            # wykonujemy odpowiednie ruchy i w zachowanej kolejności dodajemy plansze do kolejki fifo
            for i in range(len(allowed_moves)):
                array_copy = []
                array_copy = copy.deepcopy(v)
                array_copy["values"] = self.move_node(
                    array_copy["values"], allowed_moves[i])
                # w każdym ze słowników zapisujemy wykonany ruch
                array_copy["moves"] += allowed_moves[i]

                # sprawdzamy, czy dany układ nie był wcześniej przetwarzany
                # robiąc to w tym miejscu unikamy dodania do kolejki i wielokrotnego przetworzenia
                # tego samego układu
                if self.is_visited(array_copy["values"]) == False:
                    self.fifo.append(array_copy)

            # zwiększamy liczbę stanów przetworzonych, bo odpytaliśmy
            # już o sąsiedztwo obecnie przetwarzanego węzła
            self.processed += 1

            # postępowanie w przypadku niepowodzenia w rozwiązaniu układanki
            if solution_level == self.max_level:
                # ustawiamy status zakończenia algorytmu (-1 -> niepowodzenie) 
                # i kończymy liczenie czasu działania
                self.algo_return = -1
                end_time = time.time()
                self.processed_time = float((end_time - start_time) * 1000)
                return -1

    # algorytm dfs - zwraca rozwiązaną plansze lub -1
    def dfs(self, v_dict):
        # w sytuacji osiągnięcia maksymalnego poziomu rekurencji zwraca none i powraca poziom wyżej
        if len(v_dict["moves"]) >= self.max_level:
            return None

        # ustawiamy poziom rekurencji (jeśli poziom planszy różni się od obecnie przyjętego)
        if len(v_dict["moves"]) > self.recursion_level:
            self.recursion_level = len(v_dict["moves"])

        # sprawdzenie czy układanka jest rozwiązana (jeśli tak ustawia status = 1 i zwraca rozwiązaną plansze)
        if self.compare_arrays(v_dict["values"]):
            self.moves = v_dict["moves"].copy()
            self.algo_return = 1
            self.recursion_level = len(self.moves)
            return v_dict

        # sprawdzamy, jakie ruchy możemy wykonać, ale w odróżnieniu od algorytmu bfs 
        # zawsze zachowujemy tą samą kolejność ruchów
        moves = self.check_all_moves(v_dict["values"])

        # odpytujemy po kolei wszystkie kierunki
        for i in range(len(moves)):
            # wykonujemy ruch w danym kierunku jeśli możemy, aktualizujemy 
            # wartość ostatnio wykonanego ruchu, dodajemy ten ruch do listy  
            # a układankę po wykonaniu ruchu dodajemy do listy odwiedzonych
            # wywołujemy algorytm dla nowej planszy
            if moves[i] == 1:
                dict_copy = []
                dict_copy = copy.deepcopy(v_dict)
                dict_copy["values"] = self.move_node(
                    dict_copy["values"], self.order[i])
                self.prev_move = self.order[i]
                dict_copy["moves"] += self.order[i]
                self.open_list.append(dict_copy)
                new_dict = self.dfs(dict_copy)
                # jeśli algorytm znajdzie rozwiązanie - ustawiamy status na 1 oraz 
                # zwracamy rozwiązaną planszę 
                if new_dict != None and self.compare_arrays(new_dict["values"]):
                    self.moves = new_dict["moves"].copy()
                    self.algo_return = 1
                    self.recursion_level = len(self.moves)
                    return new_dict

        # zwiększamy liczbę przetworzonych stanów po odpytaniu sąsiedztwa
        self.processed += 1

    def get_valid_moves(self):
        x = self.get_zero(self.state)[0]
        y = self.get_zero(self.state)[1]
        rows = len(self.state)
        cols = len(self.state[0])
        moves = []
        if (x > 0 and self.last_move != 'D'):
            moves.append('U')
        if ((x < (rows - 1)) and self.last_move != 'U'):
            moves.append('D')
        if (y > 0 and self.last_move != 'R'):
            moves.append('L')
        if ((y < (cols - 1)) and self.last_move != 'L'):
            moves.append('R')
        return moves

    def get_ordered_moves(self, strategy):
        moves = self.get_valid_moves()
        ordered = []
        for sign in strategy:
            for move in moves:
                if(sign == str(move)):
                    ordered.append(move)
        return ordered

    def get_path(self):
        path = ''
        if(self.parent == None):
            return path
        path += self.parent.get_path() + str(self.last_move)
        return path

    def a_star(self):
        self.state = self.values
        return AStar(self.state, self.template, self.file_name, self.sol_name, self.stats_name, self.strategy, self.order).solve()

    # funkcja wywołująca odpowiednią funkcję w zależności od 
    # wybranego algorytmu 
    def process(self):
        if self.algo == "bfs":
            return self.bfs()
        elif self.algo == "dfs":
            v_dict = {
                "values": self.values.copy(),
                "moves": []
            }
            start = time.time()
            result = self.dfs(v_dict)
            if result != None:
                self.algo_return = 1
            else:
                self.algo_return = -1
            stop = time.time()
            self.processed_time = float((stop - start) * 1000)
            return result
        elif self.algo == "astr":
            result = []
            result = self.a_star()
            if result[0] != -1:
                self.algo_return = 1
                self.moves = result[0]
                self.recursion_level = len(self.moves)
                self.open_list_length = result[1]
                self.processed = result[2]
                self.processed_time = result[4]
            else:
                self.algo_return = -1
            print(self.moves)
            return result


class AStar:

    frontier = {}
    explored = {}

    def __init__(self, start, target, file_name, sol_name, stats_name, strategy, order):
        self.target = target
        self.path = []
        self.strategy = strategy
        self.start = Puzzle("astr", order, file_name, sol_name,
                            stats_name, strategy, start, None, 0)
        self.max_depth = 7
        self.max_recursion = 20
        self.rows = len(start)
        self.columns = len(start[0])
        if(self.start != self.target):
            if(self.strategy == 'manh'):
                distance = self.Manhattan(self.start.state)
            elif(self.strategy == 'hamm'):
                distance = self.Hamming(self.start.state)
            self.frontier.setdefault(distance, []).append(self.start.state)
            self.explored[str(self.start.state)] = self.start

    def Manhattan(self, state):
        distance = 0
        for x in state:
            for y in x:
                if(y != 0):
                    temp = y % self.columns
                    if(temp == 0):
                        temp = self.columns
                    distance += abs((state.index(x) + 1) - ceil(y /
                                                                self.rows)) + abs((x.index(y) + 1) - temp)
        return distance

    def Hamming(self, state):
        distance = 0
        for x in state:
            for y in x:
                if(y != 0):
                    temp = y % self.columns
                    if(temp == 0):
                        temp = self.columns
                    if(((state.index(x) + 1) != ceil(y / self.rows)) or ((x.index(y) + 1) != temp)):
                        distance += 1
        return distance

    def return_path(self):
        return self.path

    def solve(self):
        start_time = time.time()
        solution_level = 0
        while(len(self.frontier) > 0):
            if solution_level < self.max_recursion:
                closest = min(self.frontier)
                current_state = self.frontier[closest].pop(0)
                if(len(self.frontier[closest]) == 0):
                    del(self.frontier[closest])
                current_state_string = current_state.__str__()
                current_state = self.explored[current_state_string]
                moves = current_state.get_valid_moves()
                for move in moves:
                    new_array = current_state.move_node(
                        current_state.state, move)
                    solution_level = len(current_state.get_path())
                    new_cost = current_state.path_cost + 1
                    new_move = move
                    new_state = Puzzle("astr", new_move, self.start.file_name, self.start.sol_name,
                                       self.start.stats_name, self.start.strategy, new_array, current_state, new_cost)
                    new_state_string = new_array.__str__()
                    if(new_state_string not in self.explored):
                        self.explored[new_state_string] = new_state
                        if(new_cost > self.max_depth):
                            self.max_depth = new_cost
                        if(new_array == self.target):
                            solving_time = time.time() - start_time
                            solved = round(solving_time, 3)
                            path = new_state.get_path()
                            explored = (len(self.explored) + 1)
                            frontier = len(self.explored) - len(self.frontier)
                            return [path, explored, frontier, self.max_depth, solved]
                        if(self.strategy == 'manh'):
                            distance = self.Manhattan(new_array)
                        elif(self.strategy == 'hamm'):
                            distance = self.Hamming(new_array)
                        if(distance not in self.frontier):
                            self.frontier.setdefault(
                                distance, []).append(new_array)
                        else:
                            self.frontier[distance].append(new_array)
            else:
                return -1
