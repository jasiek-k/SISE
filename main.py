from src.Puzzle import *


puzzle = Puzzle(4, 4, "RDUL")
puzzle.read_values('./files/puzzle_gen/4x4_01_00001')
puzzle.read_template('./files/wzorzec')
puzzle.compare_arrays(puzzle.values)

puzzle.bfs()




# './files/puzzle_gen/4x4_01_00001'
# './files/wzorzec'