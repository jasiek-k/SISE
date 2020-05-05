from src.Puzzle import *

puzzle = Puzzle( 4, 4 )
#puzzle.save_to_file()
puzzle.read_values('./files/puzzle_gen/4x4_01_00001')
puzzle.read_template('./files/wzorzec')
puzzle.compare_arrays()
puzzle.print_values()
#print(puzzle.get_zero())
print(puzzle.check_up())
print(puzzle.check_down())
print(puzzle.check_right())
print(puzzle.check_left())
puzzle.switch_values([2, 3], [3, 3])
puzzle.print_values()
print(puzzle.check_up())
print(puzzle.check_down())
print(puzzle.check_right())
print(puzzle.check_left())
print(puzzle.compare_arrays())




# './files/puzzle_gen/4x4_01_00001'
# './files/wzorzec'