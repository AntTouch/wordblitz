import copy 
import sys
from multiprocessing.dummy import Pool
from functools import partial
from itertools import repeat
from pprint import pprint

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

sys.setrecursionlimit(5000)
def next_character(visited, current_row, current_column, dictionary):
	counter = 0
	if(len(visited) > 7):
		return counter
	word = ""
	visited.append((current_row, current_column))
	for letter in visited:
		word+=board[letter[0]][letter[1]]
	if(word.upper() in dictionary and len(word) > 3):
		word_candidates.append(word)
		print(word, end=' ')
		# word_candidates.append(word)
	prev_row = current_row - 1
	next_row = current_row + 1
	prev_column = current_column - 1
	next_column = current_column + 1
	# print(word)
	# Adds the charcter S the current pos
	if(len(board[current_row]) > next_row and ((next_row, current_column) not in visited)):
		counter += next_character(copy.deepcopy(visited), next_row, current_column, dictionary)
	#Adds the character SE the current pos
	if(len(board[current_row]) > next_row and len(board) > next_column) and ((next_row, next_column) not in visited):
		counter += next_character(copy.deepcopy(visited), next_row, next_column, dictionary)
	# Adds the charcter E of the current pos
	if(len(board) > next_column and ((current_row, next_column) not in visited)):
		counter += next_character(copy.deepcopy(visited), current_row, next_column, dictionary)
	#Adds the character NE the current pos
	if(len(board) > next_column and prev_row >= 0 and ((prev_row, next_column) not in visited)):
		counter += next_character(copy.deepcopy(visited), prev_row, next_column, dictionary)
	# Adds the charcter N the current pos
	if(prev_row >= 0 and ((current_row -1, current_column) not in visited)):
		counter += next_character(copy.deepcopy(visited), prev_row, current_column, dictionary)
	# Adds the charcter NW of the current pos
	if(prev_row >= 0 and prev_column >= 0 and ((prev_row, prev_column) not in visited)):
		counter += next_character(copy.deepcopy(visited), prev_row, prev_column, dictionary)
	# Adds the charcter W of the current pos
	if(prev_column >= 0 and ((current_row, prev_column) not in visited)):
		counter += next_character(copy.deepcopy(visited), current_row, prev_column, dictionary)
	# Adds the charcter SW of the current pos
	if(prev_column >= 0 and len(board[current_row]) > next_row and ((next_row, prev_column) not in visited)):
		counter += next_character(copy.deepcopy(visited), next_row, prev_column, dictionary)
	return counter
def create_board(input):
	arr = [[input[0], input[1], input[2], input[3]],
	[input[4], input[5], input[6], input[7]],
	[input[8], input[9], input[10], input[11]],
	[input[12], input[13], input[14], input[15]]]
	print(input[0], input[1], input[2], input[3])
	print(input[4], input[5], input[6], input[7])
	print(input[8], input[9], input[10], input[11])
	print(input[12], input[13], input[14], input[15])
	return arr
f = open('words-greek.txt', 'r')
dictionary = set(f.read().splitlines())
input = input("Πληκτρολογήστε τα γράμματα των τεσσάρων γραμμών κολλητά (16): ")
print('')
board = create_board(input)
print('')
word_candidates = []
iterator = []
for row in range(0, 4):
	for column in range(0, 4):
		iterator.append(([], row, column, dictionary))
results = []
with Pool(4) as pool:
	results = pool.starmap(next_character, iterator)
word_candidates.sort()
word_candidates.sort(key=len, reverse=True)
#print(sum(results))
#print(len(word_candidates))
#pprint(word_candidates)
print('\n')

def divideList(lst): 
    dct = {} 
  
    for element in lst: 
        if len(element) not in dct: 
            dct[len(element)] = [element] 
        elif len(element) in dct: 
            dct[len(element)] += [element] 
      
    res = [] 
    for key in sorted(dct): 
        res.append(dct[key]) 
      
    return res 
    
#pprint(dictionary)
#xorizei tin lista se stiles analoga me to megethos tis leksis
a=divideList(word_candidates)

#briskoi tin lista me to megalitero ypsos
maxlen=0
for i in range(len(a)):
    if len(a[i]) > maxlen: maxlen = len(a[i])

#loop me basi to megethos tis megaliteris stilis
for i in range(maxlen):
    for j in range(len(a)):
        #pernei apo kathe grammi to stoixeio kathe listas an yparxei
        #an den yparxei antikathista to plithos ton grammaton me kena
        if len(a[j]) > i:
            print(a[j][i], end =" ")
        else :
            print(' ' * len(a[j][0]), end =" ")
    print('')
