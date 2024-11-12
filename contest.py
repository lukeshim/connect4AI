from game_utils import initialize, step, get_valid_col_id

c4_board = initialize()
print(c4_board.shape)

print(c4_board)

get_valid_col_id(c4_board)

step(c4_board, col_id=2, player_id=1, in_place=True)

print(c4_board)

step(c4_board, col_id=2, player_id=2, in_place=True)
step(c4_board, col_id=2, player_id=1, in_place=True)
step(c4_board, col_id=2, player_id=2, in_place=True)
step(c4_board, col_id=2, player_id=1, in_place=True)
step(c4_board, col_id=2, player_id=2, in_place=True)
print(c4_board)

print(get_valid_col_id(c4_board))

step(c4_board, col_id=2, player_id=1, in_place=True)

class ZeroAgent(object):
    def __init__(self, player_id=1):
        pass
    def make_move(self, state):
        return 0

# Step 1
agent1 = AIAgent(player_id=1) # Yours, Player 1
agent2 = ZeroAgent(player_id=2) # Opponent, Player 2

# Step 2
contest_board = initialize()

# Step 3
p1_board = contest_board.view()
p1_board.flags.writeable = False
move1 = agent1.make_move(p1_board)

# Step 4
step(contest_board, col_id=move1, player_id=1, in_place=True)

from simulator import GameController, HumanAgent
from connect_four import ConnectFour

board = ConnectFour()
game = GameController(board=board, agents=[HumanAgent(1), HumanAgent(2)])
game.run()

## Task 1.1 Make a valid move

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
        pass
    def make_move(self, state):
        """
        Determines and returns the next move for the agent based on the current game state.

        Parameters:
        -----------
        state : np.ndarray
            A 2D numpy array representing the current, read-only state of the game board. 
            The board contains:
            - 0 for an empty cell,
            - 1 for Player 1's piece,
            - 2 for Player 2's piece.

        Returns:
        --------
        int
            The valid action, ie. a valid column index (col_id) where this agent chooses to drop its piece.
        """
        """ YOUR CODE HERE """
        raise NotImplementedError
        """ YOUR CODE END HERE """

def test_task_1_1():
    from utils import check_step, actions_to_board
    
    # Test case 1
    res1 = check_step(ConnectFour(), 1, AIAgent)
    assert(res1 == "Pass")
    
    # Test case 2
    res2 = check_step(actions_to_board([0, 0, 0, 0, 0, 0]), 1, AIAgent)
    assert(res2 == "Pass")
    
    # Test case 3
    res2 = check_step(actions_to_board([4, 3, 4, 5, 5, 1, 4, 4, 5, 5]), 1, AIAgent)
    assert(res2 == "Pass")

## Task 2.1: Defeat the Baby Agent

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
        pass
    def make_move(self, state):
        """
        Determines and returns the next move for the agent based on the current game state.

        Parameters:
        -----------
        state : np.ndarray
            A 2D numpy array representing the current, read-only state of the game board. 
            The board contains:
            - 0 for an empty cell,
            - 1 for Player 1's piece,
            - 2 for Player 2's piece.

        Returns:
        --------
        int
            The valid action, ie. a valid column index (col_id) where this agent chooses to drop its piece.
        """
        """ YOUR CODE HERE """
        raise NotImplementedError
        """ YOUR CODE END HERE """

def test_task_2_1():
    assert(True)
    # Upload your code to Coursemology to test it against our agent.

## Task 2.2: Defeat the Base Agent

class AIAgent(object):
    """
    A class representing an agent that plays Connect Four using Q-learning.
    """
    def __init__(self, player_id=1, epsilon=0.2, alpha=0.3, gamma=0.9):
        """Initializes the agent with the specified player ID.

        Parameters:
        -----------
        player_id : int
            The ID of the player assigned to this agent (1 or 2).
        epsilon : float
            The epsilon parameter for epsilon-greedy policy.
        alpha : float
            The learning rate.
        gamma : float
            The discount factor.
        """
        self.player_id = player_id
        self.epsilon = epsilon  # Chance of random exploration
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.q_table = {}       # Q-table to store state-action values
        self.prev_state = None  # Previous state
        self.prev_action = None # Previous action

    def state_to_key(self, state):
        """
        Converts the game state to a hashable key for the Q-table.

        Parameters:
        -----------
        state : np.ndarray
            The game state.

        Returns:
        --------
        tuple
            A hashable representation of the state.
        """
        return tuple(state.flatten())

    def get_q_value(self, state, action):
        """
        Retrieves the Q-value for a given state-action pair from the Q-table.

        Parameters:
        -----------
        state : np.ndarray
            The game state.
        action : int
            The action (column index).

        Returns:
        --------
        float
            The Q-value for the state-action pair.
        """
        state_key = self.state_to_key(state)
        if (state_key, action) not in self.q_table:
            # Initialize with optimistic value to encourage exploration
            self.q_table[(state_key, action)] = 1.0
        return self.q_table[(state_key, action)]

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
            The valid column index where this agent chooses to drop its piece.
        """
        # Get list of valid actions (columns that are not full)
        valid_actions = [col for col in range(state.shape[1]) if state[0, col] == 0]

        # Epsilon-greedy policy for action selection
        if random.random() < self.epsilon:
            # Explore: select a random valid action
            action = random.choice(valid_actions)
        else:
            # Exploit: select the action with the highest Q-value
            q_values = [self.get_q_value(state, a) for a in valid_actions]
            max_q = max(q_values)
            # If multiple actions have the same max Q-value, choose one at random
            if q_values.count(max_q) > 1:
                best_actions = [a for a, q in zip(valid_actions, q_values) if q == max_q]
                action = random.choice(best_actions)
            else:
                action = valid_actions[q_values.index(max_q)]

        # Store the state and action for learning
        self.prev_state = state.copy()
        self.prev_action = action

        return action

    def update_q_value(self, next_state, reward, terminated):
        """
        Updates the Q-table based on the reward received and the next state.

        Parameters:
        -----------
        next_state : np.ndarray
            The state after the action has been taken.
        reward : float
            The reward received after taking the action.
        terminated : bool
            Whether the game has ended.

        """
        if self.prev_state is not None and self.prev_action is not None:
            prev_state_key = self.state_to_key(self.prev_state)
            prev_action = self.prev_action
            prev_q = self.get_q_value(self.prev_state, prev_action)

            if terminated:
                max_future_q = 0
            else:
                # Get the maximum Q-value for the next state
                valid_actions = [col for col in range(next_state.shape[1]) if next_state[0, col] == 0]
                if valid_actions:
                    future_qs = [self.get_q_value(next_state, a) for a in valid_actions]
                    max_future_q = max(future_qs)
                else:
                    max_future_q = 0

            # Q-learning formula to update Q-value
            new_q = prev_q + self.alpha * (reward + self.gamma * max_future_q - prev_q)
            self.q_table[(prev_state_key, prev_action)] = new_q

            # Reset previous state and action if the game has ended
            if terminated:
                self.prev_state = None
                self.prev_action = None

def test_task_2_2():
    assert(True)
    # Upload your code to Coursemology to test it against our agent.


if __name__ == '__main__':
    test_task_1_1()
    test_task_2_1()
    test_task_2_2()