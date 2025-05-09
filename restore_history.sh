#!/usr/bin/env bash
"""
    Het restore_history.sh-script zoekt in de map filtered-graphs/ 
    naar alle bestanden history-*.txt, toont die als een genummerd keuzemenu, 
    en wacht op jouw invoer (het nummer van de gewenste backup). Zodra je kiest, 
    kopieert het de geselecteerde backup over history.txt, 
    waardoor je de geschiedenis nauwkeurig terugzet naar dat tijdstip
"""

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/filtered-graphs"
HISTORY_FILE="history.txt"

# Maak een array van alle history-*.txt bestanden in $BACKUP_DIR
backups=( "$BACKUP_DIR"/history-*.txt )

# Als er geen enkel bestand matched, dan bestaat ${backups[0]} als literal pad
if [ ! -e "${backups[0]}" ]; then
  echo "Geen backups gevonden in $BACKUP_DIR"
  exit 1
fi

echo "Kies een backup om te herstellen:"
select f in "${backups[@]}"; do # Elke backup krijgt een nummer; je typt het nummer om je keuze te maken.
  [ -n "$f" ] && cp "$f" "$HISTORY_FILE" && \
    echo "Hersteld $HISTORY_FILE vanuit $(basename "$f")" && exit 0
  echo "Ongeldige keuze, probeer opnieuw."
done
