import os
from psycopg import connect
from psycopg.rows import dict_row

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://barfpani@localhost:5432/know_your_stuff"
)

def get_connection():
    return connect(DATABASE_URL, row_factory=dict_row)