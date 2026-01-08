import sys
from pathlib import Path

# Add src to the python path so imports work correctly
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))
