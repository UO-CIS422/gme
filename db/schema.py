"""
Scheme of database, for sharing between applicaton, forms, and
templates
"""
DBSCHEMA = ["date", "member", "teammate",
            "dependable", "dependable_comments",
            "constructive", "constructive_comments",
            "engaged", "engaged_comments",
            "productive", "productive_comments",
            "asset", "asset_comments" ]

DBSCHEMA_SQL = ", ".join( map(lambda item: item + " text", DBSCHEMA))

