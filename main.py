# Michał Katusza Jan Klamka - SISE - zadanie 1 - GKiM
from src.Puzzle import *
import sys


def puzzle_init(algo, algo_param, task_file, sol_file, stats_file, strategy="", state="", parent="", path_cost=""):
    if algo == "astr":
        strategy = algo_param
        algo_param = "RDUL" 
    puzzle = Puzzle(algo, algo_param, task_file, sol_file, stats_file, strategy, state, parent, path_cost)
    return puzzle

# Przykładowe wywołanie programu:
# python main.py dfs LURD "4x4_07_00101" "4x4_07_00101_sol" "4x4_07_00101_stat"
# pliki do wczytania znajdują się w folderze ./files/puzzle_gen
# rozwiązania tworzone są w folderze ./files/solutions
# pliki z informacjami dodatkowymi tworzone są w folderze ./files/stats
puzzle = puzzle_init(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
puzzle.process()
puzzle.save_solution()
puzzle.save_stats()
