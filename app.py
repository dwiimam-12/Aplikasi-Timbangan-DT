
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)

DB_NAME = 'penimbangan.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS penimbangan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tanggal TEXT,
                    kapal TEXT,
                    plat TEXT,
                    tonase REAL,
                    shift TEXT,
                    gudang TEXT,
                    jam TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        kapal = request.form['kapal']
        plat = request.form['plat']
        tonase = float(request.form['tonase'])
        shift = request.form['shift']
        gudang = request.form['gudang']
        tanggal = datetime.now().strftime('%Y-%m-%d')
        jam = datetime.now().strftime('%H:%M:%S')

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO penimbangan (tanggal, kapal, plat, tonase, shift, gudang, jam) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (tanggal, kapal, plat, tonase, shift, gudang, jam))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM penimbangan", conn)
    summary = df.groupby(['tanggal', 'shift', 'gudang'])['tonase'].sum().reset_index()
    conn.close()
    return render_template('index.html', data=df.to_dict(orient='records'), summary=summary.to_dict(orient='records'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
