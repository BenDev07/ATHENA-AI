
import sqlite3

connexion = sqlite3.connect("mwalimu.db")

connexion.executescript("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reclamations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    agent_response TEXT,
    status VARCHAR(50) DEFAULT 'En attente',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

connexion.commit()
connexion.close()

print("Les tables ont été créées avec succès !")
