Post processing survey results.

A CSV file is produced in the sibling "db" directory by the
dumpdb_sqlite.py program (which runs in the same
virtual environment as the server).  Copy it here for
post-processing.  

Here we use our own virtual environment, because we are
not concerned with database access but we are concerned with
processing csv and excel files.  

For now, we deal with multiple CSV files rather than an XSLX file
with multiple sheets. 

clean_names.py:
    We need to normalize (uniquify) student names so that
    we can match them.  We iteratively build a "names" sheet
    that maps names as entered to normalized names.

    On each pass:
       If a name appears in the "as entered" column, with a
       substitution on the "substitute" column, we make the
       substitution.

       If the substitution is "delete", we delete the row.

       Otherwise, we create a new entry in names sheet
       mapping the name to itself.   The user can then alter
       that entry and run again.

