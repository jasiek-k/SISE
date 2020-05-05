class Puzzle:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.values = []
        self.template = []
        self.moves = []

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
        file = open(f"{file_name}.txt","w") 
        file.write(content) 
        file.close() 

    # funkcja pomocnicza do wyświetlania układanki
    def print_values(self):
        for i in range(len(self.values)):
            printed_string = ''
            for j in range(len(self.values[0])):
                printed_string += f'{self.values[i][j]} \t'
            print(printed_string)

    def set_values(self, new_values):
        self.values = new_values

    # sprawdzamy, czy rozwiązywana układanka 
    # osiągnęła postać wzorca 
    def compare_arrays(self):
        return(self.values == self.template)

    def switch_values(self, value1_position, value2_position):
        copy_value = self.values[value1_position[0]][value1_position[1]]
        self.values[value1_position[0]][value1_position[1]] = self.values[value2_position[0]][value2_position[1]]
        self.values[value2_position[0]][value2_position[1]] = copy_value

    # znajdujemy pozycje zera w naszej układance
    def get_zero(self):
        for i in range(len(self.values)):
            for j in range(len(self.values[0])):
                if self.values[i][j] == 0:
                    return [i, j] 
   
    def check_up(self):
        if self.get_zero()[0] > 0:
            return True
        else:
            return False
    
    def check_down(self):
        if self.get_zero()[0] < 3:
            return True
        else:
            return False
    
    def check_left(self):
        if self.get_zero()[1] > 0:
            return True
        else:
            return False

    def check_right(self):
        if self.get_zero()[1] < 3:
            return True
        else:
            return False

    
    """
    def bfs(self):

    def dfs(self):

    def a_star(self):
    """
    