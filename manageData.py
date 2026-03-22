from sqlite3 import *

from utils import encrypt, decrypt


def creating_tables() -> None:
    """
        Creates table Login for storing users username and password and table Credentials for storing users credentials fot other sites.

    """
    with connect("data.db") as manager:
        cursor = manager.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS login (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (
            num INTEGER PRIMARY KEY AUTOINCREMENT,
            id INTEGER,
            site VARCHAR(255),
            username VARCHAR(255),
            password VARCHAR(255)
        )''')

def set_up_account(username: str, password: bytes) -> None:
    """
        Adds users username and hashed password to the login table.

        Args:
            username (str): Plain text username
            password (str): Hashed password
    """
    with connect("data.db") as manager:
        cursor = manager.cursor()
        cursor.execute('''INSERT INTO login (username, password) 
            VALUES (?, ?)''', (username, password))

def username_exists(username: str) -> bool:
    """
        Checking login table whether username exists there.

        Args:
            username (str): Plain text username
        Returns:
            bool: True if username exists False otherwise
    """
    with connect("data.db") as manager:
        cursor = manager.cursor()

        cursor.execute("SELECT * FROM login WHERE username = ?", (username,))
        result = cursor.fetchone()

    if result:
        return True
    else:
        return False

def retrieve_password(username: str) -> bytes:
    """
        Retrieving users hashed password.

        Args:
            username (str): Plain text username
        Returns:
            bytes: Users Hashed password
    """
    with connect("data.db") as manager:
        cursor = manager.cursor()
        cursor.execute("SELECT password FROM login WHERE username = ?", (username,))
        result = cursor.fetchone()

    hashed = result[0]
    return hashed

def get_user_id(username: str) -> str:
    """
        Finding users ID based on username.

        Args:
            username (str): Plain text username
        Returns:
            str: Users ID
    """
    with connect("data.db") as manager:
        cursor = manager.cursor()

        cursor.execute("SELECT id FROM login WHERE username = ?", (username,))
        result = cursor.fetchone()

    return result[0]

def insert_credential(id_num: int, site: str, username: str, password: str, key: bytes) -> None:
    """
        Adds users credentials: ID number, site, username and encrypted password to the credentials table.

        Args:
            id_num (int): ID of user
            site (str): Name of Site
            username (str): Username for the site
            password (str): Plain text password
            key (bytes): Fernet encryption key
    """

    encrypt_password = encrypt(password, key)
    with connect("data.db") as manager:
        cursor = manager.cursor()

        cursor.execute('''INSERT INTO credentials (id, site, username, password) 
            VALUES (?, ?, ?, ?)''', (id_num, site, username, encrypt_password))

def retrieve_credentials(id_num: int) -> list:
    """
        Retrieves users site and the respective username in a dictionary where the key is the site and the usernames are the values.

        Args:
            id_num (str): users ID
        Returns:
            list: dictionary list of credentials
    """
    with connect("data.db") as manager:
        cursor = manager.cursor()

        cursor.execute("SELECT site, username FROM credentials WHERE id = ?", (id_num,))
        rows = cursor.fetchall()

    site_dict = {}
    for site, username in rows:
        if site not in site_dict:
            site_dict[site] = [site]  # First value is the site name
        site_dict[site].append(username)

    return list(site_dict.values())

def get_password(id_num: int, username: str, site: str, key: bytes) -> str:
    """
        Retrieves users decrypted password from the credentials table.

        Args:
            id_num (int): ID of user
            username (str): Plain text username
            site (str): Name of Site
            key (bytes): Fernet encryption key
        Returns:
            bytes: Plain text password
    """
    with connect("data.db") as manager:
        cursor = manager.cursor()

        cursor.execute("SELECT password FROM credentials WHERE id = ? AND username = ? AND site = ?", (id_num, username, site))
        result = cursor.fetchone()

    password = decrypt(result[0], key)

    return password

def deleted_credential(id_num: int, username: str, site: str) -> None:
    """
        Deleting the specified record for the user.

        Args:
            id_num (int): ID of user
            username (str): Plain text username
            site (str): Name of Site
    """
    with connect("data.db") as manager:
        cursor = manager.cursor()

        cursor.execute("DELETE FROM credentials WHERE id = ? AND username = ? AND site = ?", (id_num, username, site))

def update_credential(id_num: int, old_username: str, old_site: str, new_site: str, new_username: str, new_password: str, key: bytes) -> None:
    """
        Updating the specified record for the user.

        Args:
            id_num (int): ID of user
            old_username (str): Plain text old username
            old_site (str): Name of old Site
            new_site (str): Name of new Site
            new_username (str): Plain text new username
            new_password (str): Plain text new password
            key (bytes): Fernet encryption key
    """

    new_password = encrypt(new_password, key)

    with connect("data.db") as manager:
        cursor = manager.cursor()

        cursor.execute('''UPDATE credentials 
                       SET site = ?, username = ?, password = ?
                       WHERE id = ? AND username = ? AND site = ?''',
                       (new_site, new_username, new_password, id_num, old_username, old_site))
