def get_struct_init(structure):
    return [
    "CREATE TABLE IF NOT EXISTS "+table+"("+", ".join(
    [
    colname+" "+content for colname, content in cols.items()
    ])+")"
    for table, cols in structure.items()
    ]
