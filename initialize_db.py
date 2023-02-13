import pyodbc
from credentials.credentials import db_connection_str


def sql_query_w_commit(sql_statement):
    with pyodbc.connect(db_connection_str) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_statement)
            cursor.commit()


def create_sql_str_drop_table(table_name):
    sql_str_drop_table = f"DROP TABLE IF EXISTS {table_name}"
    return sql_str_drop_table


sql_str_create_processed_data = """
    IF OBJECT_ID(N'processed_data', N'U') IS NULL
    BEGIN
    CREATE TABLE dbo.processed_data
        (
        id INT IDENTITY PRIMARY KEY,
        filename NVARCHAR(128) NOT NULL,
        pixel_count INT NOT NULL,
        )
    END;
    """

sql_query_w_commit(create_sql_str_drop_table("processed_data"))
sql_query_w_commit(sql_str_create_processed_data)
