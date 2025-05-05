#database
import os
import sqlite3
from pathlib import Path

# Adicione no início do arquivo
BASE_DIR = Path(__file__).parent
DB_PATH = os.path.join(BASE_DIR, 'furia_fans.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        # Habilita WAL mode
        conn.execute('PRAGMA journal_mode=WAL')
        
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            birthdate TEXT,
            cep TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            games TEXT,
            favorite_team TEXT,
            nick_name TEXT,
            events_attended TEXT,
            merch_purchases TEXT,
            twitter_profile TEXT,
            instagram_profile TEXT,
            esports_profiles TEXT,
            id_document_path TEXT,
            proof_of_address_path TEXT,
            registration_date TEXT DEFAULT CURRENT_TIMESTAMP,
            ai_insights TEXT
        )
        ''')
        conn.commit()


def save_user_data(user_data):
    with get_db_connection() as conn:
        # Converter lista de jogos para JSON
        games_json = str(user_data['interests']['games'])
        
        conn.execute('''
        INSERT INTO users (
            name, cpf, email, birthdate, cep, address, city, state,
            games, favorite_team, nick_name, events_attended, merch_purchases,
            twitter_profile, instagram_profile, esports_profiles,
            id_document_path, proof_of_address_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['personal_info']['name'],
            user_data['personal_info']['cpf'],
            user_data['personal_info']['email'],
            user_data['personal_info']['birthdate'],
            user_data['address']['cep'],
            user_data['address']['address'],
            user_data['address']['city'],
            user_data['address']['state'],
            games_json,
            user_data['interests']['favorite_team'],
            user_data['interests']['nick_name'],
            user_data['interests']['events_attended'],
            user_data['interests']['merch_purchases'],
            user_data['social_media']['twitter_profile'],
            user_data['social_media']['instagram_profile'],
            user_data['social_media']['esports_profiles'],
            user_data['documents'].get('id_document'),
            user_data['documents'].get('proof_of_address')
        ))
        conn.commit()


# Inicializa o banco de dados quando o módulo é importado
init_db()