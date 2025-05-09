#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for PNG generation
import matplotlib.pyplot as plt
from flask import Flask, render_template, url_for, send_file, abort
import networkx as nx
from io import BytesIO

# Create Flask app
app = Flask(
    __name__,
    template_folder='templates'
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# history.txt is one level above webapp/
HISTORY_FILE = os.path.abspath(os.path.join(BASE_DIR, '..', 'history.txt'))


def read_graphs():
    """
    Read history.txt, extract all Graph6 strings (last field, comma-separated),
    and return the most recent 20.
    """
    graphs = []
    try:
        with open(HISTORY_FILE, 'r') as f:
            lines = [l.strip() for l in f if l.strip()]
    except Exception as e:
        app.logger.error(f"Error reading history file: {e}")
        return []

    for line in lines:
        parts = line.split('\t')
        last = parts[-1]
        for g in last.split(','):
            g = g.strip()
            if g:
                graphs.append(g)
    return graphs[-20:]

@app.route('/index')
def index():
    """
    Render the index page with the 20 most recent Graph6 strings.
    """
    graphs = read_graphs()
    return render_template('index.html', graphs=graphs)

@app.route('/graph/<int:idx>.png')
def graph_image(idx):
    """
    Generate and return a PNG image for the graph at position idx.
    """
    graphs = read_graphs()
    if idx < 0 or idx >= len(graphs):
        abort(404)
    g6 = graphs[idx]
    try:
        G = nx.from_graph6_bytes(g6.encode())
        buf = BytesIO()
        plt.figure(figsize=(4, 4))
        nx.draw(G, with_labels=False)
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        app.logger.error(f"Error generating image for graph '{g6}': {e}")
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)