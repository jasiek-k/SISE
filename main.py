# Michał Katusza Jan Klamka - SISE - zadanie 1 - GKiM
from src.Puzzle import *
from src.Calculator import * 
import glob
import sys


def compute_level(level):
    stats_files = glob.glob(f"./files/stats/4x4_0{level}*")
    calc = Calculator(stats_files)
    print(calc.compute_files())


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
"""
puzzle = Puzzle("bfs", "LUDR", "4x4_02_00001.txt", "4x4_02_00001_sol.txt", "4x4_02_00001_stats.txt")
result = puzzle.bfs()
if result != None and result != -1:
    puzzle.print_values(result["values"])
    print(puzzle.processed_time)
    print(puzzle.moves)
    print(puzzle.processed)
    print(len(puzzle.open_list))
    puzzle.save_solution()
    puzzle.save_stats()
puzzle = Puzzle("bfs", "LUDR", "4x4_02_00002.txt", "4x4_02_00002_sol.txt", "4x4_02_00002_stats.txt")
result = puzzle.bfs()
if result != None and result != -1:
    puzzle.print_values(result["values"])
    print(puzzle.processed_time)
    print(puzzle.moves)
    print(puzzle.processed)
    print(len(puzzle.open_list))
    puzzle.save_solution()
    puzzle.save_stats()
"""

"""
stats_files = glob.glob("./files/stats/4x4_02*")

calc = Calculator(stats_files)
print(calc.compute_files())
"""
#compute_level(2)
puzzle = Puzzle("dfs", "LUDR", "4x4_05_00021.txt", "4x4_02_test_sol.txt", "4x4_02_test_stats.txt")
v_dict = {
            "values": puzzle.values.copy(), 
            "moves": []
        }

print(puzzle.dfs(v_dict))