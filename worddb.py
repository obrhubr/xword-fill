import random

# Interface that takes a scored wordlist and provides fast lookup times
class WordDB:
	def __init__(self, wordlist):
		# Shuffle the wordlists to make better puzzles
		self.__build_dict(wordlist)
		# Shuffle the wordlists to make different puzzles every time
		self.__shuffle_wordlist()
		# Build lookup table
		self.__build_bitmap()

		return
	
	# Create dictionary by length
	def __build_dict(self, wordlist):
		self.wordlist = {}

		for word, score in wordlist:
			word_length = str(len(word))
			if not word_length in self.wordlist:
				self.wordlist[word_length] = []

			self.wordlist[word_length] += [(word.upper(), score)]
	
	# Create lookup table by letter position
	def __build_bitmap(self):
		self.bitmap = {}

		for word_length in self.wordlist:
			for index, (word, _) in enumerate(self.wordlist[word_length]):
				for character_pos, character in enumerate(word):
					# Lookup string
					bitmap_str = f"{word_length}{character}{character_pos}"

					if not bitmap_str in self.bitmap:
						self.bitmap[bitmap_str] = []
					# Add reference to word's index in self.wordlist into the bitmap object
					self.bitmap[bitmap_str] += [index]

		return
	
	# Shuffle the wordlists
	def __shuffle_wordlist(self):
		for key in self.wordlist:
			random.shuffle(self.wordlist[key])
			# Pre sort the wordlist again
			self.wordlist[key] = sorted(self.wordlist[key], key=lambda tup: tup[1], reverse=True)

		return
	
	# Shuffle wordlist and rebuild bitmap with new indexes
	def shuffle_wordlist(self):
		self.__shuffle_wordlist()
		self.__build_bitmap()
		return
	
	def get_word(self, word):
		# Use the matching_words algorithm with bitmaps instead
		words = self.matching_words(word)
		if len(words) > 0:
			# Return score
			return words[0][1]
		
		return None

	def matching_words(self, match_string):
		word_length = str(len(match_string))

		# If string has no constraint
		# Return all words (presorted) from wordlist with given length
		if len(match_string.strip()) == 0:
			return self.wordlist[word_length]
		
		words_indexes = []
		for index, character in enumerate(match_string):
			if character == " ":
				continue

			# Get every word that conforms to certain rules from bitmap
			# - {word_length} characters long
			# - has letter {character} at position {index}
			bitmap_string = f"{word_length}{character}{index}"
			if bitmap_string in self.bitmap:
				words_indexes += [set(self.bitmap[bitmap_string])]
			else:
				return []

		# Intersect the lists to find words 
		# that match all of the constraints in match_string
		common = words_indexes[0]
		for i in range(1, len(words_indexes)):
			common = common.intersection(words_indexes[i])

		# Find all words from intersected list
		words = []
		for word_index in list(common):
			words += [self.wordlist[word_length][word_index]]

		# Return list, sorted by score descending
		return sorted(words, key=lambda tup: tup[1], reverse=True)