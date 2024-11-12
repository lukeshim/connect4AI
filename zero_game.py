import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'  # Uncomment if needed
from pygame_simulator import GameControllerPygame, HumanPygameAgent
from connect_four import ConnectFour
import random

import numpy as np

class ZeroAgent(object):
    def __init__(self, player_id):
        pass
    def make_move(self, state):
        return 0
import numpy as np
import random

class AIAgent(object):
    """
    A class representing an agent that plays Connect Four.
    """
    def __init__(self, player_id=1):
        """Initializes the agent with the specified player ID.
        Parameters:
        -----------
        player_id : int
            The ID of the player assigned to this agent (1 or 2).
        """
        self.player_id = player_id
        self.opp_player_id = 3 - player_id
        # Precompute window indices for all possible 4-in-a-row combinations
        self.window_row_indices, self.window_col_indices = self.get_window_indices()
    def get_window_indices(self):
        ROW_COUNT, COLUMN_COUNT = 6, 7
        window_row_indices = []
        window_col_indices = []
        # Horizontal windows
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT - 3):
                window_rows = [row] * 4
                window_cols = [col + i for i in range(4)]
                window_row_indices.append(window_rows)
                window_col_indices.append(window_cols)
        # Vertical windows
        for row in range(ROW_COUNT - 3):
            for col in range(COLUMN_COUNT):
                window_rows = [row + i for i in range(4)]
                window_cols = [col] * 4
                window_row_indices.append(window_rows)
                window_col_indices.append(window_cols)
        # Positive diagonal windows
        for row in range(3, ROW_COUNT):
            for col in range(COLUMN_COUNT - 3):
                window_rows = [row - i for i in range(4)]
                window_cols = [col + i for i in range(4)]
                window_row_indices.append(window_rows)
                window_col_indices.append(window_cols)
        # Negative diagonal windows
        for row in range(ROW_COUNT - 3):
            for col in range(COLUMN_COUNT - 3):
                window_rows = [row + i for i in range(4)]
                window_cols = [col + i for i in range(4)]
                window_row_indices.append(window_rows)
                window_col_indices.append(window_cols)
        return np.array(window_row_indices), np.array(window_col_indices)
    def make_move(self, state):
        """
        Determines and returns the next move for the agent based on the current game state.
        Parameters:
        -----------
        state : np.ndarray
            A 2D numpy array representing the current, read-only state of the game board.
        Returns:
        --------
        int
            The valid action, i.e., a valid column index (col_id) where this agent chooses to drop its piece.
        """
        ROW_COUNT, COLUMN_COUNT = state.shape
        MAX_DEPTH = 5  # Adjust depth for performance
        # Make a mutable copy of the state to avoid modifying the read-only array
        board = state.copy()
        board.flags.writeable = True
        def is_valid_location(board, col):
            return board[0, col] == 0
        def get_valid_locations(board):
            return np.where(board[0, :] == 0)[0]
        def get_next_open_row(board, col):
            rows = np.where(board[:, col] == 0)[0]
            if len(rows) == 0:
                return None
            else:
                return rows[-1]
        def drop_piece(board, row, col, piece):
            board[row, col] = piece
        def remove_piece(board, row, col):
            board[row, col] = 0
        def winning_move(board, piece):
            window_values = board[self.window_row_indices, self.window_col_indices]  # Shape: (number_of_windows, 4)
            is_winning_window = np.all(window_values == piece, axis=1)
            return np.any(is_winning_window)
        def is_terminal_node(board):
            return (
                winning_move(board, self.player_id)
                or winning_move(board, self.opp_player_id)
                or len(get_valid_locations(board)) == 0
            )
        def score_position(board, piece):
            score = 0
            opp_piece = self.opp_player_id
            # Center column preference
            center_col = COLUMN_COUNT // 2
            center_array = board[:, center_col]
            center_count = np.count_nonzero(center_array == piece)
            score += center_count * 3
            window_values = board[self.window_row_indices, self.window_col_indices]
            # Masks for counting
            piece_mask = window_values == piece
            empty_mask = window_values == 0
            opp_piece_mask = window_values == opp_piece
            piece_counts = np.sum(piece_mask, axis=1)
            empty_counts = np.sum(empty_mask, axis=1)
            opp_piece_counts = np.sum(opp_piece_mask, axis=1)
            # Scoring
            score += np.sum((piece_counts == 4) * 100000)
            score += np.sum(((piece_counts == 3) & (empty_counts == 1)) * 5)
            score += np.sum(((piece_counts == 2) & (empty_counts == 2)) * 2)
            score -= np.sum(((opp_piece_counts == 3) & (empty_counts == 1)) * 4)
            return score
        def order_moves(board, valid_locations, piece):
            scores = []
            for col in valid_locations:
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, piece)
                score = score_position(board, piece)
                remove_piece(board, row, col)
                scores.append((score, col))
            sorted_moves = [col for score, col in sorted(scores, reverse=True)]
            return sorted_moves
        def minimax(board, depth, alpha, beta, maximizingPlayer):
            valid_locations = get_valid_locations(board)
            is_terminal = is_terminal_node(board)
            if depth == 0 or is_terminal:
                if is_terminal:
                    if winning_move(board, self.player_id):
                        return (None, float('inf'))
                    elif winning_move(board, self.opp_player_id):
                        return (None, float('-inf'))
                    else:
                        return (None, 0)
                else:
                    return (None, score_position(board, self.player_id))
            if maximizingPlayer:
                value = float('-inf')
                best_col = random.choice(valid_locations)
                ordered_moves = order_moves(board, valid_locations, self.player_id)
                for col in ordered_moves:
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, self.player_id)
                    new_score = minimax(board, depth - 1, alpha, beta, False)[1]
                    remove_piece(board, row, col)
                    if new_score > value:
                        value = new_score
                        best_col = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break  # Beta cut-off
                return best_col, value
            else:
                value = float('inf')
                best_col = random.choice(valid_locations)
                ordered_moves = order_moves(board, valid_locations, self.opp_player_id)
                for col in ordered_moves:
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, self.opp_player_id)
                    new_score = minimax(board, depth - 1, alpha, beta, True)[1]
                    remove_piece(board, row, col)
                    if new_score < value:
                        value = new_score
                        best_col = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break  # Alpha cut-off
                return best_col, value
        valid_locations = get_valid_locations(board)
        if not len(valid_locations):
            raise ValueError("No valid moves")
        # Check for immediate winning moves
        for col in valid_locations:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, self.player_id)
            if winning_move(board, self.player_id):
                remove_piece(board, row, col)
                return col
            remove_piece(board, row, col)
        # Check for immediate opponent winning moves and block them
        for col in valid_locations:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, self.opp_player_id)
            if winning_move(board, self.opp_player_id):
                remove_piece(board, row, col)
                return col
            remove_piece(board, row, col)
        # Use minimax to decide the best move
        col, minimax_score = minimax(board, MAX_DEPTH, float('-inf'), float('inf'), True)
        if col is None:
            col = random.choice(valid_locations)
        return col

board = ConnectFour()
game = GameControllerPygame(board=board, agents=[AIAgent(1), HumanPygameAgent(2)])
winner_id = game.run()
print(f"Winner: Player {winner_id}")








