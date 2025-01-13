import sqlite3


def run_query(db, query, params=None):
    try:
        cursor = db.cursor()
        cursor.execute(query, params or [])
        rows = cursor.fetchall()
        return [
            dict(zip([column[0] for column in cursor.description], row)) for row in rows
        ]
    except sqlite3.Error as e:
        print(f"Error querying: {e}")
        raise


def run_insert(db, query, params=None):
    try:
        cursor = db.cursor()
        cursor.execute(query, params or [])
        db.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error running query {query} with params {params}: {e}")
        raise


def create_table(db, query, table_name):
    try:
        run_insert(db, query)
        print(f"Table {table_name} created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"Error creating table {table_name}: {e}")
