class Calculator:

    def __init__(self, files, algo, param):
        self.files = files
        self.fix_paths()
        self.algo = algo
        self.param = param
        self.current_file =""

    def fix_paths(self):
        for i in range(len(self.files)):
            self.files[i] = self.files[i].translate({ord('\\'): '/'})

    def compute_files(self):
        file_content = []
        content = ""
        summary = [0.0] * 5
        for i in range(len(self.files)):
            file_content = self.read_from_file(self.files[i])
            for i in range(len(summary)):
                summary[i] += file_content[i]
        for i in range(len(summary)):
            summary[i] = float(summary[i] / len(self.files))
            content += str(summary[i])
            content += " "
        self.save_solution(content)

    def read_from_file(self, file_name):
        lines_number = 5
        content = []
        f = open(f"{file_name}", "r")
        self.current_file = file_name
        for i in range(lines_number):
            single_line = f.readline()
            single_line = single_line.translate({ord('\n'): None})
            if i == 4:
                single_line = float(single_line)
            else: 
                single_line = int(single_line)
            if single_line == (-1):
                print("UWAGA BŁĄD")
            content.append(single_line)
        return content

    def save_to_file(self, file_name, content):
        file = open(f"{file_name}.txt", "w")
        file.write(content)
        file.close()

    def save_solution(self, content):
        saved_string = f"{self.current_file[19:20]} level {self.algo} {self.param}\n{content}"
        self.save_to_file(f"./glob/{self.algo}_{self.param}_{self.current_file[19:20]}_computed", saved_string)
