import sqlite3

# создаем функцию по созданию и подключению к бд 'my_wallet.db'
def create_db():
    conn = sqlite3.connect("my_wallet.db")
    cursor = conn.cursor()

# создаем таблицу с данными id, date, description, amount
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS my_wallet 
    (id INTEGER PRIMARY KEY,
    amount REAL,
    description TEXT,
    date DATE
    )
    """)

# сохраняем и зарывает соединение
    conn.commit()
    conn.close()

create_db()

# функция для написания sql-запросов в таблицу
def connection_bd(name, *args):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    cursor.execute(*args)

    conn.commit()
    conn.close()