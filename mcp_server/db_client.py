import oracledb
import os

wallet_path = "/Users/sadanandupase/PycharmProjects/trial/23AI"
SERVICE_NAME = "m04vxfqnjt7h6fh0_high"
print(wallet_path)
connection = oracledb.connect(
    user="admin",
    password="Welcome_123#",
    dsn=SERVICE_NAME,  # match what's in tnsnames.ora
    config_dir=wallet_path,
    wallet_location=wallet_path
)

def run_query(sql: str):
    cursor = connection.cursor()
    cursor.execute(sql)
    cols = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    return [dict(zip(cols, row)) for row in rows]
