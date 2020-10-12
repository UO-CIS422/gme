#! /bin/bash
#
# Backup old database if present.
# Create new database if not present
# Requires virtual environment in current directory
#
source env/bin/activate
if  test -f db/sqlite.db ; then
  echo "Backing up prior database"
  mv db/sqlite.db db/bak_${$}.db;
else
  echo "No prior database to back up"
fi
python3 db/initdb_sqlite.py

