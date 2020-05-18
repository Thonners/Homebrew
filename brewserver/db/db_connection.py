from .db_credentials import db_host, db_username, db_password, db_database
import back.authentication as auth
import mysql.connector
from .sql_statements import GET_SALT, CREATE_NEW_USER, CREATE_NEW_BREW

class DatabaseConnection:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=db_host,
            user=db_username,
            passwd=db_password,
            database=db_database
        )
        self.cursor = self.mydb.cursor(prepared=True)
    
    def __enter__(self):
        """
            Returns the instance that will be used if instantiated with a 'with' clause. 
            This (i.e. with DatabaseConnection as dc:) is the preferred way to use this class as it ensures the connection is closed properly
        """
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
            Called when a 'with' statement ends, regardless of whether an exception has occurred.
            Performs the database closing 'clean up' to ensure the connection is properly terminated
        """
        if (self.mydb.is_connected()):
            self.cursor.close()
            self.mydb.close()

    def execute_statement(self, statement, args=None):
        """
            Executes the given SQL statement and returns a list of tuples for the response
        """
        # TODO: Make sure the connection is active - also could wrap in try/catch for syntax errors too
        # TODO: Make sure that the previous statements have been read to avoid: mysql.connector.errors.InternalError: Unread result found
        # If there are any arguements to be passed to the statement, make sure they're in a tuple, otherwise submit it without args
        if args:
            if type(args) is not tuple:
                args = (args,)
            self.cursor.execute(statement,args)
        else:
            self.cursor.execute(statement)
        # Get the response
        if self.cursor.description:
            # Make sure there is a description (e.g. inserting values returns 'NoneType' for description)
            column_names = [i[0] for i in self.cursor.description]
        else:
            column_names = []
        # Store each line of the response in a list
        response = [line for line in self.cursor]
        # Return the column names and the response
        return column_names, response

    def add_new_user(self, email, firstname, lastname, password_plain_text):
        salt, pw_hash = auth.get_new_user_credentials(password_plain_text)
        new_user_details = (firstname, lastname, email, pw_hash, salt)
        try:
            self.execute_statement(CREATE_NEW_USER, new_user_details)
            # Need to commit the query if successful
            self.mydb.commit()
            # Return True to indicate success
            return True
        except mysql.connector.errors.IntegrityError:
            # Duplicate entry for email
            return False

    def add_new_brew(self, email, brew_name, brew_description):
        # TODO: Work out how the user authentication will be handled. Assuming we will have knowledge of the user's brewer_id, that can be swapped for the email and the insert statement simplified
        brew_key = auth.get_new_brew_key()
        brew_details = (brew_key, brew_name, brew_description, email)
        try:
            self.execute_statement(CREATE_NEW_BREW, brew_details)
            # Need to commit the query if successful
            self.mydb.commit()
            # Return True to indicate success
            return True
        except mysql.connector.errors.IntegrityError:
            # Duplicate entry for brew key
            return False




    def authenticate_user(self, email, password):
        """
            Checks the given user's password and returns true if the passwords match. 
            False if they password is wrong or the user doesn't exist in the system.

            Note: User is identified using their email.
        """
        salt, stored_hash = self._get_stored_salt_and_hash(email)
        if salt is not None:
            return auth.authenticate_user(salt, password, stored_hash)
        else:
            return False

    def _get_stored_salt_and_hash(self, email):
        cols, response = self.execute_statement(GET_SALT, email)
        if len(response) == 1:
            i_salt = cols.index('password_salt')
            i_hash = cols.index('password_hash')
            # Get the 'bytes' value as it will be returned as a bytearray by mysql.connector
            salt = bytes(response[0][i_salt])
            stored_hash = bytes(response[0][i_hash])
            return salt, stored_hash
        else:
            # Email not matched, so return None to indicate as such
            return None, None