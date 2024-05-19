# MCTS Hex Game
This repository contains the coursework for the AI & Games module. The project involves implementing two algorithms to solve the Hex game: Monte Carlo Tree Search (MCTS) with AlphaGo enhancements and the Minimax algorithm with Alpha-Beta Pruning. The goal is to evaluate and compare the performance of these algorithms in the context of the Hex game.

### Algorithms Implemented

1. Monte Carlo Tree Search (MCTS) with AlphaGo Enhancements
- Strengths:
  - Suitable for games with large state and action spaces.
  - Does not require an explicit evaluation function.
  - Can handle complex decision spaces and uncertainties.
  - Integrates deep neural networks for evaluating board positions and making strategic decisions.
- Key Techniques:
  - Upper Confidence Bound for Trees (UCT)
  - All Moves as First (AMAF)
  - Rapid Action Value Estimation (RAVE)
    
2. Minimax Algorithm with Alpha-Beta Pruning
- Strengths:
  - Efficient with a well-designed heuristic.
  - Effective for games with a smaller state space.
  - Provides a deterministic evaluation of game states.

## Project Development

### Team Division
- MCTS with AlphaGo: Chittesh Kumar Singore and Vedant Agrawal
- Minimax with Alpha-Beta Pruning: Suphal Sharma and Amaan Ahmad

### Key Project Stages

Research and Planning
- Understanding the rules of the Hex game.
- Researching AI algorithms and selecting suitable ones.
- Choosing Python for implementation.

Design and Development
- Implementing MCTS with enhancements such as RAVE.
- Comparing the performance of MCTS and Minimax algorithms.
- Optimizing the implementation for efficiency.

Mid-Project Review
- Identifying and solving potential errors.
- Deciding to focus on MCTS after comparing results.
- Utilizing Python libraries like NumPy for optimization.
  
Final Stages and Testing
- Completing presentation slides.
- Testing the algorithms against various test agents.
- Further optimizing the code to reduce execution time.

### Results
MCTS algorithm consistently outperformed Minimax in terms of efficiency and effectiveness in defeating test agents.
Conclusion

The project successfully demonstrated the application of advanced AI techniques to solve the Hex game. The MCTS algorithm with AlphaGo enhancements proved to be the more effective solution, handling complex decision spaces and uncertainties better than the Minimax algorithm with Alpha-Beta Pruning.
