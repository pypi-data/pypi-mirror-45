__doc__=f"""mrldb by Rémi "Mr e-RL" LANGDORPH
Copyright (c) 2019 Rémi LANGDORPH - mrerl@warlegend.net
under MIT License (https://github.com/merlleu/mrldb/blob/master/LICENSE)"""
__all__=["dbutils"]
class _dbutils:
    def __init__(self):
        pass
    def insert(self, table, data):
        # table= "mytable"
        # data= {"name": "tom", "age": 1}
        def frmt(d):
            return f"'{d}'" if isinstance(d, str) else str(d)
        return f"INSERT INTO {table} ({', '.join([frmt(x) for x in data.keys()])}) VALUES ({', '.join([frmt(x) for x in data.values()])})"
    def update(self, table, data, conds=None):
        # table= "mytable"
        # data= {"name": "tom", "age": 1}
        # conds= "(x=1) or (x=2 and y=3)"
        def frmt(d):
            return f"'{d}'" if isinstance(d, str) else str(d)
        return f"UPDATE {table} SET {', '.join([key+'='+frmt(arg) for key, arg in data.items()])}{' WHERE '+conds if conds!=None else ''}"
    def select(self, table, columns, conds=None):
        # table= "mytable"
        # columns= ["test", "x"]
        # conds= "(x=1) or (x=2 and y=3)"
        return f"SELECT {'*' if columns=='*' else ', '.join(columns)} FROM {table}{' WHERE '+conds if conds!=None else ''}"
dbutils=_dbutils()
