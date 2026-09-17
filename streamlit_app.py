import sys
from pathlib import Path

# Add src to sys.path so 'agent.*' imports resolve anywhere
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Run the app code
import runpy
runpy.run_path(str(SRC_DIR / "agent" / "app.py"), run_name="__main__")