

class ServerConnection:

    def __init__(self):
        # TODO: Load settings
        pass
    
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
        # TODO: Disconnect cleanly
        pass