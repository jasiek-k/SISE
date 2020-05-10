from src.Puzzle import *
import glob


"""
puzzle_gen = glob.glob("./files/puzzle_gen/*")

for i in range(len(puzzle_gen)):
    puzzle_gen[i] = puzzle_gen[i].translate({ord('\\'): '/'})
    puzzle = Puzzle(4, 4, puzzle_gen[i], "RDUL", "bfs")
    puzzle.read_template("./files/template.txt")
    result = puzzle.bfs()
    if result is not None:
        puzzle.print_values(result["values"])
        #print(puzzle.moves)
        #puzzle.save_solution()
        #puzzle.save_info()
    print(f"{i}/{len(puzzle_gen)}")
"""
puzzle = Puzzle(4, 4, "./files/puzzle_gen/4x4_07_00212.txt", "RDUL", "bfs")
puzzle.read_template("./files/template.txt")
result = puzzle.bfs()
if result is not None:
    puzzle.print_values(result["values"])
    print(puzzle.processed_time)
    print(puzzle.moves)
    puzzle.save_solution()
    puzzle.save_info()

