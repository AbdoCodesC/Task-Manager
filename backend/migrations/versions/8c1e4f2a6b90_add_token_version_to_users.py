"""add token version to users

Revision ID: 8c1e4f2a6b90
Revises: 71acce8bf7a2
Create Date: 2026-09-15

"""
from alembic import op
import sqlalchemy as sa


revision = "8c1e4f2a6b90"
down_revision = "71acce8bf7a2"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "token_version",
                sa.Integer(),
                nullable=False,
                server_default="0",
            )
        )

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column("token_version", server_default=None)


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("token_version")
