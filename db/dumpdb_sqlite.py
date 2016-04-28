"""
Dump the database of evaluations into CSV
File name is "sqlite.db".

Run as "python3 dumbdb_sqlite.py >dump.csv"
M Young, April 2016 for CIS 422
"""

DBFILE = "sqlite.db"
CSVFILE = "db.csv"
from schema import DBSCHEMA_SQL
from schema import DBSCHEMA

import csv    # Write Excel-compatible file
import arrow  # Date-Time module, better than the built-in datetime
import sqlite3

csvfile = open(CSVFILE, 'w', newline='')
writer = csv.writer(csvfile,dialect='excel')

def write_row(row):
    """Write database row as CSV"""
    # for field in row:
    #     print('"{}",'.format(escapify(field)), end="")
    # print()
    writer.writerow(row)

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
results = c.fetchall()

write_row(DBSCHEMA)
for row in results:
    write_row(row)


conn.close()

