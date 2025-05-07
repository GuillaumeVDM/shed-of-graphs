# test_filter.py
import io
import sys
import pytest
import networkx as nx # grafen te bouwen en naar graph6-formaat om te zetten

from filter import load_rules, filter_graphs # testen van deze functies

"""
    We gebruiken één vaste graf (bijv. een pad van 3 knopen, dus 2 edges en sumdeg 4) 
    en variëren alleen de filterregels: eerst een regel die exact bij die waarden past 
    en controleren dat de graf in de outputlijst verschijnt, dan een regel die er niet bij past 
    en bevestigen dat de lijst leeg blijft. 
    Daarnaast verifiëren we dat load_rules bij ongeldige JSON een fout werpt. 
    Hiermee testen we zowel het juiste doorlaten als blokkeren van grafen én de foutafhandeling.
 """

def make_graph6(G: nx.Graph) -> str:
    """Helper: converteer NetworkX-graaf naar graph6-string (zonder header)."""
    return nx.to_graph6_bytes(G, header=False).decode().strip()

def test_exact_edges_pass(monkeypatch):
    # Bouw een padgraf met 3 knopen, 2 edges, sumdeg = 4
    G = nx.path_graph(3)    # bouwt een lijn (path) met 3 knopen
    g6 = make_graph6(G)     # zet die graph om in een graph6-string

    # filterregel die exact 2 edges en sumdeg 4 eist
    rules = load_rules('{"rules":[{"type":"exact","edges":2,"sumdeg":4}]}')

    # Stub sys.stdin zodat filter_graphs daaruit leest
    monkeypatch.setattr(sys, "stdin", io.StringIO(g6 + "\n"))

    # output-lijst passed moet exact de ene string g6 bevatten
    passed = filter_graphs(rules)
    assert passed == [g6] # de test faalt als dit niet zo is

def test_exact_edges_fail(monkeypatch):
    # Zelfde graph, maar eist exact 3 edges (fout)
    G = nx.path_graph(3)
    g6 = make_graph6(G)

    # Hier eist de filter 3 edges en sumdeg 6, maar onze graf heeft slechts 2 edges en sumdeg 4.
    rules = load_rules('{"rules":[{"type":"exact","edges":3,"sumdeg":6}]}')
    monkeypatch.setattr(sys, "stdin", io.StringIO(g6 + "\n"))

    passed = filter_graphs(rules)
    assert passed == []  # geen enkele graf voldoet

def test_invalid_json():
    # test verifieert simpelweg dat load_rules een fout gooit 
    # zodra je er iets instopt wat géén geldige JSON is
    with pytest.raises(ValueError):
        load_rules("dit is geen JSON")
