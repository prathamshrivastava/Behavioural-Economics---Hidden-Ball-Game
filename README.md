#  Behavioral Economics Game – Hidden Number (3-Player Game)

This is an interactive behavioral experiment designed for 3 players, focusing on strategic quoting and decision-making under uncertainty. The game simulates reward allocation dynamics based on hidden information and player choice.

---

## Game Concept

All three players are presented with **10 identical balls**, each hiding a number between **1 and 10** (inclusive). 

### Here's how it works:

1.  Each player clicks on **one random ball** to **reveal a number** (privately).
2.  The player then **quotes a number** in the input box below.  
   - The quoted number can be the same as the revealed number or any other number between 1 and 10.
3.  After all players have submitted their quoted numbers, **one player is randomly selected**.
4.  That selected player receives **the exact number of points they quoted**.
5.  The **other two players receive**: `11 - quoted_number` points each.

This setup creates a strategic tension between honesty, risk, and expected value.

---

##  Game Objective

The game is designed to analyze:
- Honesty in self-reported data
- Strategic misrepresentation in competitive settings
- Group dynamics and randomness in reward distribution

---

##  Interface Flow

- Users interact through a clean web interface.
- Each player selects and reveals one ball.
- They then enter their quoted number.
- After submission, rewards are computed and displayed.

---

##  Project Structure

| File / Directory     | Description                                        |
|----------------------|----------------------------------------------------|
| `BallGame.html`      | Main game interface for ball selection and input   |
| `__init__.py`        | Flask app backend with game logic and player states|
| `Result.html`        | Displays outcome and rewards for all players       |
| `Instruction.html`   | Conatains Detailed Instructions                    |
| `README.md`          | This documentation file                            |

---

##  Getting Started

### 🔧 Prerequisites
- Python 3.10
- Web Browser and Internet Connection

