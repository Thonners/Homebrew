""" Main code to run the server """

import os
import json
import sys
import socket
import socketserver

class BrewServerConnectionHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print(f"{self.client_address[0]} wrote:")
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


class BrewServer():
    """ This is the server class that will be called to run. It will pass handling of connections to the BrewServerConnectionHandler class.

    It's designed to be used as a resource (i.e. 'with BrewServer as server:...'), so has __enter__ and __exit__ functions accordingly
    """

    settings_file = "./data/config.json"

    def __init__(self):
        """ Create the server & load the settings """
        self.settings = self.get_settings()
        self.host = "0.0.0.0"
        self.port = self.settings['port']
        # Use this to determine when to close the server
        self.running = True


    def get_settings(self):
        """ Parse the config.json file """
        # TODO: try-except as appropriate to deal with 'port' not existing as a field or it not being a parsable int. (or decide where to do the try/except)
        settings={}
        self.settings_file = os.path.join(os.path.dirname(__file__),os.pardir,'data','config.json')
        with open(self.settings_file,"r") as settings_json:
            settings_raw = json.load(settings_json)
            # Convert the port to an int
            settings['port'] = int(settings_raw['port'])
        return settings

    def __enter__(self):
        """ Start listening for connections """
        # Create the server, binding to host/port set in the settings
        print(f"Starting server on host: {self.host}, listening on port: {self.port}...")
        self.server = socketserver.TCPServer((self.host, self.port), BrewServerConnectionHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        self.server.serve_forever()

    def __exit__(self, exc_type, exc_value, traceback):
        """ Called when the 'with' statement ends, so clean up the connection """
        self.server.shutdown()


