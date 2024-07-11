import sqlite3
import json

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id, username, refferal_id=None):
        with self.connection:
            if refferal_id is not None:
                self.cursor.execute("INSERT INTO users (user_id, refferer_id, username) VALUES (?, ?, ?)", (user_id, refferal_id, username))
            else:
                self.cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        self.connection.commit()

    def set_active(self, user_id, active):
        with self.connection:
            self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id,))
        self.connection.commit()

    def get_data_users(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users").fetchall()

    def set_money(self, user_id, money):
        with self.connection:
            self.cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (money, user_id,))
        self.connection.commit()

    def set_ref_user(self, user_id, option):
        with self.connection:
            self.cursor.execute("UPDATE users SET refferals = ? WHERE user_id = ?", (option, user_id,))
        self.connection.commit()

    def set_user_lang(self, user_id, lang):
        with self.connection:
            self.cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
            
    def get_user_rank_by_balance(self, user_id):
        with self.connection:
            query = """
            SELECT user_id, 
                RANK() OVER (ORDER BY balance DESC) as rank
            FROM users
            """
            results = self.cursor.execute(query).fetchall()
            user_rank = next((rank for uid, rank in results if uid == user_id), None)
            return user_rank
    def get_top_10_users(self):
        with self.connection:
            query = """
            SELECT username, balance
            FROM users
            ORDER BY balance DESC
            LIMIT 10
            """
            top_users = self.cursor.execute(query).fetchall()
            return top_users

    