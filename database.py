
import sqlite3

def init_db():
    conn = sqlite3.connect("kaya.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS chats(role TEXT, user TEXT, reply TEXT)")
    conn.commit()
    conn.close()

def log_chat(role, user, reply):
    conn = sqlite3.connect("kaya.db")
    c = conn.cursor()
    c.execute("INSERT INTO chats VALUES(?,?,?)", (role, user, reply))
    conn.commit()
    conn.close()
