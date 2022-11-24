import numpy as np
import time 
from copy import deepcopy

from P import *
from chess_utils import *

class Chess:
	'''A Chess class handle all backend component for a board and consist of 2 "Agent".'''
	def __init__(self):
		self.logger = [] 
		self.turn = 0
		self.agentA = None
		self.agentB = None
		self.terminated_members = []
	@property # members of all pieces, not including terminated pieces
	def all_members(self): return (*self.agentA.members, *self.agentB.members)

	@property
	def state(self): return e_print_board(self.all_members)
 
	def initialize_board(self):
		self.agentA = Agent(agent_id=0, board=self)
		self.agentB = Agent(agent_id=1, board=self)

	def eliminate_piece(self, piece):
		'''Eliminate piece instantly'''
		piece.is_alive = False
		self.terminated_members.append(piece)
		if piece.teamid == 0: self.agentA.members.remove(piece)
		else: self.agentB.members.remove(piece)
	
	def raise_checkmate(self, piece):
		'''Raise checkmate event'''
		if self.turn == 0:
			move_a = self.agentA.get_possible_move()
			if self.agentA.get_piece("king0").spec.coordinate in move_a:
				self.agentA.checkmate = True
		else:
			move_b = self.agentB.get_possible_move()
			if self.agentB.get_piece("king1").spec.coordinate in move_b:
				self.agentB.checkmate = True
    
	def promote_pawn(self, piece, value):
		'''Promote pawn'''
		pass

class Agent:
	'''Representation of a player'''
	def __init__(self, agent_id, board):
		self.agent_id = agent_id
		self.members = all_piece_initializer(teamid=agent_id)
		self.left = self.members
		self.been_checked_mate = False
		self.board = board
		self.history = {}
	
	def get_possible_move(self):
		return {piece: self.get_valid_move(piece) for piece in self.members}
	
	def get_valid_move(self, piece):
		# return a list of valid move for given piece
		occupied = [translate(c).xy for c in get_all_position(self.board)]
		if isinstance(piece, Pawn):
			def _d_pawn(val): # val is instance of Coord, is overloaded returning tuple of (x, y)	
				_p = []
				if piece.spec.coordinate.xy in [(i, 6) for i in range(8)] + [(i, 1) for i in range(8)]: # if this is the first move
					if not (val + (0, 1) in occupied):  
						_p += [val + (0, 1)] 
						if not (val + (0, 2) in occupied): 
							_p += [val + (0, 2)]
				else: 
					if not (val + (0, 1) in occupied): _p += [val + (0, 1)]

				if check_is_empty(self.board, val + (1, 1), team="opponent"): # if opponent piece is on the right diagonal
					_p += [val + (1, 1)]
				if check_is_empty(self.board, val + (-1, 1), team="opponent"):	# if opponent piece is on the left diagonal	
					_p += [val + (-1, 1)] 

				_p = del_out_of_bound(_p) # remove out of bound move
				_p = set.difference(set(occupied), set(_p)) # remove occupied move

				return _p

			_d_pawn(piece.spec.coordinate)
   
		if isinstance(piece, Knight):
			def _d_knight(val):
				_p = set.difference(piece.movable(val), set(get_all_position(self.board))) # delete all the position that is occupied by the same team
				for _px in _p:
					if _px[0] not in range(8) or _px[1] not in range(8): _p.remove(_px) # remove out of bound move
				return _p
			_d_knight(piece.spec.coordinate.xy)
   
		if isinstance(piece, Bishop):
			def _d_bishop(val): 
				_p = piece.movable(val)
				for _px in _p:
					if _px[0] not in range(8) or _px[1] not in range(8): _p.remove(_px)
					if _px in get_all_position(self.board):
						pass
					
		if isinstance(piece, Rook):
			def _d_rook(val):
				_p = piece.movable(val)
				for _px in _p:
					if _px[0] not in range(8) or _px[1] not in range(8): _p.remove(_px)
					if _px in get_all_position(self.board):
						pass
  
		if isinstance(piece, Queen):
			def _d_queen(val):
				return None
		
		if isinstance(piece, King):
			def _d_king(val):
				_p = set.difference(piece.movable(val), set(get_all_position(self.board)))
				return _p

	def move(self, piece, value):
		# assume value and piece is valid
		self.assert_move(piece, value)
		piece.spec.coordinate.xy = value
		self.board.position = e_print_board(self.board.all_members)
		# self.board.raise_elimination(piece, value)
  
	def assert_move(self, piece, value):
     
		assert self.board.turn == self.agent_id, "Incorrect moving turn"
		assert piece in self.left, "Piece is terminated, cannot move"
		assert isinstance(value, (tuple, list)), "Value must be a tuple or list"
		assert len(value) == 2, "Value must be a tuple or list of length 2, (x, y)"
		assert value[0] in range(8) and value[1] in range(8), \
  			"Value must be a tuple or list of length 2, (x, y) where x and y is in range(8)"
		assert check_is_empty(self.board, value, team="self"),\
      		"Cannot move to a position that is occupied by the same team"
		assert value in self.get_valid_move(piece), "Invalid move"
		self.board.raise_check_mate()

	def get_piece(self, name):
		for piece in self.members:
			if piece.name == name: return piece
		return None

