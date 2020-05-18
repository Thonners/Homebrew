""" Module to handle all authentication related activities """
import os
import hashlib
import string
import random

SALT_SIZE_IN_BYTES = 32
BREW_KEY_LENGTH = 15

def get_new_user_credentials(password_plain_text):
    """ Creates a salt and hashes the given password for storage in the DB """
    salt = os.urandom(SALT_SIZE_IN_BYTES)
    key = _get_password_hash(salt, password_plain_text)
    return salt, key

def get_new_brew_key():
    return ''.join(random.choice(string.ascii_letters) for i in range(BREW_KEY_LENGTH))

def authenticate_user(salt, password, stored_hash):
    """ Returns True if the stored hash matches that of the given password and salt """
    given_password_hash = _get_password_hash(salt, password)
    return given_password_hash == stored_hash
    
def _get_password_hash(salt, password):
    key = hashlib.pbkdf2_hmac(
        'sha512', # The hash digest algorithm for HMAC
        password.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )
    return key