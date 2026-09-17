import sys
from pathlib import Path

# Add src to the head of sys.path
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Directly import and run the main entry point
from agent import app