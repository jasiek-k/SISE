from src.Puzzle import *


puzzle = Puzzle(4, 4, "RDUL", "bfs")
puzzle.read_values('./files/puzzle_gen/4x4_03_00001')
puzzle.read_template('./files/wzorzec')
puzzle.compare_arrays(puzzle.values)

result = puzzle.bfs()
if result is not None:
    print("ZWYCIĘSTWO")

