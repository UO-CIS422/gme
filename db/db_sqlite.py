"""
The sqlite database module.
This is designed to be one of multiple
database implementations that can be
dynamically chosen when installing the
flask application.  Currently it's the only
choice, and it is likely to require some
revisions when we create another choice.

See design notes at bottom of file.
"""

import arrow
import sqlite3
from db.schema import DBSCHEMA

DBFILE = "db/sqlite.db"  # Relative to main program, not to this module

sqlite3.enable_callback_tracebacks(True)

def write_ratings(timestamp, ratings):
    """
    Insert a rant to the database, tagging it with an ISO-formatted
    timestamp.
    """
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    #FIXME:  We should produce this tuple from the DBSCHEMA constant
    argtuple = (timestamp, ratings["member"], ratings["teammate"], 
                ratings["dependable"], ratings["comments-dependable"],
                ratings["constructive"], ratings["comments-constructive"],
                ratings["engaged"], ratings["comments-engaged"],
                ratings["productive"], ratings["comments-productive"],
                ratings["asset"], ratings["comments-asset"])
            
    c.execute("INSERT INTO evals VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", argtuple)
    conn.commit()
    conn.close()

def deconstruct_row(row):
    """
    Apply DBSCHEMA constant to convert row tuple to
    dict with named items, ready for display on web form.
    """
    print("Deconstructing row: {}".format(row))
    values = { }
    for i in range(len(DBSCHEMA)):
        values[ DBSCHEMA[i] ] = row[i]
    return values

def read_ratings(member, timestamp):
    """
    Read ratings for this member (needs to be limited to session; this is insecure)
    """
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    args = ( member , timestamp)
    print("Querying database for '{}', '{}'".format(member,timestamp))
    c.execute("SELECT * FROM evals WHERE member = ? AND date = ?", args)
    result = c.fetchall()
    print("Query result {}".format(result))

    values = [ ] 
    for row in result: 
        values.append(deconstruct_row(row))
    conn.close()
    return values

def dump_db():
    """
    Print all the records in the database
    """
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute("SELECT * FROM evals")
    result = c.fetchall()
    for item in result:
        print(item)

    #  Warning: 'fetchmany()' may return just one row! 
    conn.close()
    return result






# Design notes:
#
# Note that SQLite Python module does not allow
# sharing connections between threads. Since we may
# well be in a multi-threaded environment (depending on
# how Flask and Gunicorn manage processes), we will make
# a separate connection for each operation.
#
# This is something that might change when we have multiple
# possible database implementations (e.g., Redis and MongoDB
# in addition to SQLite).  I haven't thought through how
# to gracefully accomodate different approaches to threading.
#

