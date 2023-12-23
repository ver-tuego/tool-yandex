import sqlite3 as sql
import secrets

con = sql.connect('data/users.db', check_same_thread=False)

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS accounts ( id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT, password TEXT, "
            "token TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS files ( file_id INTEGER PRIMARY KEY AUTOINCREMENT, folder_id INT, name TEXT, "
            "size TEXT,user_id INT, private INT)")
cur.execute("CREATE TABLE IF NOT EXISTS folders ( folder_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, "
            "user_id TEXT )")

con.commit()
cur.close()

def create_user(login, password):
    token = secrets.token_hex(16)

    cur = con.cursor()
    cur.execute('INSERT INTO accounts (login, password, token) VALUES (?, ?, ?)', (login, password, token,))
    con.commit()
    cur.close()
    return token

def get_account(login = '', id = '', token = '', password = '', get_user=False):
    cur = con.cursor()
    if get_user:
        cur.execute('SELECT * FROM accounts WHERE login = ? AND password = ?', (login, password, ))
    else:
        cur.execute('SELECT * FROM accounts WHERE (login = ?) or (id = ?) or (token = ?)', (login, id, token, ))
    result = cur.fetchone()
    con.commit()
    cur.close()

    return result

    #cur.execute("INSERT INTO users (login, password, token) VALUES ('example_user', 'example_password', 'example_token')")

def save_file(name, size, user_id, folder_id, private):
    cur = con.cursor()
    cur.execute("INSERT INTO files (name, size, user_id, folder_id, private) VALUES (?, ?, ?, ?, ?)", (name, size, user_id, folder_id, private,))
    con.commit()
    cur.close()

def get_file(file_id=None, file_name=None):
    cur = con.cursor()
    cur.execute("SELECT * FROM files WHERE (file_id = ?) or (name = ?)", (file_id, file_name))
    result = cur.fetchone()
    con.commit()
    cur.close()

    return result

def get_files_user(user_id):
    cur = con.cursor()
    cur.execute("SELECT * FROM files WHERE user_id = ?", (user_id,))
    result = cur.fetchall()
    print(result)

    con.commit()
    cur.close()

    return result

def delete_file(file_id):
    cur = con.cursor()
    cur.execute("DELETE FROM files WHERE file_id = ?", (file_id,))
    con.commit()
    cur.close()

    return

def get_unique_id(branch_name):
    cur = con.cursor()
    cur.execute("SELECT * FROM sqlite_sequence WHERE name = ?", (branch_name,))
    result = cur.fetchone()
    con.commit()
    cur.close()

    return result[1]
