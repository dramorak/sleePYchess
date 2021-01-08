#! /usr/bin/python3
"""
SleepyChess v0.1

Chess AI. Features variable search depth, piece-capture node evaluation,
minimax board evaluation and a basic alpha-beta optimization method.

Dev notes:
    -positive board evaluation represents white advantage
    -Program works most effectively at depth = 4 (still bad)
Stats
Search depth:Time:Node Evaluations:mean nodes/second

    1: 00.051   : 21       : 403
    2: 00.375   : 60       : 1602
    3: 00.157   : 581      : 3711
    4: 00.329   : 1516     : 4607
    5: 04.465   : 22463    : 5031
    6: 91.060   : 451555   : 4959 
    7: -----    : -----    : -----
    
"""
      
import sys, chess, logging, time
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logging.disable(logging.CRITICAL)


#Convenience function. Returns the max of a list if its white's turn, returns the min of the list if it's black's.
def minimax(moves,turn):
    current = moves[0]
    
    if turn: #white's move
        for i in moves:
            if i[0] > current[0]:
                current = i
    elif not turn: #black's move
        for i in moves:
            if i[0] < current[0]:
                current = i
    
    return current

#Naive evaluation of board position
#Weighted difference of board pieces.
def heval(board):
    piece_val = {1:10, 2:30, 3:30, 4:50, 5:90, 6:3200} 
    result = 0
    for i in range(1,7): 
        result += piece_val[i]*(len(board.pieces(piece_type = i, color = True))-len(board.pieces(piece_type = i, color = False)))
    return result

#Finds best move from current position.
#Returns tuple: (move value, move literal)
def best_move(board, current_depth, target_depth, a=-float('inf'), b=float('inf')):

    
    global leaf_count
    global node_count
    node_count += 1
    
    if current_depth == target_depth:   #Return heuristic evaluation
        leaf_count += 1
        return (heval(board),)
        
    else:
        move_evaluations = []

        if board.turn: #White's move, max step

            for move in board.legal_moves:
     
                board.push(move)
                
                comp_move = (best_move(board,current_depth+1, target_depth, a, b)[0],move)

                a = max(a,comp_move[0])
                if comp_move[0] > b:
                    board.pop()
                    return (comp_move[0],)
                
                move_evaluations.append(comp_move)

                board.pop()
            
        else: #Black's move, min step

            for move in board.legal_moves:
                
                board.push(move)
                
                comp_move = (best_move(board, current_depth+1,target_depth,a,b)[0],move)

                b = min(b,comp_move[0])
                if comp_move[0] < a:
                    board.pop()
                    return (comp_move[0],)

                move_evaluations.append(comp_move)

                board.pop()
            
        if move_evaluations:    #if there are legal moves.   
            return minimax(move_evaluations, board.turn)
        else:

            if board.is_checkmate() and board.turn:
                return (3200,)
            elif board.is_checkmate() and not board.turn:
                return (-3200,)
            elif board.is_stalemate:
                return (0,)


