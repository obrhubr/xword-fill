import click
import time
import sys
import xword_converter as xword

from worddb import WordDB
from util import *
from solver import Crossword_Solver

@click.command()
@click.argument('wordlist', type=click.Path(exists=True))
@click.argument('input-file', type=click.Path(exists=True))
@click.argument('input-format', type=str)
@click.option('--output-file', type=click.Path(exists=True), help='The path to which to write the filled puzzle file.')
@click.option('--output-format', type=str, help='The format in which to write the filled puzzle.')
@click.option('--min-score', default=0, type=int, help='Minimum score to achieve.')
def main(wordlist, input_file, input_format, output_file, output_format, min_score):
	print(f"Starting XWORD filler.\n")

	# Read in wordlist
	words = load_wordlist(wordlist)
	# Print stats about the wordlist
	print(f"🆗 - Successfully loaded wordlist from {wordlist}.")
	print(f"Imported {len(words)} words.\n")

	# Build database
	worddb = WordDB(words)
	# Print stats about the db
	print(f"🆗 - Successfully built the word-db.")
	size = sys.getsizeof(worddb.wordlist) + sys.getsizeof(worddb.bitmap)
	print(f"DB has a size of {round(size / 1024, 2)}mb.\n")
	
	# Read in puzzle
	converter = xword.Converter()
	puzzle = converter.import_puzzle(input_file, input_format)

	# Print stats about the puzzle
	print(f"🆗 - Successfully loaded puzzle from {input_file}.")
	print(f"Puzzle size: {puzzle.dimensions[0]}x{puzzle.dimensions[1]}. Words to fill: {len(puzzle.across_clues + puzzle.down_clues)}")
	print_grid(puzzle.grid, puzzle.dimensions[0], puzzle.dimensions[1])

	# Start timer
	print(f"🔄 - Attempting to solve puzzle. {'Minimum score ' + str(min_score) + '.' if min_score else ''}")
	start = time.time()

	# Solve puzzle
	solver = Crossword_Solver(puzzle, worddb)
	filled_puzzle, score = solver.solve(min_score=min_score)

	# Print time needed to solve
	end = time.time()
	print(f"✅ - Done solving puzzle in {round(end - start, 3)}s.\n")

	# Make this beautiful
	print(f"The filled puzzle has a score of: {score}.")
	print_grid(filled_puzzle.grid, puzzle.dimensions[0], puzzle.dimensions[1], puzzle.grid)

	if output_file and output_format:
		# Write the filled puzzle to file
		converter.export_puzzle(filled_puzzle, output_file, output_format)
		print(f"🆗 - Successfully exported puzzle to {output_file}.")

	return

if __name__ == "__main__":
	main()