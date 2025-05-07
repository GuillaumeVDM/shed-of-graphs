#!/usr/bin/env bash
#
# backup_history.sh
# Maak een timestamped backup van history.txt in ~/.filtered-graphs

#!/usr/bin/env bash
set -euo pipefail

HISTORY_FILE="history.txt"
# berekent het absolute pad naar de submap filtered-graphs binnen jouw projectmap
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/filtered-graphs"

mkdir -p "$BACKUP_DIR"   # zorgt dat deze map "filtered-graphs" er altijd is
timestamp=$(date +'%Y%m%d-%H%M%S') # maakt een string van de huidige datum en tijd
cp "$HISTORY_FILE" "$BACKUP_DIR/history-$timestamp.txt" # Kopiëren van history.txt

