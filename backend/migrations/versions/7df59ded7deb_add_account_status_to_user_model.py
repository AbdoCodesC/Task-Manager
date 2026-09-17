"""add account_status to user model

Revision ID: 7df59ded7deb
Revises: b2845ca8b88c
Create Date: 2026-09-15 09:35:27.866935

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7df59ded7deb"
down_revision = "b2845ca8b88c"
branch_labels = None
depends_on = None


def upgrade():
    account_status_enum = postgresql.ENUM(
        "active",
        "suspended",
        "deleted",
        name="account_status",
    )
    account_status_enum.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "email_verified",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )
        batch_op.add_column(
            sa.Column(
                "account_status",
                account_status_enum,
                nullable=False,
                server_default="active",
            )
        )
        batch_op.add_column(
            sa.Column(
                "deleted_at",
                sa.DateTime(timezone=True),
                nullable=True,
            )
        )

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column("email_verified", server_default=None)
        batch_op.alter_column("account_status", server_default=None)


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("deleted_at")
        batch_op.drop_column("account_status")
        batch_op.drop_column("email_verified")

    account_status_enum = postgresql.ENUM(
        "active",
        "suspended",
        "deleted",
        name="account_status",
    )
    account_status_enum.drop(op.get_bind(), checkfirst=True)

    # ### end Alembic commands ###
