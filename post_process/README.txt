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

group_ratings.py:
	After clean_names has been iterated to get unique names,
	use group_ratings to produce a CSV file that cross-tabulates
	team member ratings of each other, with comments.

	Bugs:  Comments go into a single column (no way to span
	in CSV format), and if you manually merge and wrap cells,
	Excel auto-height will fail to adjust row height.  It appears
	to be necessary to manually merge, wrap, AND adjust row
	height.  It is not clear how to avoid this.

