import re


class Parse:
    """
    Regex based parser for SQL `SELECT * FROM TABLE_NAME LIMIT n`/ `SELECT * FROM TABLE_NAME WHERE col = x` type queries

    """

    def __init__(self, query):
        self.query_template = re.compile("(?i)(select)\s+(.*?)\s*(from)\s+(.*?)\s*((where)\s(.*?)\s*|(limit)\s(.*?)\s*)?;")
        self.result = None
        self.query = query if query.endswith(";") else query + ";"

    def _validate(self):
        if not self.query.startswith("SELECT"):
            return False
        self.result = self.query_template.search(self.query)
        if self.result.group(1) and self.result.group(2) and self.result.group(3) and self.result.group(4):
            return True
        return False

    def get_table(self):
        if self.query and not self.query.startswith("SELECT"):
            raise Exception("Query parser currently only compatible with SELECT queries")
        if not self.result:
            results = self._validate()
            if not results:
                raise Exception("Syntax not detected")
        return self.result.group(4)

    def get_row_limit(self):
        if self.query and not self.query.startswith("SELECT"):
            raise Exception("Query parser currently only compatible with SELECT queries")
        if not self.result:
            results = self._validate()
            if not results:
                raise Exception("Syntax not detected")
        return self.result.group(9)

    def get_filter(self):
        if self.query and not self.query.startswith("SELECT"):
            raise Exception("Query parser currently only compatible with SELECT queries")
        if not self.result:
            results = self._validate()
            if not results:
                raise Exception("Syntax not detected")
        return self.result.group(7)
