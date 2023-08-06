from .struct import get_struct_init

class MrlDBCassandra:
    def __init__(self, cluster, db=None, structure=None, username=None, password=None):
        from cassandra.cqlengine import connection
        from cassandra.cluster import Cluster
        if isinstance(cluster, str):
            cluster=[cluster]
        if (user==None or password==None):
            self.cluster=Cluster(cluster)
        else:
            from cassandra.auth import PlainTextAuthProvider
            auth_provider = PlainTextAuthProvider(username=username, password=password)
            self.cluster=Cluster(cluster, auth_provider=auth_provider)
        if db!=None:
            self.db=self.cluster.connect(db)
            self.connection=self.db
        else:
            self.connection=self.cluster
        self.structure=structure
        self.cursor=self.db
        self._config={"system":"cassandra", "cluster": cluster,"database": name, "structure": f"{len(structure)} tables", "username": username, "password":password}
        return
    def insert(self, table, data):
        def frmt(d):
            return f"'{d}'" if isinstance(d, str) else str(d)
        return self.connection.execute(f"INSERT INTO {table} ({', '.join([frmt(x) for x in data.keys()])}) VALUES ({', '.join([frmt(x) for x in data.values()])})")
    def update(self, table, data, conds=None):
        def frmt(d):
            return f"'{d}'" if isinstance(d, str) else str(d)
        return self.connection.execute(f"UPDATE {table} SET {', '.join([key+'='+frmt(arg) for key, arg in data.items()])}{' WHERE '+conds if conds!=None else ''}")
    def select(self, table, columns, conds=None):
        if self.structure!=None:
            if columns=="*":columns=self.structure[table].keys()
            return [
            {_col:_var for _col, _var in zip(columns, record)}
            for record in
            self.connection.execute(f"SELECT {'*' if columns=='*' else ', '.join(columns)} FROM {table}{' WHERE '+conds if conds!=None else ''}")
            ]
        else:
            return self.connection.execute(f"SELECT {'*' if columns=='*' else ', '.join(columns)} FROM {table}{' WHERE '+conds if conds!=None else ''}")
    def _getinfos(self):
        return self._config
    def init(self):
        [self.connection.execute(command) for command in get_struct_init(self.structure)]
        return self
    def __str__(self):
        return f"<mrldb.MrlDBCassandra at {id(self)} - connection: {self._config['cluster']}>"
    def __repr__(self):
        return f"<mrldb.MrlDBCassandra at {id(self)} - connection: {self._config['cluster']}>"
