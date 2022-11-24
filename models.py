import psycopg2

from settings import DB_TABLE_NAME, DBI_URI


class Model:
    @staticmethod
    def select_time(message):
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''SELECT time
                                  FROM {DB_TABLE_NAME}
                                  WHERE user_id = %s
                               '''
        cursor.execute(sqlite_select_query, (message.chat.id,))
        time = cursor.fetchone()[0]
        conn.commit()
        return time

    @staticmethod
    def select_random_task():
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''SELECT *
                                  FROM {DB_TABLE_NAME}
                                  WHERE message IS NOT NULL
                                  ORDER BY RANDOM()
                                  LIMIT 1;
                               '''
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        conn.commit()
        return records

    @staticmethod
    def select_all(user_id):
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''SELECT *
                                  FROM {DB_TABLE_NAME}
                                  WHERE user_id = %s
                               '''
        cursor.execute(sqlite_select_query, (user_id,))
        records = cursor.fetchall()
        conn.commit()
        return records

    @staticmethod
    def select_empty_message(user_id, bot):
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''SELECT *
                                  FROM {DB_TABLE_NAME}
                                  WHERE user_id = %s AND message IS NULL
                               '''
        cursor.execute(sqlite_select_query, (user_id,))
        empty_msg = cursor.fetchall()
        conn.commit()
        return empty_msg

    @staticmethod
    def update_message(user_msg, user_id):
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        val = (user_msg, user_id)
        sqlite_select_query = f'''UPDATE {DB_TABLE_NAME}
                                  SET message = %s
                                  WHERE user_id = %s'
                                  AND message IS NULL'''
        cursor.execute(sqlite_select_query, val)
        conn.commit()

    @staticmethod
    def update_time(time, user_id):
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''UPDATE {DB_TABLE_NAME}
                                  SET time = %s
                                  WHERE user_id = %s'''
        cursor.execute(sqlite_select_query, (time, user_id))
        conn.commit()

    @staticmethod
    def update_utc(utc, user_id):
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''UPDATE {DB_TABLE_NAME}
                                  SET utc = %s
                                  WHERE user_id = %s'''
        cursor.execute(sqlite_select_query, (utc, user_id))
        conn.commit()

    @staticmethod
    def insert_all(val):
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''INSERT INTO {DB_TABLE_NAME}
                                     (user_id, "user_name",
                                     "user_surname", "username",
                                     "message", utc, time)
                                  VALUES (%s, %s, %s, %s, %s, %s, %s)
                               '''
        cursor.execute(sqlite_select_query, val)
        conn.commit()

    @staticmethod
    def insert_exclude_time(val):
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''INSERT INTO {DB_TABLE_NAME}
                                      (user_id, "user_name", "user_surname",
                                      "username", "message")
                                  VALUES
                                      (%s, %s, %s, %s, %s)'''
        cursor.execute(sqlite_select_query, val)
        conn.commit()

    @staticmethod
    def insert_exclude_time_message(
        user_id,
        user_name,
        user_surname,
        username
    ):
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''INSERT INTO {DB_TABLE_NAME}
                                      (user_id, "user_name",
                                      "user_surname", "username")
                                  VALUES'
                                      (%s, %s, %s, %s)
                                   '''
        cursor.execute(
            sqlite_select_query,
            (user_id, user_name, user_surname, username)
        )
        conn.commit()
