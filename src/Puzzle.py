class Puzzle:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.arrangement = []

    def arrange_array(self):
        print("test")
        
    def read_from_file(self):
        print("test")

    def save_to_file(self):
        file = open("./files/test_file.txt","w") 
        L = ["This is Delhi \n","This is Paris \n","This is London \n"]  
        file.write(f"{self.width} {self.height}\n") 
        file.writelines(L) 
        file.close() 

    