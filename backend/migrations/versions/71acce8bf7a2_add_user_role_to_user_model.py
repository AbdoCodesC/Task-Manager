"""add user role to user model

Revision ID: 71acce8bf7a2
Revises: 7df59ded7deb
Create Date: 2026-09-15 17:53:15.697413

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '71acce8bf7a2'
down_revision = '7df59ded7deb'
branch_labels = None
depends_on = None


def upgrade():
    user_role_enum = postgresql.ENUM(
        'user',
        'admin',
        name='user_role',
    )
    user_role_enum.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'role',
                user_role_enum,
                nullable=False,
                server_default='user',
            )
        )

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('role', server_default=None)


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('role')

    user_role_enum = postgresql.ENUM(
        'user',
        'admin',
        name='user_role',
    )
    user_role_enum.drop(op.get_bind(), checkfirst=True)
