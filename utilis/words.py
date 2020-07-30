from typing import List, Tuple, Union
import sqlite3
import random

"""module of <app.py>"""

Records = Tuple[str, str]


class DatabaseConnection:
    """connect, create cursor, commit and close "database.db" file"""

    def __init__(self, host: str):
        self.connection = None
        self.host = host

    def __repr__(self) -> str:
        return f"<DatabaseConnection connection: {self.connection}, host: {self.host}>"

    def __enter__(self) -> sqlite3.Connection.cursor:
        self.connection = sqlite3.connect(self.host)
        cursor = self.connection.cursor()
        return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()


class Words:
    """framework for main application <app.py>. Includes all necessary properties and methods to run program"""
    def __init__(self, category: str):
        self._category = category
        self.score = 0
        self._table_from_db = None
        self._record_from_database = None

    def __repr__(self) -> str:
        return f"<Words category: {self._category}, score: {self.score}, table: {self._table_from_db}, " \
               f"record: {self._record_from_database}>"

    def _pull_table_from_database(self) -> Union[List[Records], None]:
        """
        pull table from database and shuffle records within or return empty table
        """
        with DatabaseConnection("database.db") as cursor:
            cursor.execute(f"SELECT * FROM {self._category}")
            if self._table_from_db is None:  # if table is empty
                self._table_from_db = list(cursor.fetchall())
                random.shuffle(self._table_from_db)
                return self._table_from_db
            else:
                return self._table_from_db

    def _get_random_record_from_table(self):
        """
        get last record from table only if table is not empty
        """
        self._table_from_db = self._pull_table_from_database()
        return self._table_from_db.pop()

    def ask_user_to_translate(self) -> str:
        """
        ask user to translate polish word into english word
        """
        try:
            self._record_from_database = self._get_random_record_from_table()
            return self._record_from_database[1]  # polish_word
        except IndexError:
            if self.score == 0:
                print("\nTable is empty so far...\n")
            else:
                print(f"Congratulation !!! You've translated all words in table. Your total score is: {self.score}\n")

    def _calculate_points(self, boolean_value: bool):
        """
        calculate points gain or lost by user
        overwrite "self.score" in __init__
        """
        if boolean_value:
            self.score += 5
        else:
            self.score -= 5

    @staticmethod
    def clear_table_wrong_answers():
        """
        clear all table which including incorrect translate of words by user
        """
        with DatabaseConnection("database.db") as cursor:
            cursor.execute("DELETE FROM incorrect_translate")
            print("\nTable has been clear\n")

    @staticmethod
    def add_record_into_incorrect_translate_table(eng_word: str, pol_word: str, table="incorrect_translate"):
        """
        add record (eng_word, pol_word) into table <incorrect_translate> including wrong user"s answer in database
        whenever user doesn't provide the correct translate of word. If record already exist in table than just
        skip it
        """
        with DatabaseConnection("database.db") as cursor:
            try:
                cursor.execute(f"INSERT INTO {table} VALUES(?, ?)", (eng_word, pol_word))
            except sqlite3.IntegrityError:  # if value already exist than skip it
                pass

    def check_translate_is_correct(self, user_answer: str) -> str:
        """
        check whether user translate is correct or not. If translate is not correct than insert record again to
        actual table for reuse by program
        """
        if user_answer == self._record_from_database[0]:  # english word
            self._calculate_points(True)
            return f"\nCorrect translate! You got 5 points"
        else:
            self._calculate_points(False)
            self._table_from_db.insert(0, self._record_from_database)
            eng_word = self._record_from_database[0]
            pol_word = self._record_from_database[1]
            self.add_record_into_incorrect_translate_table(eng_word, pol_word)
            return f"\nIncorrect translate! You lost 5 points\n" \
                   f"The correct translate should look like this '{eng_word}'"

