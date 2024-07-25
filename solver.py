import copy

class Crossword_Solver:
	def __init__(self, puzzle, worddb):
		self.puzzle = puzzle
		self.worddb = worddb

		# Normalize the letters in the grid
		for square in range(len(self.puzzle.grid)):
			self.puzzle.grid[square] = self.puzzle.grid[square].upper()

		return
	
	# Get all the words that match the empty squares in the clue
	def __get_matching_words(self, grid, clue):
		# List containing all words that match
		match_string = ""
		for square in clue["squares"]:
			match_string += grid[square]
		matching_words = self.worddb.matching_words(match_string)
		return matching_words
	
	# Fill the clue with the word
	def __fill_grid(self, grid, clue, word):
		for square in clue["squares"]:
			if grid[square] == " ":
				grid[square] = word[0]
				word = word[1:]
			else:
				word = word[len(grid[square]):]

		return grid
	
	# Check that the word filled in does not make it impossible
	# To fill it's crossing words
	def __check_crosses(self, clue, grid):
		# Check which direction the clue is going
		clues = self.puzzle.across_clues
		if clue["squares"][0] + 1 == clue["squares"][1]:
			clues = self.puzzle.down_clues

		# Find all crossing clues
		crossing_clues = []
		for square_n, square in enumerate(clue["squares"]):
			for cross_clue in clues:
				if square in cross_clue["squares"]:
					crossing_clues += [(square_n, square, cross_clue)]
					break

		# Check that all crossing clues are still possible
		for square_n, square, cross_clue in crossing_clues:
			if len(self.__get_matching_words(grid, cross_clue)) == 0:
				return False
			
		return True
	

	# Check if grid has been correctly filled
	def __check_filled(self, grid, words_used):
		# Check that all clues were used
		if len(words_used) != len(self.puzzle.across_clues + self.puzzle.down_clues):
			return False

		# If the grid has been filled
		# Check if it's valid
		total_score = 0
		for clue in self.puzzle.across_clues + self.puzzle.down_clues:
			# If the word was already filled by player
			# don't check if in wordlist
			if not " " in clue["word"]:
				continue

			entry = ""
			for square in clue["squares"]:
				entry += grid[square]
			
			# Check if the word exists in the wordlist
			score = self.worddb.get_word(entry)
			if score == None:
				return False
			
			total_score += score

		return total_score
	
	# Sort a list of clues by number of words that match each clue
	# In ascending order
	def __sort_clues(self, clues, grid):
		# Get the number of matches for each clue
		clues_index = []
		for clue in clues:
			word_list = self.__get_matching_words(grid, clue)
			clues_index += [(len(word_list), clue)]

		# Sort in ascending order by number of matching words
		clues_index = sorted(clues_index, key=lambda tup: tup[0])
		
		# Return the sorted clues
		return [clue for _, clue in clues_index]
	
	def __recur(self, grid, min_score, words_used, clues):
		if len(clues) == 0:
			score = self.__check_filled(grid, words_used)
			if score:
				# Return the solution if the score is high enough
				if score >= min_score:
					return grid, score
				
				return None
			else:
				raise Exception("Error while filling grid.")

		# Get clue with the least matching entries
		clue = clues[0]

		# Continue if the clue is already filled out by the player
		if not " " in clue["word"]:
			return self.__recur(
				grid,
				min_score,
				words_used, 
				self.__sort_clues(clues[1:], grid)
			)
		
		# Check if the word has already all squares filled
		# Only works if crosses are checked before filling in grid
		squares_filled = False
		for square in clue["squares"]:
			if square == " ":
				squares_filled = True
				break
		if squares_filled:
			return self.__recur(
				grid,
				min_score,
				words_used, 
				self.__sort_clues(clues[1:], grid)
			)
		
		# Get words matching the blank in the grid
		matching_words = self.__get_matching_words(grid, clue)
		for word, score in matching_words:
			# If the word was already used, skip
			if word in words_used:
				continue
				
			# Fill in the word
			filled_words_used = copy.deepcopy(words_used) + [word]
			filled = self.__fill_grid(copy.deepcopy(grid), clue, word)

			# Check if the word produces impossible crosses
			if not self.__check_crosses(clue, filled):
				continue

			# Proceed by filling the grid
			solution = self.__recur(
				filled,
				min_score,
				filled_words_used, 
				self.__sort_clues(clues[1:], grid)
			)

			# If the grid was successfully filled return the solution
			if solution:
				return solution
			
		# If there was no solution found after iterating through all the words
		# Return failure
		return None
	
	# Update the clues in the self.puzzle object
	def __fill_puzzle_object(self, filled_grid):
		filled_puzzle = copy.deepcopy(self.puzzle)

		# Write new grid to object
		filled_puzzle.grid = filled_grid

		# Write words to the clues
		for clue in filled_puzzle.across_clues + filled_puzzle.down_clues:
			word = ""
			for square in clue["squares"]:
				word += filled_grid[square]

			clue["word"] = word

		filled_puzzle.metadata["notes"]["filled"] = "Filled with github.com/obrhubr/xword-fill."

		return filled_puzzle
	
	def solve(self, min_score=0):
		# Get words that the user already input
		words_used = []
		for clue in self.puzzle.across_clues + self.puzzle.down_clues:
			clue["word"] = clue["word"].upper()
			if not " " in clue["word"]:
				words_used += [clue["word"]]

		# Solve the puzzle
		try:
			filled_grid, score = self.__recur(
				self.puzzle.grid,
				min_score,
				words_used,
				self.puzzle.across_clues + self.puzzle.down_clues
			)
		except:
			raise Exception("Could not fill puzzle.")

		# Write the filled solution to the puzzle object
		filled_puzzle = self.__fill_puzzle_object(filled_grid)

		return filled_puzzle, score