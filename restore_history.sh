#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then # controleren of aantal argumenten minder dan 3 is
  echo "Usage: $0 <graph-order> '<JSON_FILTER>' <threads> [output_prefix]" # korte gebruiksaanwijzing
  exit 1
fi

ORDER="$1"
FILTER_JSON="$2"
THREADS="$3"  # hoeveel parallelle batches (threads)  (vb: 4 results)
PREFIX="${4:-filtered}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)" # Bepaalt de map waarin dit script staat, ongeacht vanuit welke directory je het aanroept

# Directory voor output
OUTDIR="$SCRIPT_DIR/${PREFIX}-threads"
mkdir -p "$OUTDIR"


# Als order buiten 8–64 valt, gebruik geng in één thread
#  Plantri ondersteunt alleen orders in de range 8–64, 
#  dus we vangen hier alle andere gevallen af.
if [ "$ORDER" -lt 8 ] || [ "$ORDER" -gt 64 ]; then
  echo "Order $ORDER outside Plantri’s 8–64 range, falling back to geng."
  geng -q "$ORDER" | python3 filter.py --filter "$FILTER_JSON" \
    > "$OUTDIR/${PREFIX}_thread0.g6"
  exit 0
fi

# Anders: parallel via Plantri res/mod-splitting
for ((i=0; i<THREADS; i++)); do
  (
    echo "[Thread $i] plantri -g $ORDER $i/$THREADS → filtering…"
    plantri -g "$ORDER" "$i/$THREADS" \
        | python3 filter.py --filter "$FILTER_JSON" \
        > "$OUTDIR/${PREFIX}_thread${i}.g6"


    echo "[Thread $i] klaar, output → ${PREFIX}_thread${i}.g6"
  ) &
done


echo "Wacht op alle $THREADS jobs…"
wait    # pauzeert het hoofdscript totdat álle achtergrondprocessen (threads) gereed zijn
echo "Klaar! Kijk in $OUTDIR voor de resultaten."
