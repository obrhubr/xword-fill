def print_grid(grid, width, height):
	string = ""

	for y in range(height):
		for x in range(width):
			if grid[y * width + x][0] == ".":
				string += " X "
			else:
				string += f" {grid[y * width + x][0]} "
		string += "\n"

	print(string)

def load_wordlist(file):
	wordlist = []

	with open(file, "r") as f:
		text_list = f.readlines()

	for word in text_list:
		w = word.strip().split(";")
		wordlist += [(w[0], int(w[1]))]

	return wordlist