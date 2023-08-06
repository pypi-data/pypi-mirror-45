import pyhive.exc
from pyhive import presto
import requests
from requests.auth import HTTPBasicAuth
import atexit
from doorda_sdk.util.decorators import timeout

requests.packages.urllib3.disable_warnings()


def connect(*args, **kwargs):
    return Connection(*args, **kwargs)


class Connection:
    def __init__(self, *args, **kwargs):

        self._args = args
        self._kwargs = kwargs

    def cursor(self):
        return Cursor(*self._args, **self._kwargs)

    def close(self):
        pass

    def commit(self):
        pass


class Cursor(presto.Cursor):

    """
    Expands on PyHive Library.
    Fixes keyboardinterrupt/process exits bug which doesn't cancel running task before exiting.

    """

    def __init__(self, username, password, host='host.doorda.com', port=443, protocol='https',
                 catalog='default', schema='default'):
        self.__host = host
        self.__port = port
        self._username = username
        self._catalog = catalog
        self._schema = schema
        self._password = password
        self._protocol = protocol
        self.__source = 'doorda-python-client-v1'
        self._credentials = {'auth': HTTPBasicAuth(self._username, self._password), }
        self.schema = []
        super(Cursor, self).__init__(host=self.__host,
                                     port=self.__port,
                                     protocol=self._protocol,
                                     catalog=self._catalog,
                                     schema=self._schema,
                                     username=self._username,
                                     requests_kwargs=self._credentials,
                                     source=self.__source)

        def exit_handler():

            """
            Safely cancel query on exit

            """
            try:
                self.cancel()
            except pyhive.exc.ProgrammingError as _:
                pass
        atexit.register(exit_handler)

    def execute(self, operation, parameters=None):
        """
        1) Cancel previous query if still running
        2) Execute query

        """
        if self._state == 1:
            self.cancel()
        super().execute(operation, parameters)

    def show_catalogs(self):
        """
        Returns a list of catalogs that user has access to.

        """
        self.execute("SHOW CATALOGS")
        return self.fetchall()

    def col_names(self):
        """
        Returns a list of column names IF a query has been executed

        """
        assert self.description, "Column names not available"
        if self.description:
            return [col[0] for col in self.description]

    def col_types(self):
        """
        Returns a list of column names mapped to column types IF a query has been executed

        """
        assert self.description, "Column types not available"
        if self.description:
            return {col[0]: col[1] for col in self.description}

    def table_stats(self, catalog, schema, table):
        """
        Returns number of rows in a table

        """
        if catalog and schema and table:
            fmt = "SHOW STATS FOR {catalog_name}.{schema_name}.{table_name}"
            self.execute(fmt.format(catalog_name=catalog, schema_name=schema, table_name=table))
            results = self.fetchall()
            return {"number_of_rows": results[-1][-3]}

    @timeout(20, "Cursor not connected")
    def is_connected(self):
        """
        Checks connection with DoordaHost.

        """
        fmt = "SELECT 1"
        self.execute(fmt)
        rows = self.fetchall()
        return rows[0][0] == 1
