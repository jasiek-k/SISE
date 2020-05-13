

class Calculator:

    def __init__(self, files):
        self.files = files
        self.fix_paths()

    def fix_paths(self):
        for i in range(len(self.files)):
            self.files[i] = self.files[i].translate({ord('\\'): '/'})

    def compute_files(self):
        file_content = []
        summary = [0.0] * 5
        for i in range(len(self.files)):
            file_content = self.read_from_file(self.files[i])
            for i in range(len(summary)):
                summary[i] += file_content[i]
        for i in range(len(summary)):
            summary[i] = float(summary[i] / len(self.files))
        print(len(self.files))
        return summary 

    def read_from_file(self, file_name):
        lines_number = 5
        content = []
        f = open(f"{file_name}", "r")
        for i in range(lines_number):
            single_line = f.readline()
            single_line = single_line.translate({ord('\n'): None})
            if i == 4:
                single_line = float(single_line)
            else: 
                single_line = int(single_line)
            content.append(single_line)
        return content