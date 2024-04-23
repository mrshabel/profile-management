import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

metadata = sa.MetaData()

UsersTable = sa.Table(
    "users",
    metadata,
    sa.Column("id", UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True,
              index=True, nullable=False),
    sa.Column("username", sa.String(100), index=True, nullable=False),
    sa.Column("password", sa.String, nullable=False),
    sa.Column("first_name", sa.String(100), nullable=False),
    sa.Column("last_name", sa.String(100), nullable=False),
    sa.Column("is_active", sa.Boolean, server_default="true", nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True),
              server_default=func.now(), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True),
              server_onupdate=sa.text('NOW()'), nullable=False),
    sa.UniqueConstraint("username", name="users_username_unique_constraint")
)
