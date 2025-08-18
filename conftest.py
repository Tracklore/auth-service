import sys
from pathlib import Path

# Add the shared-libs directory to the Python path
shared_libs_path = Path(__file__).resolve().parent.parent / "shared-libs"
sys.path.append(str(shared_libs_path))