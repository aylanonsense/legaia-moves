import pickle

character_moves = None

try:
	with open('move_data.pkl', 'rb') as input:
		character_moves = pickle.load(input)
except IOError:
	character_moves = {}

def is_integer(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def print_commands():
	print('  Type [char_name] [move] to record a move being used (e.g. noa ulrdul)')
	print('  Type [char_name] [move_length] [prohibited_moves] to request a move suggestion (e.g. noa 6 ud)')

def for_each_move_leq_length(move_length, restrictions, callback):
	for_each_move_leq_length_recur('', restrictions, move_length, callback)

def for_each_move_leq_length_recur(move_so_far, restrictions, length_to_add, callback):
	if len(move_so_far) > 0:
		callback(move_so_far)
	if length_to_add > 0:
		if 'u' not in restrictions:
			for_each_move_leq_length_recur(move_so_far + 'u', restrictions, length_to_add - 1, callback)
		if 'd' not in restrictions:
			for_each_move_leq_length_recur(move_so_far + 'd', restrictions, length_to_add - 1, callback)
		if 'l' not in restrictions:
			for_each_move_leq_length_recur(move_so_far + 'l', restrictions, length_to_add - 1, callback)
		if 'r' not in restrictions:
			for_each_move_leq_length_recur(move_so_far + 'r', restrictions, length_to_add - 1, callback)

def list_all_moves_leq(move_length, restrictions):
	arr = []
	list_all_moves_leq_recur('', move_length, restrictions, arr)
	return arr

def list_all_moves_leq_recur(move_so_far, length_to_add, restrictions, arr):
	if len(move_so_far) > 0:
		arr.append(move_so_far)
	if length_to_add > 0:
		if 'u' not in restrictions:
			list_all_moves_leq_recur(move_so_far + 'u', length_to_add - 1, restrictions, arr)
		if 'd' not in restrictions:
			list_all_moves_leq_recur(move_so_far + 'd', length_to_add - 1, restrictions, arr)
		if 'l' not in restrictions:
			list_all_moves_leq_recur(move_so_far + 'l', length_to_add - 1, restrictions, arr)
		if 'r' not in restrictions:
			list_all_moves_leq_recur(move_so_far + 'r', length_to_add - 1, restrictions, arr)

def find_move_suggestion(char_moves, move_length, restrictions):
	if 'u' in restrictions and 'd' in restrictions and 'l' in restrictions and 'r' in restrictions:
		return '  No moves possible!'
	best_move = None
	best_score = 0
	all_moves = list_all_moves_leq(move_length, restrictions)
	for i in range(0, len(all_moves)):
		move = all_moves[i]
		score = 0
		if len(move) == move_length:
			for j in range(0, len(all_moves)):
				move_part = all_moves[j]
				if move_part in move and move_part not in char_moves:
					score += 1
		if score > best_score:
			best_move = move
			best_score = score
	return '  Best move: %s [score: %i]' % (best_move, best_score)

def request_command():
	# ask for a command
	cmd = raw_input('Enter or request a move: ')
	# exit if invalid
	parts = cmd.split()
	if len(parts) < 2:
		print_commands()
		return
	# collect character name
	char_name = parts[0].lower()
	if char_name not in character_moves:
		character_moves[char_name] = {}
	# if move_length is given, we're suggesting a move
	if is_integer(parts[1]):
		move_length = int(parts[1])
		restrictions = (parts[2].lower() if len(parts) > 2 else '')
		print(find_move_suggestion(character_moves[char_name], move_length, restrictions))   
	# record each part of the move as having been performed
	else:
		move = parts[1]
		for start in range(0, len(move)+1):
			for end in range(start+1, len(move)+1):
				move_part = move[start:end].lower()
				character_moves[char_name][move_part] = True
		# save move data to file
		with open('move_data.pkl', 'wb') as output:
			pickle.dump(character_moves, output, pickle.HIGHEST_PROTOCOL)
			print('  Recorded move for %s!' % (char_name))

# run the loop
print_commands()
while(True):
	request_command()