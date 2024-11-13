# Connect Four AI Game



This repository contains an implementation of a Connect Four game featuring an AI agent developed using the minimax algorithm with alpha-beta pruning. The game is played between an AI agent and a human player using a Pygame interface.

## Table of Contents
- [Zero Game Demo](#Zero-Game-Demo)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [AI Agent](#ai-agent)
- [How to Play](#how-to-play)
- [References](#references)

## Zero-Game-Demo

<video src="zero_game_demo.mp4" controls></video>
https://www.dropbox.com/scl/fi/xzui1ekxqz68i406pfqct/zero_game.py-contest-Visual-Studio-Code-2024-11-13-20-01-45.mp4?rlkey=m8bb5ffgpq6vdbi1z4zkzjzx0&st=8hou7dx2&dl=0

Got top 10% within around 1000 NUS CS students


https://www.dropbox.com/scl/fi/ql4ijkp0wm1ss7gcof91r/2024-11-12-175237.png?rlkey=bv1ag9y1flootox8b7919exlp&st=tq3wo7hj&dl=0

## Features
- Connect Four game simulation using Pygame.
- Human vs AI gameplay.
- AI agent uses the minimax algorithm with alpha-beta pruning to make intelligent moves.
- Easy-to-use interface for interacting with the game.

## Requirements
To run this game, the following dependencies are required:

- Python 3.x
- Pygame
- NumPy

You can install the dependencies using the following command:

```bash
pip install pygame numpy
```

## Installation
1. Clone this repository:

   ```bash
   git clone https://github.com/lukeshim/connect4AI.git
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the Connect Four game, use the following command:

```bash
python zero_game.py
```

The game will open a window where you can play against the AI.

## AI Agent
The AI agent is implemented using the minimax algorithm with alpha-beta pruning. It evaluates possible moves up to a specified depth, attempting to choose the optimal move based on maximizing its own score and minimizing the opponent's score.

The AI considers different board configurations and assigns scores based on potential win conditions. Key features include:
- **Center Column Preference:** The AI gives priority to the center column, as placing pieces there increases the likelihood of a win.
- **Window Evaluation:** The AI uses a sliding window technique to evaluate different possible 4-in-a-row combinations for scoring.
- **Alpha-Beta Pruning:** This technique is used to reduce the number of nodes evaluated, improving the efficiency of the minimax algorithm.

## How to Play
- Player 1 is the AI agent, and Player 2 is the human player.
- The objective of the game is to get four of your pieces in a row (horizontally, vertically, or diagonally).
- The human player takes turns by clicking on the desired column in the Pygame window to drop their piece.
- The game ends when either player gets four in a row, or if the board is full (resulting in a draw).

## References
- The AI agent uses a variation of the classic minimax algorithm with alpha-beta pruning for efficiency. For more information on the minimax algorithm, see [this article](https://en.wikipedia.org/wiki/Minimax).
- Pygame library documentation: [Pygame Docs](https://www.pygame.org/docs/)
