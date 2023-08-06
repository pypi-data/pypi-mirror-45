
from .struct import get_struct_init

class MrlDBMsql:
    def __init__(self, host, database=None, structure=None, username=None, password=None):
        import mysql.connector as mariadb
        self.connection = mariadb.connect(host=host, database=database, username=username, password=password)
        self.cursor = mariadb_connection.cursor()
        self.structure=structure
        self._config={"system":"mysql", "host": host, "database": database, "structure": f"{len(structure)} tables", "username": username, "password":password}
        return
    def insert(self, table, data):
        def frmt(d):
            return f"'{d}'" if isinstance(d, str) else str(d)
        return self.cursor.execute(f"INSERT INTO {table} ({', '.join([frmt(x) for x in data.keys()])}) VALUES ({', '.join([frmt(x) for x in data.values()])})")
    def update(table, data, conds=None):
        def frmt(d):
            return f"'{d}'" if isinstance(d, str) else str(d)
        return self.cursor.execute(f"UPDATE {table} SET {', '.join([key+'='+frmt(arg) for key, arg in data.items()])}{' WHERE '+conds if conds!=None else ''}")
    def select(table, columns, conds=None):
        if self.structure!=None:
            if columns=="*":columns=self.structure[table].keys()
            return [
            {_col:_var for _col, _var in zip(columns, record)}
            for record in
            self.cursor.execute(f"SELECT {'*' if columns=='*' else ', '.join(columns)} FROM {table}{' WHERE '+conds if conds!=None else ''}")
            ]
        else:
            return self.cursor.execute(f"SELECT {'*' if columns=='*' else ', '.join(columns)} FROM {table}{' WHERE '+conds if conds!=None else ''}")
    def _getinfos(self):
        return self._config
    def init(self):
        [self.cursor.execute(command) for command in get_struct_init(self.structure)]
        return self
