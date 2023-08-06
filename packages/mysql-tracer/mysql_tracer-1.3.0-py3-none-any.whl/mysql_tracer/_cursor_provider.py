import logging
from getpass import getpass

import keyring
from alone import MetaSingleton
from mysql import connector

from mysql_tracer import chest

log = logging.getLogger('mysql_tracer.CursorProvider')


class CursorProvider(metaclass=MetaSingleton):

    def __init__(self):
        assert chest.host is not None, "You forgot to provide host, check module mysql_tracer.chest"
        assert chest.user is not None, "You forgot to provide user, check module mysql_tracer.chest"

        service = 'CursorProvider-{host}'.format(host=chest.host, db=chest.database)
        keyring_password = keyring.get_password(service, chest.user)
        if keyring_password is None or chest.ask_password:
            password = getpass("Password for {user}@{host}: ".format(user=chest.user, host=chest.host))
        else:
            log.debug('Retrieving password from keyring')
            password = keyring_password

        port = chest.port if chest.port is not None else 3306

        log.debug('Trying to connect to the database {}@{}:{}/{}'.format(chest.user, chest.host, port, chest.database))
        self.connection = connector.connect(
            host=chest.host,
            port=port,
            user=chest.user,
            db=chest.database,
            passwd=password)
        log.debug('Connection successful')

        if password is not keyring_password and chest.store_password:
            keyring.set_password(service, chest.user, password)

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()

    @staticmethod
    def cursor():
        return CursorProvider().connection.cursor()
