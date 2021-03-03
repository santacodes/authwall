"""AuthWall Backend."""
from hash_pass import hash_password, check_hash
import mysql.connector
from mysql.connector import connect
import sys


class AuthWall():
    """AuthWall Backend."""

    def __init__(self, host='localhost', database='login',
                 user='SuperUser', password='Rocky123'):
        """Connect to SQL Database."""
        try:
            self.db = connect(host=host, database=database,
                              user=user, password=password)
        except mysql.connector.errors.ProgrammingError as e:
            if str(e) != f"1045 (28000): Access denied for user '{user}'@'{host}' (using password: YES)":
                raise e
        try:
            if self.db.is_connected():
                self.cursor = self.db.cursor()
        except mysql.connector.errors as e:
            raise e

    def _get_hash(self, user):
        self.cursor.execute(f"select hashcode from info where user='{user}'")
        return self.cursor.fetchone()[0]

    def authenticate(self, user, password):
        """Authenticate User."""
        return True if check_hash(self._get_hash(user), password) else False

    def authenticate_seq(self, user, sq, index):
        """Authenticate Security Question & Index."""
        self.cursor.execute(f"select sq, sq_index from info where user='{user}'")
        data = self.cursor.fetchone()
        if check_hash(data[0], sq) and check_hash(data[1], index):
            return True
        return False

    def change_hash(self, user, password):
        """Change Password."""
        if check_hash(self._get_hash(user), password):
            return False
        self.cursor.execute(
            f"UPDATE info set hashcode='{hash_password(password)}' WHERE user='{user}'")
        self.db.commit()
        return True

    def delete(self, user):
        """Delete User."""
        self.cursor.execute(f"DELETE FROM info WHERE user='{user}'")
        self.db.commit()

    def check_existance(self, user):
        """Check if User Exists."""
        self.cursor.execute(f"SELECT * FROM info where user='{user}'")
        return True if self.cursor.fetchall() else False

    def add(self, user, password, sq, sq_index):
        """Add User."""
        self.cursor.execute(
            f"INSERT INTO info VALUES ('{user}', '{hash_password(password)}', '{hash_password(sq)}', '{hash_password(sq_index)}')")
        self.db.commit()
