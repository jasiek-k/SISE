from collections import deque
import copy
import time


class Puzzle:

    def __init__(self, algo, order, file_name, sol_name, stats_name):
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
        self.algo_return = 1            # status wykonanego algorytmu (-1 brak rozwiązania, 1 rozwiązanie)
        self.algo = algo
        self.max_level = 20
        self.open_list = []             # lista stanów już odwiedzonych
        self.read_values()
        if self.algo == "bfs":
            self.fifo = deque()         # kolejka wykorzystywana przy algorytmie bfs
            self.processed = 0          # liczba stanów przetworzonych
        elif self.algo == "dfs":
            self.stack = []             # stos wykorzystywany przy algorytmie dfs
            self.prev_move = ""
        self.read_template("./files/template.txt")
          

    # wczytujemy dane z pliku txt, przechowywane
    # są w postaci 2 wymiarowej tablicy int'ów
    def read_from_file(self, file_name):
        lines_number = 5
        content = []
        f = open(f"{file_name}", "r")
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
        self.set_values(content)

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
        if self.algo_return == 0:
            moves_string = "".join(self.moves)
            saved_string = f"{len(self.moves)}\n{moves_string}"
        elif self.algo_return == -1:
            saved_string = "-1"
        self.save_to_file(f"./files/solutions/{self.file_name}_{self.algo}_{self.order}_sol", saved_string)

    # zapisywanie pliku z dodatkowymi informacjami
    def save_info(self):
        if self.algo_return == 0:
            saved_string = f"{len(self.moves)}\n{len(self.open_list)}\n{format(self.processed_time, '.3f')}"
        elif self.algo_return == -1:
            saved_string = "-1"
        self.save_to_file(f"./files/stats/{self.file_name}_{self.algo}_{self.order}_stats", saved_string)

    # funkcja pomocnicza do wyświetlania układanki
    def print_values(self, array):
        for i in range(len(array)):
            printed_string = ''
            for j in range(len(array[0])):
                printed_string += f'{array[i][j]} \t'
            print(printed_string)

    # setter do ustawiania atrybutu zawierającego 
    # przetwarzaną układanke
    def set_values(self, new_values):
        self.values = new_values

    # sprawdzamy, czy rozwiązywana układanka
    # osiągnęła postać wzorca
    def compare_arrays(self, array):
        return (array == self.template)

    # funkcja do zamieniami miejscami 2 pól tablicy 2-wymiarowej 
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

    # funkcja poruszająca pustym polem w zadanym kierunku
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

    # sprawdzamy, czy dany układ piętnastki znajduje się na liście odwiedzonych
    def is_visited(self, array):
        if len(self.open_list) == 0:
            return False
        for i in range(len(self.open_list)):
            if self.open_list[i] == array:
                return True
        return False

    # mechanizm nawrotu wykorzystywany w algorytmie dfs 
    def move_back(self, dict):
        print(dict["moves"])
        last_move = dict["moves"].pop()
        print(dict["moves"])
        print(last_move)
        if last_move == "U":
            dict["values"] = self.move_node(dict["values"], "D")
            dict["moves"] += "D"
        if last_move == "D":
            dict["values"] = self.move_node(dict["values"], "U")
            dict["moves"] += "U"
        if last_move == "L":
            dict["values"] = self.move_node(dict["values"], "R")
            dict["moves"] += "R"
        if last_move == "R":
            dict["values"] = self.move_node(dict["values"], "L")
            dict["moves"] += "L"
        return dict

    # algorytm bfs - zwraca rozwiązaną plansze lub -1
    def bfs(self):
        start_time = time.time()
        # przeglądanie grafu zaczynamy od wybranego wierzchołka v - stan początkowy układanki
        v_dict = {
            "values": self.values.copy(), 
            "moves": []
        }
        self.fifo.append(v_dict)
        solution_level = 0
       
        while len(self.fifo) != 0:
            # pobieramy wierzchołek z kolejki
            v = self.fifo.popleft()
           
            # dodajemy go do listy stanów odwiedzonych
            values_copy = v["values"].copy()
            self.open_list.append(values_copy)
            
            # sprawdzamy, czy stanowi on rozwiązanie - jeśli tak to zwracamy plansze
            if self.compare_arrays(v["values"]):
                self.moves = v["moves"].copy()
                self.algo_return = 0
                end_time = time.time()
                self.processed_time = float((end_time - start_time) * 1000)
                return v
            
            if solution_level < len(v["moves"]):
                solution_level = len(v["moves"])

            # sprawdzamy, jakie ruchy możemy wykonać i porównujemy je z parametrami wywołania
            allowed_moves = self.compare_moves(values_copy)

            # wykonujemy odpowiednie ruchy i w zachowanej kolejności dodajemy plansze do kolejki 
            for i in range(len(allowed_moves)):
                array_copy = []
                array_copy = copy.deepcopy(v) 
                array_copy["values"] = self.move_node(array_copy["values"], allowed_moves[i])
                array_copy["moves"] += allowed_moves[i] 
                
                # sprawdzamy, czy dany układ nie był wcześniej przetwarzany
                if self.is_visited(array_copy["values"]) == False:
                    self.fifo.append(array_copy)

            # zwiększamy liczbę stanów przetworzonych, bo odpytaliśmy 
            # już o sąsiedztwo obecnie przetwarzanego węzła
            self.processed += 1

            # postępowanie w przypadku niepowodzenia w rozwiązaniu układanki 
            if solution_level == self.max_level:
                self.algo_return = -1
                end_time = time.time()
                self.processed_time = float((end_time - start_time) * 1000)
                return -1 
    
    # algorytm dfs - zwraca rozwiązaną plansze lub -1
    def dfs(self):
        start_time = time.time()
        # przeglądanie grafu zaczynamy od wybranego wierzchołka v - stan początkowy układanki
        v_dict = {
            "values": self.values.copy(), 
            "moves": []
        }
        solution_level = 0
        max_moves = 4
        self.stack.append(v_dict)
        current_direction = ""
        levels_list = [0] * self.max_level

        while self.compare_arrays(v_dict["values"]):
            if solution_level < self.max_level:
                if levels_list[solution_level] < max_moves:
                    if 
                        values_copy = v_dict["values"].copy()
                        self.open_list.append(values_copy)
                        levels_list[solution_level - 1] += 1
                    else:
                        levels_list[solution_level] += 1
                else:
                    levels_list[solution_level] = 0
                    v_dict = self.move_back(v_dict)





        while len(self.stack) != 0:
            # przeglądanie grafu zaczynamy od wybranego wierzchołka v - stan początkowy układanki
            # pobieramy wierzchołek ze stosu
            v = self.stack.pop()
            print(v)
            # sprawdzamy, czy dany układ nie był już odwiedzany
            """
            if self.is_visited(v["values"]) == True:
                while self.is_visited(v["values"]) == True:
                    v = self.stack.pop()
            """
            

            























            # dodajemy go do listy stanów odwiedzonych
            values_copy = v["values"].copy()
            self.open_list.append(values_copy)

            # sprawdzamy, czy stanowi on rozwiązanie - jeśli tak to zwracamy plansze
            if self.compare_arrays(v["values"]):
                self.moves = v["moves"].copy()
                self.algo_return = 0
                end_time = time.time()
                self.processed_time = float((end_time - start_time) * 1000)
                return v

            if solution_level < len(v["moves"]):
                solution_level = len(v["moves"])

            allowed_moves = self.compare_moves(v["values"])

            if solution_level == 0:
                current_direction = allowed_moves[0]

            if 0 < solution_level < self.max_level:

                if current_direction not in allowed_moves:
                    current_direction = allowed_moves[0]


                array_copy = []
                array_copy = copy.deepcopy(v) 
                array_copy["values"] = self.move_node(array_copy["values"], current_direction)
                array_copy["moves"] += current_direction
                
                # sprawdzamy, czy dany układ nie był wcześniej przetwarzany
                # tylko jeśli sie nie cofamy 
                if self.is_visited(array_copy["values"]) == False:
                    self.stack.append(array_copy)
            """
            if len(allowed_moves) > 0:
                direction = allowed_moves[0]
            print(direction)
            """
            """
            for i in range(2):
                v["values"] = self.move_node(v["values"], allowed_moves[i])
                v["moves"] += allowed_moves[i]
                print(v)
            v = self.move_back(v)
            print(v)        

            if solution_level == self.max_level 
            """
            if solution_level == self.max_level:
                self.algo_return = -1
                end_time = time.time()
                self.processed_time = float((end_time - start_time) * 1000)
                return -1 






"""
    def process(self):
        if self.algo is "bfs":
            return self.bfs()
        elif self.algo is "dfs":
            return self.dfs()
"""
            
        
    
