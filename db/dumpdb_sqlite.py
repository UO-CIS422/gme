"""
Dump the database of evaluations into CSV
File name is "sqlite.db".

Run as "python3 dumbdb_sqlite.py >dump.csv"
M Young, April 2016 for CIS 422
"""

DBFILE = "sqlite.db"
from schema import DBSCHEMA_SQL
from schema import DBSCHEMA

import arrow  # Date-Time module, better than the built-in datetime
import sqlite3

def write_headers(schema):
    """Write the headers as first row of CSV"""
    for field in schema:
        print('"{}",'.format(field), end="")
    print()

def write_row(row):
    """Write database row as CSV"""
    for field in row:
        print('"{}",'.format(field), end="")
    print()




conn = sqlite3.connect(DBFILE)
c = conn.cursor()
# c.execute("CREATE TABLE evals (date text, member text, teammate text"
#           + ", dependable integer, dependable_comments text"
#           + ", constructive integer, constructive_comments text"
#           + ", engaged integer, engaged_comments text"
#           + ", productive integer, productive_comments text"
#           + ", asset integer, asset_comments text"
#           + ")")



c.execute("SELECT * FROM evals")
results = c.fetchmany()

write_headers(DBSCHEMA)
for row in results:
    write_row(row)


conn.close()

