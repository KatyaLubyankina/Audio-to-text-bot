import pycouchdb

import src.config as config

username = config.get_settings().couchdb_username
password = config.get_settings().couchdb_password.get_secret_value()
server = config.get_settings().couchdb_server
couchdb_url = f"http://{username}:{password}@{server}/"
database_name = config.get_settings().couchdb_database_name


class CouchManager(object):
    """Singleton for operations with couchdb."""

    _instance = None

    @staticmethod
    def get_instance() -> pycouchdb.client.Database:
        """Get connection to database.

        Returns:
            database: pycouchdb.client.Database.
        """
        if CouchManager._instance is None:
            server = CouchManager.create_server(couchdb_url)
            db = CouchManager.create_database(database_name, server)
            CouchManager._instance = db
        return CouchManager._instance

    def create_server(couchdb_url: str) -> pycouchdb.client.Server:
        """Create couchdb database instance.

        Args:
            couchdb_url (str): url for connection with
            username, password, host and port.

        Returns:
            pycouchdb.client.Server: connection to couchdb server.
        """
        return pycouchdb.Server(couchdb_url)

    def create_database(
        database_name: str, server: pycouchdb.Server
    ) -> pycouchdb.client.Database:
        """Create database with database_name.

        Args:
            database_name (str): database name
            server (pycouchdb.Server): connection to couchdb server.

        Returns:
            pycouchdb.client.Database: database instance.
        """
        if database_name in server:
            db = server.database(database_name)
        else:
            db = server.create(database_name)
        return db

    def add_document(path_to_doc: str) -> str:
        """Add document to couchdb.

        Args:
            path_to_doc (str): path to document.

        Returns:
            Id(type=str) for added document.
        """
        with open(path_to_doc, "r") as file:
            text = file.read()
            doc_to_couchdb = {"transcript": text}
            db = CouchManager.get_instance()
            id = db.save(doc_to_couchdb)["_id"]
        return id

    def get_document(doc_id: int) -> dict:
        """Get document from couchdb.

        Args:
            doc_id (int): it of document.

        Returns:
            dict: {"id": str, "transcript": str, "_rev": str}.
        """
        db = CouchManager.get_instance()
        return db.get(doc_id)
