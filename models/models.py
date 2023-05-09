from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, ForeignKey


metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

album = Table(
    "album",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_user", Integer, ForeignKey(user.c.id)),
    Column("email", String, nullable=False),
    Column("uuid", String, nullable=False),
)

photo = Table(
    "photo",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_user", Integer, ForeignKey(user.c.id)),
    Column("id_album", Integer, ForeignKey(album.c.id)),
    Column("uuid", String, nullable=False),
    Column("url", String, nullable=False),
)
