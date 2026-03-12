import sqlite3


def init_db():
    conn = sqlite3.connect('experiments.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner TEXT NOT NULL,
            primary_metric TEXT NOT NULL,
            traffic_split REAL NOT NULL,
            sample_size INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            status TEXT DEFAULT 'draft'
        )
    ''')
    
    conn.commit()
    conn.close()


def create_experiment(name, owner, primary_metric, traffic_split, sample_size, start_date):
    init_db()
    conn = sqlite3.connect('experiments.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO experiments (name, owner, primary_metric, traffic_split, sample_size, start_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, owner, primary_metric, traffic_split, sample_size, start_date))
    
    experiment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return experiment_id


def _row_to_dict(result):
    return {
        'id': result[0],
        'name': result[1],
        'owner': result[2],
        'primary_metric': result[3],
        'traffic_split': result[4],
        'sample_size': result[5],
        'start_date': result[6],
        'status': result[7]
    }


def get_experiment(experiment_id):
    init_db()
    conn = sqlite3.connect('experiments.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM experiments WHERE id = ?', (experiment_id,))
    result = cursor.fetchone()
    conn.close()
    
    return _row_to_dict(result) if result else None


def list_experiments():
    init_db()
    conn = sqlite3.connect('experiments.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM experiments ORDER BY id DESC')
    results = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(result) for result in results]