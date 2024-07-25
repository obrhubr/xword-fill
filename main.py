import click
import time
import xword_converter as xword

from worddb import WordDB
from util import *
from solver import Crossword_Solver

@click.command()
@click.option('--wordlist', default="./wordlists/wordlist_combined.txt", type=click.Path(exists=True), help='The wordlist to use. Expected format: "word;score".')
@click.option('--input-file', default="./puzzles/fill.json", type=click.Path(exists=True), help='The puzzle to fill.')
@click.option('--input-format', default="json", type=str, help='The format of the puzzle to fill.')
@click.option('--output-file', help='The path to which to write the filled puzzle file.')
@click.option('--output-format', type=str, help='The format in which to write the filled puzzle.')
def main(wordlist, input_file, input_format, output_file, output_format):
	print(f"Starting XWORD filler.\n")

	# Read in wordlist
	words = load_wordlist(wordlist)
	worddb = WordDB(words)
	
	# Print stats about the wordlist
	print(f"🆗 - Successfully loaded wordlist from {wordlist}.")
	print(f"Imported {len(words)} words.\n")

	# Read in puzzle
	converter = xword.Converter()
	puzzle = converter.import_puzzle(input_file, input_format)

	# Print stats about the puzzle
	print(f"🆗 - Successfully loaded puzzle from {input_file}.")
	print(f"Puzzle size: {puzzle.dimensions[0]}x{puzzle.dimensions[1]}.")
	print(f"Words to fill: {len(puzzle.across_clues + puzzle.down_clues)}.")
	print_grid(puzzle.grid, puzzle.dimensions[0], puzzle.dimensions[1])

	# Start timer
	print(f"🔄 - Attempting to solve puzzle.")
	start = time.time()

	# Solve puzzle
	solver = Crossword_Solver(puzzle, worddb)
	filled_puzzle, score = solver.solve()

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