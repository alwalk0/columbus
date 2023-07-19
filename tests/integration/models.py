import sqlalchemy


metadata = sqlalchemy.MetaData()


dogs = sqlalchemy.Table(
    "dogs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("breed", sqlalchemy.String),
    sqlalchemy.Column("age", sqlalchemy.Integer),
)

# tokens = sqlalchemy.Table(
#     "tokens",
#     metadata,
#     salalchemy.Column("token")
# )