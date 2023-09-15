import sqlite3


class SQLiteDB:
    def __init__(self, db_name="Orders.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS added_shipping (
                    po_number TEXT PRIMARY KEY,
                    tracking_number TEXT
                )
            """
            )

    def insert_data(self, po_number, tracking_number):
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO added_shipping (po_number, tracking_number) VALUES (?, ?)",
                (po_number, tracking_number),
            )

    def get_all_po_numbers(self):
        with self.conn:
            cur = self.conn.execute("SELECT po_number FROM added_shipping")
            return [row[0] for row in cur.fetchall()]
