# test_history.py
import os
import sys
import pytest
import tempfile

from filter import save_history # testen van functie save_history

def test_save_history_appends_and_formats(monkeypatch, tmp_path):
    # Verander de huidige werkmap naar een tijdelijke map
    monkeypatch.chdir(tmp_path)

    # controleert of er nog geen history.txt bestaat
    hist = tmp_path / "history.txt"
    assert not hist.exists()

    # Roep save_history twee keer aan met verschillende inputs
    save_history('{"rules":[{"type":"min","edges":1,"sumdeg":2}]}',
                 ["g6a"])
    save_history('{"rules":[{"type":"max","edges":5,"sumdeg":8}]}',
                 ["g6x","g6y","g6z"])

    # Nu moet history.txt bestaan en twee regels bevatten
    assert hist.exists()
    lines = hist.read_text().strip().splitlines()
    assert len(lines) == 2

    # Controleer de inhoud van de eerste regel
    parts1 = lines[0].split("\t")
    # parts1[0] = timestamp (niet exact controleerbaar)
    assert parts1[1] == "1"  # een gepasseerde graf
    assert '{"rules":[{"type":"min","edges":1,"sumdeg":2}]}' in parts1[2]
    assert parts1[3] == "g6a"

    # Controleer de tweede regel analogisch
    parts2 = lines[1].split("\t")
    assert parts2[1] == "3"
    assert '{"rules":[{"type":"max","edges":5,"sumdeg":8}]}' in parts2[2]
    assert parts2[3] == "g6x,g6y,g6z"
