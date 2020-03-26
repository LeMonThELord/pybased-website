import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise


# Encrypt the passwords
def encrypt(username, password):
    new_password = str([chr(ord(i) * len(username))
                        for i in password]).strip("\]").strip("\[").replace(", ", "").replace("\'", "")
    # print(new_password)
    return new_password


class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg=":memory:"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()
        self.size = 0

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    # -----------------------------------------------------------------------------

    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            Id INT,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0
        )""")

        self.commit()

        # Add our admin user
        self.add_user('admin', admin_password, admin=1)
        self.add_user("user", "user")
        self.add_user("user_space", "user password")

    # -----------------------------------------------------------------------------
    # User handling
    # -----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, admin=0):
        password = encrypt(username, password)

        sql_cmd = """
                INSERT INTO Users
                VALUES({id}, '{username}', '{password}', {admin})
            """

        sql_cmd = sql_cmd.format(id=self.size,
                                 username=username, password=password, admin=admin)

        self.size += 1

        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        password = encrypt(username, password)

        sql_query = """
                        SELECT admin
                        FROM Users
                        WHERE username = '{username}' AND password = '{password}'
                    """

        sql_query = sql_query.format(username=username, password=password)

        self.execute(sql_query)

        result = self.cur.fetchone()

        # If our query returns
        if result:
            return result[0]
        else:
            return None


# database = SQLDatabase("/users.db")
# database.database_setup()
# database.add_user("user", "user")
# database.add_user("user_space", "user password")
# print(database.check_credentials("admin", "admin"))
# print(database.check_credentials("admin", "password"))
# print(database.check_credentials("user", "user"))
# print(database.check_credentials("user", "password"))
# print(database.check_credentials("user_space", "user password"))
# print(database.check_credentials("user_space", "user_password"))
