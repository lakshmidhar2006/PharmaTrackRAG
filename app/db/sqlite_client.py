import sqlite3
from pathlib import Path
from app.config import settings


DB_PATH = Path(settings.sqlite_db)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_conn():
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
return conn


# Initialize tables on import if missing
with get_conn() as conn:
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS documents (
document_id TEXT PRIMARY KEY,
filename TEXT,
path TEXT,
metadata TEXT,
uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
status TEXT
)
''')


cur.execute('''
CREATE TABLE IF NOT EXISTS chunks (
chunk_id TEXT PRIMARY KEY,
document_id TEXT,
text TEXT,
start_offset INTEGER,
end_offset INTEGER,
embedding_index INTEGER,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(document_id) REFERENCES documents(document_id)
)
''')
conn.commit()