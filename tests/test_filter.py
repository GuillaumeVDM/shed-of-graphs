import io
import sys
import json
import pytest
import networkx as nx
import importlib

# Importeer het filter-module onder een veilige naam
filter_module = importlib.import_module('filter')

# ------------------ Tests voor load_rules ------------------

def test_load_rules_valid():
    """
    Test of load_rules een geldige JSON-string correct inleest.
    We verifiëren dat bij een juiste invoer een lijst met regels wordt geretourneerd.
    Controleer dat de inhoud overeenkomt met het verwachte Python-dict.
    """
    json_str = '{"rules":[{"type":"min","edges":2,"sumdeg":3}]}'
    rules = filter_module.load_rules(json_str)
    assert isinstance(rules, list)
    assert rules == [{"type": "min", "edges": 2, "sumdeg": 3}]


def test_load_rules_missing_key():
    """
    Controleer dat load_rules een KeyError gooit als de 'rules'-key ontbreekt.
    We geven een JSON zonder de vereiste key om de exceptie te triggeren.
    De test slaagt als de juiste foutmelding wordt opgegooid.
    """
    json_str = '{}'
    with pytest.raises(KeyError):
        filter_module.load_rules(json_str)


def test_load_rules_invalid_json():
    """
    Bevestig dat load_rules een JSONDecodeError werpt bij ongeldige JSON.
    We gebruiken een verkeerd geformatteerde JSON-string als input.
    De test controleert dat de module de fout van de json-parser doorgeeft.
    """
    json_str = '{rules: [}'
    with pytest.raises(json.JSONDecodeError):
        filter_module.load_rules(json_str)

# ------------------ Tests voor passes_rule ------------------

def test_passes_rule_min():
    """
    Test de 'min'-regel door waarden te controleren boven en onder de grens.
    Verwacht True als het aantal edges >= drempel, anders False.
    Zo testen we de minimale voorwaarden voor edge-count.
    """
    rule = {"type": "min", "edges": 2}
    assert filter_module.passes_rule(2, rule)
    assert filter_module.passes_rule(3, rule)
    assert not filter_module.passes_rule(1, rule)


def test_passes_rule_max():
    """
    Test de 'max'-regel voor waarden onder of gelijk aan de max.
    Controleer dat waarden binnen de grens True opleveren.
    Waarden erboven moeten False geven.
    """
    rule = {"type": "max", "edges": 2}
    assert filter_module.passes_rule(1, rule)
    assert filter_module.passes_rule(2, rule)
    assert not filter_module.passes_rule(3, rule)


def test_passes_rule_exact():
    """
    Test de 'exact'-regel voor precieze edge-count.
    Alleen de exacte waarde geeft True.
    Andere waarden leveren False.
    """
    rule = {"type": "exact", "edges": 1}
    assert filter_module.passes_rule(1, rule)
    assert not filter_module.passes_rule(0, rule)
    assert not filter_module.passes_rule(2, rule)


def test_passes_rule_unknown_type():
    """
    Verifieer dat een onbekend regeltype altijd False retourneert.
    We gebruiken een niet-ondersteunde 'type' waarde.
    De functie moet zonder uitzondering False geven.
    """
    rule = {"type": "foo", "edges": 1}
    assert not filter_module.passes_rule(1, rule)
    assert not filter_module.passes_rule(0, rule)

# ------------------ Tests voor filter_graphs ------------------

def generate_graph6(graph):
    """Helper om een graph6-string zonder newline te maken"""
    return nx.to_graph6_bytes(graph).decode().strip()


def test_filter_graphs_no_rules(monkeypatch):
    """
    Test filter_graphs zonder regels: alle geldige graphs moeten doorgegeven worden.
    Voeg enkele ongeldige en lege invoerregels toe om te negeren.
    Controleer of alleen de juiste graph6-strings worden teruggegeven.
    """
    g_empty = generate_graph6(nx.empty_graph(3))
    g_path = generate_graph6(nx.path_graph(2))
    stdin_content = f"{g_empty}\n{g_path}\nnotagraph\n\n"
    monkeypatch.setattr(sys, 'stdin', io.StringIO(stdin_content))

    result = filter_module.filter_graphs([])
    assert result == [g_empty, g_path]


def test_filter_graphs_single_rule(monkeypatch):
    """
    Test filter_graphs met één regel: alleen graphs die aan die regel voldoen blijven over.
    We gebruiken een exact-regel op edges en sumdeg.
    Verwacht dat alleen de pad-graph wordt geretourneerd.
    """
    g_empty = generate_graph6(nx.empty_graph(3))
    g_path = generate_graph6(nx.path_graph(2))
    stdin_content = f"{g_empty}\n{g_path}\n"
    monkeypatch.setattr(sys, 'stdin', io.StringIO(stdin_content))

    rule = {"type": "exact", "edges": 1, "sumdeg": 2}
    result = filter_module.filter_graphs([rule])
    assert result == [g_path]


def test_filter_graphs_multiple_rules(monkeypatch):
    """
    Test filter_graphs met gecombineerde min- en max-regels.
    Samen vormen ze een exacte voorwaarde.
    Controleer dat de pad-graph geselecteerd wordt.
    """
    g_path = generate_graph6(nx.path_graph(2))
    stdin_content = f"{g_path}\n"
    monkeypatch.setattr(sys, 'stdin', io.StringIO(stdin_content))

    rules_json = '{"rules":[{"type":"min","edges":1,"sumdeg":2},{"type":"max","edges":1,"sumdeg":2}]}'
    rules = filter_module.load_rules(rules_json)
    result = filter_module.filter_graphs(rules)
    assert result == [g_path]


def test_filter_graphs_empty_input(monkeypatch):
    """
    Test filter_graphs met lege stdin: moet een lege lijst retourneren.
    Geen invoer betekent geen output.
    Voorkom fouten bij empty input.
    """
    monkeypatch.setattr(sys, 'stdin', io.StringIO(""))
    result = filter_module.filter_graphs([])
    assert result == []

# ------------------ Tests voor save_history ------------------

def test_save_history(tmp_path, monkeypatch):
    """
    Test het opslaan van de filter-historie met vaste timestamp.
    Gebruik een tijdelijke file en dummy datetime om output te verifiëren.
    Controleer dat de inhoud exact overeenkomt met de verwachte regel.
    """
    history_file = tmp_path / "history_test.txt"
    monkeypatch.setattr(filter_module, 'HISTORY_FILE', str(history_file))

    class DummyDateTime:
        @staticmethod
        def now():
            import datetime as dt
            return dt.datetime(2025, 1, 1, 12, 0, 0)
    monkeypatch.setattr(filter_module, 'datetime', DummyDateTime)

    filter_str = '{"rules":[{"type":"exact","edges":2,"sumdeg":3}]}'
    passed = ['g6_a', 'g6_b']

    filter_module.save_history(filter_str, passed)
    content = history_file.read_text()

    expected_timestamp = "2025-01-01 12:00:00"
    expected_entry = f"{expected_timestamp}\t{len(passed)}\t{filter_str}\t{','.join(passed)}\n"
    assert content == expected_entry
