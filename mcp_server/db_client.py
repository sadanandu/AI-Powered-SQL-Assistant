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

def convert_oracle_types(value):
    if isinstance(value, oracledb.LOB):
        return value.read()  # Convert CLOB/BLOB to string or bytes
    return value

def run_query(sql: str):
    cursor = connection.cursor()
    # print(len(vector))
    # if vector is not None:
    #     print("Executing cursor")
    #     vector = array.array("f", vector)
    #     print("created vector", type(vector))
    #     cursor.execute(sql, [vector])
    #     print("Executed cursor")
    # else:
    cursor.execute(sql)
    cols = [col[0] for col in cursor.description]
    print("fetched columns", cols)
    rows = cursor.fetchall()
    print("Got rows", rows)
    result = rows
    # if 'distance' in cols:
    #     idx = cols.index('distance')
    # elif 'DISTANCE' in cols:
    #     idx = cols.index('DISTANCE')
    # else:
    #     idx = None
    # for row in rows:
    #     print(dict(zip(cols, row))) 
    #     if idx is not None:
    #         if row[idx] <= 0.5:
    #             result.append(row)
    #     else:
    #         result.append(row)
    cursor.close()
    result = [
        {
            col: convert_oracle_types(val)
            for col, val in zip(cols, row)
        }
        for row in result
    ]
    return result
