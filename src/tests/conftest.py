"""Shared test setup: make src/ importable, so tests can write
`from talkdesk.app import ...` however pytest is started."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
