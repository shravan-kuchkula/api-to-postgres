class DBConnection:
    """
    A wrapper class used to represent database connection

    Attributes
    ----------
    conn : psycopg2.extensions.connection
        a postgres connection object
    cur : psycopg2.extensions.cursor
        a postgres cursor object

    Methods
    -------
    run()
        takes a list of queries represented as strings

    insert_row()
        inserts a row specified by the query and its values.

    fetch()
        returns the results of select statments

    close()
        close the database connection
    """

    def __init__(self,
                 conn,
                 cur):
        # map the params
        self.conn = conn
        self.cur = cur

    def run(self, queries):
        for query in queries:
            self.cur.execute(query)
            self.conn.commit()

    def insert_row(self, query, values):
        self.cur.execute(query, values)
        self.conn.commit()

    def fetch(self, queries):
        for query in queries:
            self.cur.execute(query)
            yield self.cur

    def close(self):
        self.conn.close()
