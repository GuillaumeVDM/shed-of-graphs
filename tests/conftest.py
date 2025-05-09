# test/conftest.py
import sys, os

# Voeg de project-root (één niveau hoger) toe aan de import-path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)
