# TicTacToe RL Agent

A reinforcement learning agent trained with Q-learning to play Tic-Tac-Toe against a human player.

---

## ⚙️ Setup

### Prerequisites

- Python 3.8+
- pip

### Install dependencies

```bash
pip install flask numpy matplotlib
```

### Project structure

Make sure your folder looks like this before running:

```
TicTacToe-RL-Agent/
├── interface.py
├── tic_tac_toe.py
├── q_table.json
└── templates/
    └── index.html
```

---

## ▶️ Running the App

```bash
python interface.py
```

Then open **http://localhost:5000** in your browser.

---

## 🏋️ Retraining the Agent (optional)

```bash
python RL_agent_train.py
```

This runs 50,000 training episodes and overwrites `q_table.json`.

---

## 🖥️ CLI Mode (optional)

To play in the terminal instead of the browser:

```bash
python game_loop.py
```
