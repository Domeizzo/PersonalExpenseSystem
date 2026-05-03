-- ==========================================================
-- SCRIPT DI CREAZIONE DATABASE "SISTEMA SPESE PERSONALI"
-- Rispetta i requisiti di integrità del bando (Punto 8.1)
-- ==========================================================

-- Abilita il controllo delle chiavi esterne (specifico per SQLite)
PRAGMA foreign_keys = ON;

-- 1. TABELLA CATEGORIE
-- Memorizza le tipologie di spesa. Il nome è UNICO per evitare doppioni.
CREATE TABLE categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

-- 2. TABELLA SPESE
-- Registro delle singole operazioni. 
-- Include un CHECK per impedire importi negativi o zero.
CREATE TABLE spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_spesa TEXT NOT NULL,
    importo REAL NOT NULL CHECK (importo > 0),
    id_categoria INTEGER NOT NULL,
    descrizione TEXT,
    -- Vincolo di integrità referenziale: collega la spesa a una categoria valida
    FOREIGN KEY (id_categoria) REFERENCES categorie(id)
);

-- 3. TABELLA BUDGET
-- Definisce il limite di spesa mensile per ogni categoria.
-- Utilizza una CHIAVE PRIMARIA COMPOSTA (mese + id_categoria).
CREATE TABLE budget (
    mese TEXT NOT NULL, -- Formato YYYY-MM
    id_categoria INTEGER NOT NULL,
    importo_limite REAL NOT NULL CHECK (importo_limite > 0),
    PRIMARY KEY (mese, id_categoria),
    FOREIGN KEY (id_categoria) REFERENCES categorie(id)
);