# Michał Katusza Jan Klamka - SISE - zadanie 1 - GKiM
from src.Puzzle import *
import glob
import sys


"""
puzzle_gen = glob.glob("./files/puzzle_gen/*")

for i in range(len(puzzle_gen)):
    puzzle_gen[i] = puzzle_gen[i].translate({ord('\\'): '/'})
    puzzle = Puzzle(4, 4, puzzle_gen[i], "ULDR", "bfs")
    #puzzle.read_template("./files/template.txt")
    result = puzzle.bfs()
    if result is not None and result != -1:
        puzzle.print_values(result["values"])
        print(puzzle.processed_time)
        print(puzzle.moves)
        print()
        #puzzle.save_solution()
        #puzzle.save_info()
    print(f"{i}/{len(puzzle_gen)}")
"""
"""
puzzle = Puzzle(4, 4, "./files/puzzle_gen/4x4_07_00212.txt", "RDUL", "bfs")
#puzzle.read_template("./files/template.txt")
result = puzzle.bfs()
if result is not None and result != -1:
    puzzle.print_values(result["values"])
    print(puzzle.processed_time)
    print(puzzle.moves)
    puzzle.save_solution()
    puzzle.save_info()
"""
"""
print("This is the name of the program:", sys.argv[0]) 
print("Argument List:", str(sys.argv)) 

if sys.argv[1].lower() in ("bfs", "dfs"):
    param = sys.argv[2].upper()
elif sys.argv[1].lower() == "astr":
    param = sys.argv[2].lower()
puzzle = Puzzle(sys.argv[1], param, sys.argv[3], sys.argv[4], sys.argv[5])
result = puzzle.bfs()
if result != None and result != -1:
    puzzle.print_values(result["values"])
    print(puzzle.processed_time)
    print(puzzle.moves)
    print(puzzle.processed)
    print(len(puzzle.open_list))
    puzzle.save_solution()
    puzzle.save_info()
"""
"""
puzzle = Puzzle("dfs", "RDUL", "4x4_02_00003.txt", "dfs_test.txt", "dfs_test_stats.txt")
print(puzzle.dfs())
"""
puzzle = Puzzle("bfs", "ULDR", "4x4_07_00212.txt", "bfs_test.txt", "bfs_test_stats.txt")
result = puzzle.bfs()
if result != None and result != -1:
    puzzle.print_values(result["values"])
    print(puzzle.processed_time)
    print(puzzle.moves)
    print(puzzle.processed)
    print(len(puzzle.open_list))
    puzzle.save_solution()
    puzzle.save_info()
