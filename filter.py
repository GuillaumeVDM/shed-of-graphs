#!/usr/bin/env python3

import sys
import json
import argparse
import networkx as nx
from datetime import datetime

# Naam van het historie-bestand (in de huidige map)
HISTORY_FILE = 'history.txt'


def parse_args():
    parser = argparse.ArgumentParser(
        description="Filter graph6 graphs by degree-sum rules.")
    parser.add_argument(
        "--filter", "-f", required=True,
        help="JSON string defining filter rules; see script doc for format.")
    return parser.parse_args()


def load_filter_config(filter_text):
    try:
        config = json.loads(filter_text)
    except json.JSONDecodeError as e:
        sys.exit(f"Error: invalid JSON filter: {e}")
    if "rules" not in config or not isinstance(config["rules"], list):
        sys.exit("Error: filter JSON must have a 'rules' list.")
    # Validate each rule
    for rule in config["rules"]:
        if not all(key in rule for key in ("type", "edges", "sumdeg")):
            sys.exit("Error: each rule must have 'type', 'edges', and 'sumdeg'.")
        if rule["type"] not in ("min", "max", "exact"):
            sys.exit("Error: rule type must be 'min', 'max', or 'exact'.")
    return config


def passes_all_rules(graph, rules):
    degrees = dict(graph.degree())
    for rule in rules:
        count = 0
        for u, v in graph.edges():
            if degrees[u] + degrees[v] == rule["sumdeg"]:
                count += 1
        if rule["type"] == "min" and count < rule["edges"]:
            return False
        elif rule["type"] == "max" and count > rule["edges"]:
            return False
        elif rule["type"] == "exact" and count != rule["edges"]:
            return False
    return True


def main():
    args = parse_args()
    filter_config = load_filter_config(args.filter)
    filter_text = args.filter  # bewaar originele JSON voor historie

    input_count = 0
    passed_graphs = []

    # Verwerk elke graph6-regel van stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            graph = nx.from_graph6_bytes(line.encode())
        except Exception:
            sys.stderr.write(f"Warning: skipped invalid graph6 line: {line}\n")
            continue
        input_count += 1
        if passes_all_rules(graph, filter_config["rules"]):
            passed_graphs.append(line)

    # Schrijf alle doorgekomen grafen naar stdout
    for g in passed_graphs:
        sys.stdout.write(g + "\n")

    # Voeg een gestructureerde entry toe aan de historie
    timestamp = datetime.now().isoformat(sep=' ')
    output_count = len(passed_graphs)
    recent20 = passed_graphs[-20:]
    separator = '=' * 60

    with open(HISTORY_FILE, "a") as hist:
        hist.write(separator + "\n")
        hist.write(f"Timestamp      : {timestamp}\n")
        hist.write(f"Input graphs   : {input_count}\n")
        hist.write(f"Output graphs  : {output_count}\n")
        hist.write(f"Filter         : {filter_text}\n")
        hist.write("Last 20 passed : " + ", ".join(recent20) + "\n")
        hist.write("\n")


if __name__ == "__main__":
    main()
