from src.Puzzle import *


puzzle = Puzzle(4, 4, './files/puzzle_gen/4x4_07_00212', "RDUL", "bfs")
puzzle.read_template('./files/wzorzec')
result = puzzle.bfs()
if result is not None:
    puzzle.print_values(result["values"])
    print(puzzle.processed_time)
    print(puzzle.moves)
    puzzle.save_solution()


