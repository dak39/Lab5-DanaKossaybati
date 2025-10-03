#!/usr/bin/python
import sqlite3

DB_PATH = 'database.db'

def connect_to_db():
    return sqlite3.connect(DB_PATH)

def create_db_table():
    conn = connect_to_db()
    try:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name    TEXT NOT NULL,
            email   TEXT NOT NULL,
            phone   TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        );
        """)
        conn.commit()
        print("User table created successfully")
    except Exception as e:
        print(f"User table creation failed: {e}")
    finally:
        conn.close()

def insert_user(user):
    inserted_user = {}
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            (user['name'], user['email'], user['phone'], user['address'], user['country'])
        )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        conn.rollback()
        print(f"Insert failed: {e}")
    finally:
        conn.close()
    return inserted_user

def get_users():
    users = []
    conn = connect_to_db()
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        users = [dict(row) for row in rows]
    except Exception as e:
        print(f"Fetch failed: {e}")
    finally:
        conn.close()
    return users

def get_user_by_id(user_id):
    user = {}
    conn = connect_to_db()
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            user = dict(row)
    except Exception as e:
        print(f"Fetch by id failed: {e}")
    finally:
        conn.close()
    return user

def update_user(user):
    updated_user = {}
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ?
            WHERE user_id = ?
        """, (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"]))
        conn.commit()
        updated_user = get_user_by_id(user["user_id"])
    except Exception as e:
        conn.rollback()
        print(f"Update failed: {e}")
    finally:
        conn.close()
    return updated_user

def delete_user(user_id):
    message = {}
    conn = connect_to_db()
    try:
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception as e:
        conn.rollback()
        print(f"Delete failed: {e}")
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message

if __name__ == "__main__":
    create_db_table()
