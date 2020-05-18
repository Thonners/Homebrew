""" Collection of SQL statements for use with the database """

GET_SALT =  """SELECT password_salt, password_hash
                FROM brewers
                WHERE email = ?
            """

UPDATE_PASSWORD =   """UPDATE brewers SET (password_hash = ?, password_salt = ?) 
                        WHERE (email = ?);
                    """

CREATE_NEW_USER =   """
    INSERT INTO brewers (first_name, last_name, email, password_hash, password_salt) 
    VALUES (?, ?, ?, ?, ?)
"""

CREATE_NEW_BREW =   """
    INSERT INTO brews (brewer_id, brew_key, name, `description`) 
    SELECT brewers.brewer_id, ?, ?, ?
    FROM brewers 
    WHERE brewers.email = ?;
"""