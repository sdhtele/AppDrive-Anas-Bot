from os import path as ospath, makedirs
from psycopg2 import connect, DatabaseError

from bot import DB_URI, AUTHORIZED_CHATS, SUDO_USERS, AS_DOC_USERS, AS_MEDIA_USERS, rss_dict, LOGGER

class DbManger:
    """
    Database Manager class to handle all database-related operations.
    """

    def __init__(self):
        """
        Initialize the DbManger class with an error flag set to False.
        """
        self.err = False
        self.connect()

    def connect(self):
        """
        Connect to the database and set up a connection and cursor.
        Log any database errors and set the error flag to True if an error occurs.
        """
        try:
            self.conn = connect(DB_URI)
            self.cur = self.conn.cursor()
        except DatabaseError as error:
            LOGGER.error(f"Error in DB connection: {error}")
            self.err = True

    def disconnect(self):
        """
        Close the cursor and connection to the database.
        """
        self.cur.close()
        self.conn.close()

    def db_init(self):
        """
        Initialize the database by creating users and rss tables if they don't already exist.
        Commit any changes and log a message indicating the database has been initiated.
        Import user and rss data from the database and log messages indicating the data has been imported.
        Disconnect from the database.
        """
        if self.err:
            return
        sql = """CREATE TABLE IF NOT EXISTS users (
                 uid bigint,
                 sudo boolean DEFAULT FALSE,
                 auth boolean DEFAULT FALSE,
                 media boolean DEFAULT FALSE,
                 doc boolean DEFAULT FALSE,
                 thumb bytea DEFAULT NULL
              )
              """
        self.cur.execute(sql)
        sql = """CREATE TABLE IF NOT EXISTS rss (
                 name text,
                 link text,
                 last text,
                 title text,
                 filters text
              )
              """
        self.cur.execute(sql)
        self.conn.commit()
        LOGGER.info("Database Initiated")
        self.db_load()

    def db_load(self):
        # User Data
        self.cur.execute("SELECT * from users")
        rows = self.cur.fetchall()  #returns a list ==> (uid, sudo, auth, media, doc, thumb)
        if rows:
            for row in rows:
                if row[1] and row[0] not in SUDO_USERS:
                    SUDO_USERS.add(row[0])
                elif row[2] and row[0] not in AUTHORIZED_CHATS:
                    AUTHORIZED_CHATS.add(row[0])
                if row[3]:
                    AS_MEDIA_USERS.add(row[0])
                elif row[4]:
                    AS_DOC_USERS.add(row[0])
                path = f"Thumbnails/{row[0]}.jpg"
                if row[5] is not None and not ospath.exists(path):
                    if not ospath.exists('Thumbnails'):
                        makedirs('Thumbnails')
                    with open(path, 'wb+') as f:
                        f.write(row[5])
                        f.close()
            LOGGER.info("Users data has been imported from Database")
        # Rss Data
        self.cur.execute("SELECT * FROM rss")
        rows = self.cur.fetchall()  #returns a list ==> (name, feed_link, last_link, last_title, filters)
        if rows:
            for row in rows:
                f_lists = []
                if row[4] is not None:
                    filters_list = row[4].split('|')
                    for x in filters_list:
                        y = x.split(' or ')
                        f_lists.append(y)
                rss_dict[row[0]] = [row[1], row[2], row[3], f_lists]
            LOGGER.info("Rss data has been imported from Database.")
        self.disconnect()

    def user_auth(self, chat_id: int):
        """
        Authorize a user by updating the auth field in the users table to True or inserting a new user with auth set to True.
        Commit any changes and disconnect from the database.
        Return a success message.
        """
        if self.err:
            return "Error in DB connection, check log for details"
        elif not self.user_check(chat_id):
            sql = 'INSERT INTO users (uid, auth) VALUES ({}, TRUE)'.format(chat_id)
        else:
            sql = 'UPDATE users SET auth = TRUE WHERE uid = {}'.format(chat_id)
        self.cur.execute(sql)
        self.conn.commit()
        self.disconnect()
        return 'Authorized successfully'

    def user_unauth(self, chat_id: int):
        """
        Unauthorize a user by updating the auth field in the users table to False if the user exists.
        Commit any changes and disconnect from the database.
        Return a success message.
        """
        if self.err:
            return "Error in DB connection, check log for details"
        elif self.user_check(chat_id):
            sql = 'UPDATE users SET auth = FALSE WHERE uid = {}'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            return 'Unauthorized successfully'

    def user_addsudo(self, user_id: int):
        """
        Promote a user to sudo by updating the sudo field in the users table to True or inserting a new user with sudo set to True.
        Commit any changes and disconnect from the database.
        Return a success message.
        """
        if self.err:
            return "Error in DB connection, check log for details"
        elif not
