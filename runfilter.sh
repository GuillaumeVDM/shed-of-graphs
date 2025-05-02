#!/usr/bin/env bash
#
# runfilter.sh - Genereer en filter grafen met mensvriendelijke output
#
# Gebruik:
#   ./runfilter.sh <graph-order> '<JSON_FILTER>'
#
# Voorbeeld:
#   ./runfilter.sh 5 '{"rules":[{"type":"min","edges":2,"sumdeg":3}]}'

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <graph-order> '<JSON_FILTER>'"
  exit 1
fi

ORDER="$1"
FILTER_JSON="$2"

# Genereer alle niet-isomorfe grafen van orde $ORDER met geng (quiet mode)
# en pas daarop de Python-filter toe
filtered_output=$(geng -q "$ORDER" | python3 filter.py --filter "$FILTER_JSON")

# Als er geen grafen voldoen, geef een bericht en stop
if [ -z "$filtered_output" ]; then
  echo "Geen grafen voldeden aan de opgegeven filter."
  echo "Probeer de filtercriteria aan te passen of geef een ander aantal knopen."
  exit 0
fi

# Toon de gefilterde grafen in graph6-formaat
echo
echo "Gefilterde grafen (graph6-format):"
echo "$filtered_output"

# Tel en toon het aantal geslaagde grafen en de gebruikte filterinstellingen
count=$(echo "$filtered_output" | grep -c .)
echo
printf "==> %d grafen voldeden aan de filter: %s\n" "$count" "$FILTER_JSON"
