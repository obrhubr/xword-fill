# XWORD - Fill

This python script supports filling any crossword. It is able to load crosswords from `.json` and `.puz` files thanks to my module [xword-converter](https://github.com/obrhubr/xword-converter) which you have to install.

It uses recursion to fill the puzzle, starting with the words that have the least possible matches.

## Explanation

I was inspired by the method used by [crosshare.org](https://crosshare.org). In order to speed up finding the words matching the blanks in the grid, they precompute a lookup table.

The table is a dictionary with keys in the following format: `{word length}{character}{position of character in the word}`. If I had the following blank in my grid `__R__`, the program would lookup the key `5R2`. This corresponds to words with 5 letters and an `R` in the 3rd position.

Another more complicated example: `_AR__`. Because 2 letters are set here, we cannot directly search the lookup table for matching words. We instead perform two searches, one for `_A___` and another for `__R__`. We then get the intersection of both search results, as we are only interested in words that have both an `A` in the second position and an `R` in the third.

This method significantly speeds up searching for matching words. According to my experiments, by about 300 times for small 5 by 5 puzzles (from `20.00s` to `0.058s`).

## Usage

You have to provide your own wordlist in the following format
```python
# word;score
MOTOR;80
DIAL;85
```

Call `main.py` with the following arguments: (To solve a `.puz` for example)

```bash
python main.py --wordlist ./wordlists/wordlist.txt --input-file ./puzzles/puzzle.puz --input-format puz
```

If you also want to write the filled puzzle back to file:

```bash
python main.py --wordlist ./wordlists/wordlist.txt --input-file ./puzzles/puzzle.puz --input-format puz --output-file ./puzzle.json --output-format json
``` 