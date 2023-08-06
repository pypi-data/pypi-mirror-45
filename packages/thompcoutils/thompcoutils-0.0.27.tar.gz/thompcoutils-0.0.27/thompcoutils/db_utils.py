import sqlobject
from thompcoutils.log_utils import get_logger


class DbUtils:
    def __init__(self, db_type, host, username, password, schema, port, sqlite_file=None):
        self.connection = None
        if db_type == "sqlite":
            if sqlite_file is None:
                raise RuntimeError("--sqlite requires --sqlite-dir")
            else:
                print("Using Sqlite database")
                self._connect_sqlite(sqlite_file)
        elif db_type == "postgres":
            self._connect_postgres(username, password, schema, host, port)
        elif db_type == "mysql":
            self._connect_mysql(username, password, schema, host, port)
        elif db_type == "odbc":
            raise RuntimeError("ODBC not implemented yet")
        else:
            raise RuntimeError("No database selected")

    def _connect_uri(self, uri):
        self.connection = sqlobject.sqlhub.processConnection = sqlobject.connectionForURI(uri)

    def _connect_sqlite(self, file_path):
        uri = "sqlite:" + file_path
        self._connect_uri(uri)

    def _connect_postgres(self, username, password, database, host, port):
        port_str = ""
        if port is not None:
            port_str = ":" + str(port)
        uri = "postgres://" + username + ":" + password + "@" + host + port_str + "/" + database
        self._connect_uri(uri)

    def _connect_mysql(self, username, password, database, host, port):
        port_str = ""
        if port is not None:
            port_str = ":" + str(port)
        uri = "mysql://" + username + ":" + password + "@" + host + port_str + "/" + database
        self._connect_uri(uri)

    def create_table(self, table):
        logger = get_logger()
        if not self.connection.tableExists(table.q.tableName):
            logger.debug("creating table {}".format(str(table)))
            table.createTable()

    def create_tables(self, tables):
        logger = get_logger()
        logger.debug("Creating tables...")
        for table in tables:
            self.create_table(table)

    @staticmethod
    def drop_tables(tables):
        logger = get_logger()
        logger.debug("Dropping tables...")
        for table in tables:
            logger.debug("dropping table {}".format(str(table)))
            table.dropTable(cascade=True, ifExists=True)
