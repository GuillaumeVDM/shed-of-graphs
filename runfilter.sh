#!/usr/bin/env bash
#
# runfilter.sh - Genereer en filter grafen met mensvriendelijke output
#
# Gebruik:
#   ./runfilter.sh <graph-order> '<JSON_FILTER>'
#
# Voorbeeld:
#   ./runfilter.sh 5 '{"rules":[{"type":"min","edges":2,"sumdeg":3}]}'

set -euo pipefail # e: stop meteen bij elke fout, u: fout als je een ongedefinieerde variabele gebruikt, als een commando in een pipe faalt, stopt het hele script

# "$#" staat voor aantal argumenten. Dit moet gelijk zijn aan twee. 
# $0 = naam van het script (vb: ./runfilter.sh)
# We want at least 2 args, but allow extras (to forward to filter.py)
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <graph-order> '<JSON_FILTER>' [filter.py options …]"
  exit 1
fi

ORDER="$1"       # aantal knopen per graaf (vb: 5)
FILTER_JSON="$2" # JSON-string (vb: '{"rules":[{"type":"min","edges":3,"sumdeg":5}]}')
shift 2          # verwijder de twee parameters, $@ bevat nu alle extra flags

# Genereer alle niet-isomorfe grafen van grootte ORDER (quiet mode)
# en pas daar de Python-filter "filter.py" op toe
# filtered_ouput = alles wat de filter uitprint
filtered_output=$(geng -q "$ORDER" | python3 filter.py --filter "$FILTER_JSON")
filtered_output=$(geng -q "$ORDER" \
  | python3 filter.py --filter "$FILTER_JSON" "$@")

# checkt of filtered_output leeg is
if [ -z "$filtered_output" ]; then
  echo "Geen grafen voldeden aan de opgegeven filter."
  echo "Probeer de filtercriteria aan te passen of geef een ander aantal knopen."
  exit 0
fi

# Toon de gefilterde grafen in graph6-formaat
echo  # witregel
echo "Gefilterde grafen (graph6-format):"
echo "$filtered_output"  # graph6-graphs

# Tel en toon het aantal geslaagde grafen en de gebruikte filterinstellingen
count=$(echo "$filtered_output" | grep -c .)
echo
printf "==> %d grafen voldeden aan de filter: %s\n" "$count" "$FILTER_JSON"
