🐸 FRIDGO — A Frog’s Journey Home

FRIDGO is a Python-based platformer game about a frog on a journey to find his home. Jump across platforms, collect stars, and see how far you can go!

🎮 How to Run the Game

🪟 Windows

Step 1: Install Python 3.13

Download Python 3.13 from the official Python website.

During installation, enable Add Python to PATH.

Step 2: Open the terminal in the project folder

Run these commands one by one:

py -3.13 --version
py -3.13 -m venv .venv313
.\.venv313\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pygame
python src/main.py

If PowerShell blocks environment activation, you can run the game without activating it:

.\.venv313\Scripts\python.exe -m pip install pygame
.\.venv313\Scripts\python.exe src/main.py

🍎 macOS

Step 1: Install Python 3.13

Download Python 3.13 from the official Python website.

Alternatively, if you have Homebrew installed, run:

brew install python@3.13

Step 2: Open the terminal in the project folder

Run these commands one by one:

python3.13 --version
python3.13 -m venv .venv313
source .venv313/bin/activate
python -m pip install --upgrade pip
python -m pip install pygame
python src/main.py

🕹️ Controls

* A / Left Arrow: Move left
* D / Right Arrow: Move right
* W / Up Arrow: Face upward
* Hold SPACE: Charge your jump
* Release SPACE: Jump

🐸 Your Adventure Begins!

Help Fridgo navigate the platforms, collect stars, and find his way home. Good luck, and enjoy the game!

