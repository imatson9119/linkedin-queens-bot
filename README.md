# ♛ LinkedIn Queens Bot

Conquer the LinkedIn Queens puzzle with zero effort.  
This bot logs in, solves the board, and flexes your brain cells so you don’t have to.

## 🧠 What It Does

This bot plays LinkedIn's *Queens* game by:
1. Logging into your LinkedIn account (via saved cookies)
2. Skipping the fluff (like tutorials)
3. Solving the puzzle using a backtracking algorithm
4. Simulating natural human movement (because bots shouldn’t look like bots)
5. Clicking through the correct solution — and optionally grabbing a screenshot as proof

## 🧰 Requirements

- Python 3.11+
- Chrome installed

## ⚙️ Setup

Clone it:
```bash
git clone https://github.com/yourusername/linkedin-queens-bot.git
cd linkedin-queens-bot
````

Install with Poetry:

```bash
poetry install
```

Or with pip:

```bash
pip install undetected-chromedriver==3.5.5 selenium==4.32.0 humancursor==1.1.5
```

## 🚀 Usage

Run the bot:

```bash
poetry run python -m linkedin_queens_bot.main
```

Or:

```bash
python -m linkedin_queens_bot.main
```

### First-Time Setup

1. Browser launches → You log into LinkedIn manually
2. Press `Enter` in the terminal once logged in
3. The session gets saved
4. Bot does its thing from then on

## 🧩 How It Works

* `main.py`: Browser automation & game interaction
* `solver.py`: Brains behind the operation

  * Solves via recursive backtracking
  * Prioritizes cells with the fewest options first (like a real chess prodigy)

## 🙋 Author

Made by Ian Matson
📧 [imatson9119@gmail.com](mailto:imatson9119@gmail.com)