from sqlalchemy import Table, Column, String, Integer
from sqlalchemy.sql.expression import column
from .db import metadata

# Create your schema here.

# Example:
# people = Table(
#     "people",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String),
#     Column("age", Integer),
# )