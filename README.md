<!-- README.md -->
# Shed of Graphs

## Beschrijving

Dit is een tool voor graph6-grafen te filteren: je kunt grafen filteren op minimaal/maximaal/exact aantal randen en som van graden, waarbij automatisch een geschiedenislog wordt bijgehouden (inclusief uur-backups). De code bevat unit-tests met pytest en een CI-workflow, en er is een bash-script voor parallelle filtering. Gefilterde grafen exporteer je als PNG/SVG, je kunt ze realtime bekijken via een basic Flask-webinterface en de hele webserver draait in een Docker-container.

## Vereisten

- zie requirements.txt

## Installatie
Kopieer de shed-of-graphs.git
```bash
git clone https://github.com/GuillaumeVDM/shed-of-graphs.git
cd shed-of-graphs
```
Maak een virtual environment aan met de nodige requirements
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Gebruik
```bash
chmod +x runfilter.sh
./runfilter.sh 5 '{"rules":[{"type":"min","edges":3,"sumdeg":5},{"type":"max","edges":5,"sumdeg":6}]}'
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
```
Kies voor te restoren een index van de history_backup

## Web Server
```bash
python webapp/app.py
http://localhost:5000/index
```

## Docker-setup
Image bouwen
```bash
docker build -t graph-webapp .
```
Container starten
```bash
docker run -d \
  --name graph-webapp \
  -p 5000:5000 \
  -v "$(pwd)/history.txt:/app/history.txt:ro" \
  graph-webapp
```
Webapplicatie openen
```bash
http://localhost:5000/index
```
Container stoppen en verwijderen
```bash
docker stop graph-webapp
docker rm   graph-webapp
```
