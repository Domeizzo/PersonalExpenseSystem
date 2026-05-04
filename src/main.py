import os
import sqlite3
from datetime import datetime
from pathlib import Path

# Percorso del database
DB_LINK_PATH = Path(__file__).resolve().parents[1] / "sql" / "spese.db"

def inizializza_sessione_db():
    dblink = sqlite3.connect(DB_LINK_PATH)
    dblink.execute("PRAGMA foreign_keys = ON;")
    cursor = dblink.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS categorie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS spese (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_spesa TEXT NOT NULL,
            importo REAL NOT NULL CHECK (importo > 0),
            id_categoria INTEGER NOT NULL,
            descrizione TEXT,
            FOREIGN KEY (id_categoria) REFERENCES categorie(id)
        );
        CREATE TABLE IF NOT EXISTS budget (
            mese TEXT NOT NULL, 
            id_categoria INTEGER NOT NULL,
            importo_limite REAL NOT NULL CHECK (importo_limite > 0),
            PRIMARY KEY (mese, id_categoria),
            FOREIGN KEY (id_categoria) REFERENCES categorie(id)
        );
    """)
    dblink.commit()
    return dblink

def mostra_menu():
    print("\n" + "="*30)
    print("   SISTEMA SPESE PERSONALI   ")
    print("="*30)
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Imposta Budget Mensile")
    print("4. Visualizza Report Totale")
    print("5. Esci")
    return input("\n>>> Digita il numero dell'operazione: ").strip()

def modulo_gestisci_categorie(dblink):
    print("\n--- AGGIUNGI NUOVA CATEGORIA ---")
    nuova_cat = input("Nome categoria: ").strip()
    if not nuova_cat: return
    try:
        dblink.execute("INSERT INTO categorie (nome) VALUES (?)", (nuova_cat,))
        dblink.commit()
        print("Categoria aggiunta!")
    except sqlite3.IntegrityError: print("Errore: esiste già.")

def modulo_inserisci_spesa(dblink):
    print("\n--- REGISTRA SPESA ---")
    try:
        importo = float(input("Importo: "))
        data = input("Data (YYYY-MM-DD) o Invio per oggi: ")
        if not data: data = datetime.now().strftime("%Y-%m-%d")
        
        cursor = dblink.cursor()
        cursor.execute("SELECT id, nome FROM categorie")
        cats = cursor.fetchall()
        for c in cats: print(f"{c[0]}) {c[1]}")
        
        id_cat = int(input("Scegli ID categoria: "))
        dblink.execute("INSERT INTO spese (data_spesa, importo, id_categoria, descrizione) VALUES (?, ?, ?, ?)",
                       (data, importo, id_cat, input("Descrizione: ")))
        dblink.commit()
        print("Spesa registrata!")
    except: print("Errore nei dati.")

def modulo_budget(dblink):
    print("\n--- IMPOSTA BUDGET ---")
    try:
        mese = input("Mese (YYYY-MM): ")
        limite = float(input("Limite spesa: "))
        cursor = dblink.cursor()
        cursor.execute("SELECT id, nome FROM categorie")
        for c in cursor.fetchall(): print(f"{c[0]}) {c[1]}")
        id_cat = int(input("ID Categoria: "))
        dblink.execute("INSERT OR REPLACE INTO budget VALUES (?, ?, ?)", (mese, id_cat, limite))
        dblink.commit()
        print("Budget salvato!")
    except: print("Errore.")

def modulo_report(dblink):
    print("\n--- REPORT SPESE ---")
    cursor = dblink.cursor()
    cursor.execute("SELECT c.nome, SUM(s.importo) FROM categorie c JOIN spese s ON c.id = s.id_categoria GROUP BY c.nome")
    for r in cursor.fetchall(): print(f"{r[0]}: €{r[1]:.2f}")

def main():
    if not DB_LINK_PATH.parent.exists(): DB_LINK_PATH.parent.mkdir(parents=True)
    conn = inizializza_sessione_db()
    while True:
        scelta = mostra_menu()
        if scelta == "1": modulo_gestisci_categorie(conn)
        elif scelta == "2": modulo_inserisci_spesa(conn)
        elif scelta == "3": modulo_budget(conn)
        elif scelta == "4": modulo_report(conn)
        elif scelta == "5": break
    conn.close()

if __name__ == "__main__":
    main()