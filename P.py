import numpy as np 

class Piece(object):

	def __init__(self, name=None, spec=None, idx=None, teamid=None):
		self.name = name
		self.idx = idx
		self.teamid = teamid
		self.spec = spec
		self.posible_move = []
		self.board = None
		self.is_alive = True
		self.print_n = True
		self.repr_img = None 
  
	def movable(self, curr_station):
		return self._movable(curr_station)
  
	def move(self, move_pos):
		self._board.validate_move(move_pos)

	def __repr__(self): 
		if not self.print_n:
			return "Team:{} Name:{} Position:{} ID:{} Alive:{}".format(
				self.teamid, self.name, self.spec.str_coordinate, self.idx, self.is_alive
				)
		else : return "({}){}".format(self.teamid, self.name)

class Queen(Piece):
	def __init__(self, **kwargs): 
		super().__init__(**kwargs)
		self.repr_img = u'\u2655'
	def _movable(self, val):
		return _diagonal_move() + _hv_move()

class Pawn(Piece):
	def __init__(self, **kwargs): 
		super().__init__(**kwargs)
		self.repr_img = u'\u2659'
  
	def _movable(self, val):
		return [(val[0], val[1]+1), (val[0], val[1]+2)]

class Knight(Piece):
	def __init__(self, **kwargs): 
		super().__init__(**kwargs)
		self.repr_img = u'\u2657'
  
	def _movable(self, val):
		return [(val[0]+1, val[1]+2), (val[0]+1, val[1]-2), (val[0]-1, val[1]+2), (val[0]-1, val[1]-2),
			(val[0]+2, val[1]+1), (val[0]+2, val[1]-1), (val[0]-2, val[1]+1), (val[0]-2, val[1]-1)]
 
class Bishop(Piece):
	def __init__(self, **kwargs): 
		super().__init__(**kwargs)
		self.repr_img = u'\u2658'
  
	def _movable(self, val):
		return _diagonal_move(val)
     
class Rook(Piece):
	def __init__(self, **kwargs): 
		super().__init__(**kwargs)
		self.repr_img = u'\u2656'
  
	def _movable(self, val):
		return _hv_move(val)

class King(Piece):
	def __init__(self, **kwargs): 
		super().__init__(**kwargs)
		self.repr_img = u'\u2654'
  
	def _movable(self, val):
		return [(val[0]+1, val[1]+1), (val[0]+1, val[1]), (val[0]+1, val[1]-1), 
			(val[0]-1, val[1]+1), (val[0]-1, val[1]), (val[0]-1, val[1]-1),
			(val[0], val[1]+1), (val[0], val[1]-1)]
  
def _diagonal_move(var):
	_D = []
	_D += [(var[0]+i, var[1]+i) for i in range(1, 8)] 
	_D += [(var[0]-i, var[1]-i) for i in range(1, 8)]
	_D += [(var[0]+i, var[1]-i) for i in range(1, 8)]
	_D += [(var[0]-i, var[1]+1) for i in range(1, 8)]
	return _D

def _hv_move(var):
	_D = []
	_D += [(var[0]+i, 0) for i in range(1, 8)] 
	_D += [(var[0]-i, 0) for i in range(1, 8)]
	_D += [(0, var[1]-i) for i in range(1, 8)]
	_D += [(0-i, var[1]+i) for i in range(1, 8)]
	return _D 


