import oracledb
import os
from typing import Optional, List
import array

wallet_path = "/Users/sadanandupase/PycharmProjects/23AI"
SERVICE_NAME = "m04vxfqnjt7h6fh0_high"
print(wallet_path)
connection = oracledb.connect(
    user="admin",
    password="Welcome_123#",
    dsn=SERVICE_NAME,  # match what's in tnsnames.ora
    config_dir=wallet_path,
    wallet_location=wallet_path
)

def run_query(sql: str, vector: Optional[List[float]] = None):
    cursor = connection.cursor()
    print(len(vector))
    if vector is not None:
        print("Executing cursor")
        vector = array.array("f", vector)
        print("created vector", type(vector))
        cursor.execute(sql, [vector])
        print("Executed cursor")
    else:
        cursor.execute(sql)
    cols = [col[0] for col in cursor.description]
    print("fecthed columns", cols)
    rows = cursor.fetchall()
    print("Got rows", rows)
    for row in rows:
        print(dict(zip(cols, row)))
    cursor.close()
    return [dict(zip(cols, row)) for row in rows]
