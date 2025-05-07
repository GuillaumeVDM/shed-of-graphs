<!-- README.md -->
# Shed of Graphs

## Beschrijving

Deze applicatie implementeert Stage 1 en Stage 2 van de opdracht “Shed of Graphs”:

- **Stage 1**: filteren van grafen in graph6-formaat op basis van gecombineerde regels (minimaal/maximaal/exact aantal edges ten opzichte van som van degrees).
- **Stage 2**: bijhouden en persistent opslaan van een historie (timestamp, aantal input/output grafen, gebruikte filter, 20 recentste gefilterte grafen) in een tekstbestand.

*Gebaseerd op de projectopdracht van KU Leuven*

## Vereisten

- Python 3.8+
- NetworkX (zie `requirements.txt`)

## Installatie

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Gebruik
```bash
git clone https://github.com/GuillaumeVDM/shed-of-graphs.git
cd shed-of-graphs
chmod +x runfilter.sh
./runfilter.sh 5 \'{"rules":[{"type":"min","edges":3,"sumdeg":5},{"type":"max","edges":5,"sumdeg":6}]}'
```

## Tests

```bash
cd ~/Desktop/iwProject
source projectvenv/bin/activate
pytest
```

## BackUp & Restore
```bash
chmod +x backup_history.sh
./backup_history.sh

chmod +x restore_history.sh
./restore_history.sh
-> Kies een nummer
```
