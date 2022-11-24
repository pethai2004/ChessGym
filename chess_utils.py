import copy 
from P import *

import matplotlib.pyplot as plt

def translate(val):
    '''Return either instance of Coord or a String'''
    if isinstance(val, str):
        return def_coordXY[np.where(def_coord == val)][0]
    elif isinstance(val, Coord): 
        return def_coord[np.where(def_coordXY == val)][0]
    elif isinstance(val, (list, tuple)):
        return def_coord[np.where(def_coordXY == Coord(*val))][0]

class Coord:
	def __init__(self, x, y):
		self.xy = (x, y)

	def __repr__(self): return "C(" +str(self.xy[0])+ ","+ str(self.xy[1])+ ")"

	def __add__(self, inputs):
		if isinstance(inputs, Coord):
			return self.xy[0]+inputs.xy[0], self.xy[1]+inputs.xy[1]
		elif isinstance(inputs, (list, tuple)):
			return self.xy[0]+inputs[0], self.xy[1]+inputs[1]
	
	def __sub__(self, inputs):
		if isinstance(inputs, Coord):
			return self.xy[0]-inputs.xy[0], self.xy[1]-inputs.xy[1]
		elif isinstance(inputs, (list, tuple)):
			return self.xy[0]-inputs[0], self.xy[1]-inputs[1]

	def __eq__(self, inputs): 
		if isinstance(inputs, Coord): return self.xy == inputs.xy
		else : return self.xy == translate(inputs)
	
	def __getitem__(self, inputs): return self.xy[inputs]
	
	def __hash__(self): return hash(self.xy)
 
