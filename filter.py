
#!/usr/bin/env python3
import sys
import json
import argparse
import networkx as nx
from datetime import datetime
import os
import matplotlib.pyplot as plt

HISTORY_FILE = 'history.txt'

"""
    load_rules laadt en valideert regels uit JSON-string.
    INPUT:
        Verwacht: filter_json = '{"rules":[{"type":"min","edges":3,"sumdeg":5}]}'
    RET:
        list[dict]
"""
def load_rules(filter_json: str):
    data = json.loads(filter_json)  # zet die JSON-string om in een Python-dict
    return data['rules']            # returns Python-lijst met dicts zoals {"type": "min", "edges": 3, "sumdeg": 5}

"""
    passes_rule checkt of een enkel filtercriterium (min, max of exact) klopt voor een gegeven graf.
    INPUT:
        edges = het aantal randen in de graf.
        degsum = de som van alle knoopgraden.
        rule = één filterregel, bv. {"type": "min", "edges": 3, "sumdeg": 5}

    typ = min, max of exact van de filterregel rule
    e = getal van rule waarmee je edges vergelijkt
    s = getal van rule waarmee je degsum vergelijkt

"""
def passes_rule(edges: int, degsum: int, rule: dict) -> bool:
    typ = rule['type']
    e = rule['edges']
    s = rule['sumdeg']
    if typ == 'min':
        # Vereist dat beide voorwaarden gelden
        return edges >= e and degsum >= s
    if typ == 'max':
        # Vereist dat beide voorwaarden gelden
        return edges <= e and degsum <= s
    if typ == 'exact':
        # Vereist dat beide voorwaarden gelden
        return edges == e and degsum == s
    return False

"""
    filter_graphs verwerkt de inkomende grafen (in graph6-formaat) en selecteert de grafen die álle regels uit je filterpassage doorstaan.
    INPUT:
        rules = de lijst van dicts uit load_rules

    RET:
        lijst passed met alle graph6-strings die voldoen aan de filtercriteria
"""
def filter_graphs(rules: list[dict]) -> list[str]:
    passed = [] # hierin gaan we alle graph6-strings verzamelen die voldoen
    for line in sys.stdin:  
        g6 = line.strip()   # verwijdert overbodige witruimte
        if not g6:          # lege regels overslaan
            continue
        try:
            G = nx.from_graph6_bytes(g6.encode())   # Parseren: networkx.from_graph6_bytes maakt van de textuele graph6-representatie een NetworkX-grafobject
        except Exception:
            continue
        edges = G.number_of_edges() # edges = totaal aantal randen in graf G.
        degsum = sum(dict(G.degree()).values()) # degsum = de som van alle knoopgraden
        if all(passes_rule(edges, degsum, rule) for rule in rules): # we loopen over alle rule-dicts in rules, checken rule, 
                                                                    # all() geeft alleen True als elk individueel passes_rule-resultaat True is
            passed.append(g6) # toevoegen van oorspronkelijke graph6-string
    return passed


"""
    Schrijf entry naar history.txt:
    <timestamp>\t<outputCount>\t<filter>\t<laatste20>\n
    INPUT:
        filter_str = de JSON-string die als filter diende
        passed = de lijst van graph6-strings filterd waren
"""
def save_history(filter_str: str, passed: list[str]):
    timestamp = datetime.now().isoformat(sep=' ') # tijd van wanneer de filter gerund werd (vb: "2025-05-06 14:23:45.123456")
    count = len(passed) # aantal geslaagde grafen
    last20 = passed[-20:]   # lijst met alle 20 laatste geslaagde grafen
    entry = f"{timestamp}\t{count}\t{filter_str}\t{','.join(last20)}\n"  # de data in string vorm
    with open(HISTORY_FILE, 'a') as f: # opent of maakt history.txt en voegt nieuwe regel er aan toe
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="Eenvoudige graph6-filter.")
    parser.add_argument('--filter', '-f', required=True, help='JSON-string met regels') # verplicht argument toe: --filter of kort -f
    parser.add_argument(
        '--export', '-e', nargs=2, metavar=('TYPE', 'FOLDER'),
        help='Enable exporting of filtered graphs; TYPE must be "image" and FOLDER is output directory'
    )
    parser.add_argument(
        '--image-format', default='png',
        help='Image format for export (e.g. png, jpg)'
    )
    args = parser.parse_args() # zorgt ervoor dat het script stopt met een foutmelding als je dit argument niet meegeeft.
    
    filter_str = args.filter # Haalt de tekst uit args.filter en bewaart als filter_str
    rules = load_rules(filter_str) # roept load_rules aan om van die JSON-string een lijst van rule-dicts te krijgen.
    passed = filter_graphs(rules) # passed is een lijst van graph6-strings die aan alle regels voldoen

    if not passed:  # als passed leeg is, beëindigt het script met een foutmelding
        sys.exit("Geen grafen voldeden aan de filter.")

    for g in passed: # print elke graaf uit passed
        print(g)

    save_history(filter_str, passed) # bewaar de gegeven JSON-string en grafen in history.txt

     # Export images if requested
    if args.export and args.export[0].lower() == 'image':
        out_dir = args.export[1]
        os.makedirs(out_dir, exist_ok=True)
        for idx, g6 in enumerate(passed):
            # Reconstruct graph and draw
            G = nx.from_graph6_bytes(g6.encode())
            fig = plt.figure()
            nx.draw(G, with_labels=False)

            # Save figure
            img_path = os.path.join(out_dir, f'graph_{idx}.{args.image_format}')
            fig.savefig(img_path, format=args.image_format)
            plt.close(fig)

if __name__ == '__main__':
    main()
