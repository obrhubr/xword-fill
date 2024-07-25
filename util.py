def print_grid(grid, width, height, old_grid=None):
	string = ""

	for y in range(height):
		for x in range(width):
			if grid[y * width + x][0] == ".":
				string += f" \033[1;40;40mX\033[0m "
			else:
				if old_grid:
					new = grid[y * width + x] != old_grid[y * width + x]
					if new:
						string += f" \033[1;92m{grid[y * width + x][0]}\033[0m "
					else:
						string += f" \033[1;91m{grid[y * width + x][0]}\033[0m "
				else:
					string += f" \033[1;91m{grid[y * width + x][0]}\033[0m "

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