def_coord = np.array([[str(I)+J for J in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']] for I in reversed(range(1, 9))])
def_coordXY = np.flip(np.transpose(
    [[Coord(*[J, I]) for I in range(8)] for J in range(8)], axes=(1, 0)), 0)

class Spec(object):
    
	def __init__(self, init_pos=None, **kwargs):
		if isinstance(init_pos, Coord): self.init_pos = init_pos
		elif isinstance(init_pos, str): self.init_pos = translate(init_pos)
		elif isinstance(init_pos, (tuple, list)): self.init_pos = Coord(init_pos[0], init_pos[1])
		self.coordinate = copy.deepcopy(self.init_pos)
		self.history = []
		for k, v in kwargs.items(): setattr(self, k, v)

	def update(self, kwargs):
		for k, v in kwargs.items(): setattr(self, k, v)

	def m_coord(self, value):
		if isinstance(value, Coord): self.coordinate = copy.deepcopy(value)
		else : self.coordinate = translate(self.init_pos)

	def __repr__(self): return "Spec({})".format(self.coordinate)

	@property
	def str_coordinate(self): return translate(self.coordinate)
	@property 
	def tuple_coordinate(self): return self.coordinate.xy

Team1Pos = {"Pawn0": "2A",  "Pawn1": "2B", "Pawn2": "2C", "Pawn3": "2D" ,
         "Pawn4": "2E", "Pawn5": "2F", "Pawn6": "2G", "Pawn7": "2H",
         "Rook0": "1A", "Knight0":"1B", "Bishop0":"1C", "Queen":"1D", 
         "King":"1E", "Bishop1":"1F", "Knight1":"1G", "Rook1":"1H"}

Team0Pos = {"Pawn0": "7A", "Pawn1": "7B","Pawn2": "7C", "Pawn3": "7D", 
         "Pawn4": "7E", "Pawn5": "7F", "Pawn6": "7G", "Pawn7": "7H",
         "Rook0": "8A", "Knight0":"8B", "Bishop0":"8C", "Queen":"8D", 
         "King":"8E", "Bishop1":"8F", "Knight1":"8G", "Rook1":"8H"}

def all_piece_initializer(teamid):
	assert (teamid==0 or teamid==1)
	members = []
	if teamid ==0 : 
		shift_idx = 0
		teampos = Team0Pos
	elif teamid == 1:
		shift_idx = 16
		teampos = Team1Pos

	for i in range(8):
		namep = "Pawn"+str(i)
		members.append(Pawn(name=namep, spec=Spec(teampos[namep]), idx=i+shift_idx, teamid=teamid))
	members.append(Knight(name="Knight0", spec=Spec(teampos["Knight0"]), idx=8+shift_idx, teamid=teamid))
	members.append(Knight(name="Knight1", spec=Spec(teampos["Knight1"]), idx=9+shift_idx, teamid=teamid))
	members.append(Bishop(name="Bishop0", spec=Spec(teampos["Bishop0"]), idx=10+shift_idx, teamid=teamid))
	members.append(Bishop(name="Bishop1", spec=Spec(teampos["Bishop1"]), idx=11+shift_idx, teamid=teamid))
	members.append(Rook(name="Rook0", spec=Spec(teampos["Rook0"]), idx=12+shift_idx, teamid=teamid))
	members.append(Rook(name="Rook1", spec=Spec(teampos["Rook1"]), idx=13+shift_idx, teamid=teamid))
	members.append(Queen(name="Queen", spec=Spec(teampos["Queen"]), idx=14+shift_idx, teamid=teamid))
	members.append(King(name="King", spec=Spec(teampos["King"]), idx=15+shift_idx, teamid=teamid))
	
	return members

def get_possible_move(board):
    '''All possible the agent could pick and move the pieces'''
    pass

def out_of_bound(coord):
	if coord[0] < 0 or coord[0] > 7 or coord[1] < 0 or coord[1] > 7: return True
	else: return False

def del_out_of_bound(coord_list):
	for coord in coord_list: 
		if out_of_bound(coord): coord_list.remove(coord)
	return coord_list

def check_is_empty(board, val, team="all"):
	if team=="all":
		if e_get_board_dict(board.all_members)[translate(val)] == -1: return True
		else : return False
	elif team=="opponent":
		_pos = e_get_board_dict(board.all_members)[translate(val)]
		if _pos != -1: 
			if _pos.teamid != board.turn: return True
		else : return False
	elif team=="self":
		_pos = e_get_board_dict(board.all_members)[translate(val)]
		if _pos != -1: 
			if _pos.teamid != board.turn: return True
		else : return False

def get_all_position(board, team="all"):
	'''Get all piece location'''
	if team == "all":
		return [translate(i.spec.coordinate) for i in board.all_members]
	else :
		return [translate(i.spec.coordinate) for i in board.all_members if i.teamid == board.turn]

def e_print_board(all_members):
	'''Return 2D array of board containing piece and Coord object if is empty'''
	assert len(all_members) == 32
	_copy_board = copy.deepcopy(def_coordXY)
	for _i in all_members:
		_copy_board[translate(_i.spec.coordinate) == def_coord] = _i
	return _copy_board

def e_get_board_dict(all_members):
	'''Return dictionary of board, {coord in str : piece}, if no piece, return -1'''
	K = {}
	for v in e_print_board(all_members).flatten():
		if isinstance(v, Piece): K[translate(v.spec.coordinate)] = v
		else: K[translate(v)] = -1	
	return K

def get_matlib_board(board):
    tab = np.zeros((8,8,3)) + 1/2
    tab[::2, ::2] = 1 
    tab[1::2, 1::2] = 1 

    positions = [(i , i.spec.coordinate) for i in board.all_members]

    fig, ax = plt.subplots()
    ax.imshow(tab, interpolation='nearest')

    for i, v in positions:
        ax.text(v[0], v[1], i.repr_img, size=30, ha='center', va='center')
    for v in def_coordXY.flatten():
        ax.text(v[0], v[1], str(v[0]) + " " + str(v[1]), size=10, ha='center', va='top')   
    ax.set(xticks=[], yticks=[])
    ax.invert_yaxis()
    plt.show()
	
 
    

def postcondition(possible_moves):
    return possible_moves

def random_setup():
    raise NotImplementedError