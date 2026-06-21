"""Esempio di codice da audire — contiene pattern realistici con criticità intenzionali.

Usato per testare la modalità `tavolarotonda --audit`:
    python -m tavolarotonda --audit examples/audit_target.py --mock --output report.html
"""

from __future__ import annotations

import hashlib
import os
import pickle
import subprocess
import sys


# ❌ CRITICITÀ: password in chiaro nel codice
DATABASE_PASSWORD = "admin123"
API_SECRET = "sk-1234567890abcdef"

# ❌ CRITICITÀ: SQL injection vulnerability
def get_user(username):
    """Get user by username — INSECURE!"""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()


# ❌ CRITICITÀ: shell injection
def convert_file(input_path):
    subprocess.call(f"convert {input_path} output.png", shell=True)


# ❌ CRITICITÀ: pickle deserialization
def load_session(data):
    return pickle.loads(data)


# ⚠️ WARNING: MD5 per password
def hash_password(pw):
    return hashlib.md5(pw.encode()).hexdigest()


# ✅ PRO: type hints + docstring
def calculate_discount(price: float, percentage: float) -> float:
    """Calcola il prezzo scontato.
    
    Args:
        price: prezzo originale
        percentage: sconto in percentuale (0-100)
    
    Returns:
        prezzo scontato
    """
    if not 0 <= percentage <= 100:
        raise ValueError("percentage deve essere tra 0 e 100")
    return price * (1 - percentage / 100)


# ⚠️ WARNING: gestione errori assente
def parse_config(path):
    """Carica config da file JSON — manca gestione errori."""
    with open(path) as f:
        return json.load(f)


# ❌ CRITICITÀ: path traversal
def read_file(filename):
    base = "/var/data/"
    full = os.path.join(base, filename)
    with open(full) as f:
        return f.read()


# ❌ CRITICITÀ: eval su input utente
def calc(expression):
    return eval(expression)


# ✅ PRO: context manager + chiusura file garantita
def write_log(message: str, log_path: str = "/tmp/app.log") -> None:
    """Scrive un messaggio nel log con timestamp."""
    from datetime import datetime
    with open(log_path, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")


def get_db_connection():
    """Connessione DB (placeholder)."""
    import sqlite3
    return sqlite3.connect(":memory:")


if __name__ == "__main__":
    print("Questo è un file di esempio per audit, non eseguirlo.")
    sys.exit(1)
