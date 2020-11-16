"""
Initialize an SQLite database
in the db directory.
File name is "sqlite.db".

Designed to be invoked from one level up, i.e.,
run 'python3 db/initdb-sqlite.db' from the
main Flask directory.

M Young, April 2016 for CIS 422
"""

DBFILE = "db/sqlite.db"
from schema import DBSCHEMA_SQL

import arrow  # Date-Time module, better than the built-in datetime

import sqlite3
conn = sqlite3.connect(DBFILE)
c = conn.cursor()
# c.execute("CREATE TABLE evals (date text, member text, teammate text"
#           + ", dependable integer, dependable_comments text"
#           + ", constructive integer, constructive_comments text"
#           + ", engaged integer, engaged_comments text"
#           + ", productive integer, productive_comments text"
#           + ", asset integer, asset_comments text"
#           + ")")
c.execute("CREATE TABLE evals (" + DBSCHEMA_SQL + ")")
nowstring = arrow.now().isoformat()
argtuple = (nowstring, "http://fake.fake",
            "sample-rater", "sample-teammate",
            0, "not dependable",
            1, "slightly constructive",
            2, "kinda engaged",
            3, "pretty productive",
            4, "quite an asset")
            
c.execute("INSERT INTO evals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", argtuple)
conn.commit()

c.execute("SELECT * FROM evals")
print(c.fetchone())

c.execute("DELETE FROM evals WHERE date > ''")
c.execute("SELECT * FROM evals")
print("Printing what's left in database")
print(c.fetchmany())

conn.close()

