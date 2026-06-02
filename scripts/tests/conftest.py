import pathlib
import sys

# Make the scripts/ dir importable so tests can `import _github`, `import open_pr`, etc.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
