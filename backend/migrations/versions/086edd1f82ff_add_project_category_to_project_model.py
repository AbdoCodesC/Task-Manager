"""add project category to project model

Revision ID: 086edd1f82ff
Revises: 8c1e4f2a6b90
Create Date: 2026-09-18 09:05:21.900967

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '086edd1f82ff'
down_revision = '8c1e4f2a6b90'
branch_labels = None
depends_on = None


def upgrade():
    project_category_enum = postgresql.ENUM(
        'health',
        'personal',
        'work',
        'learning',
        'career',
        'creative',
        'launch',
        'research',
        'team',
        'home',
        name='project_category',
    )
    project_category_enum.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'category',
                project_category_enum,
                nullable=False,
                server_default='personal',
            )
        )

    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.alter_column('category', server_default=None)


def downgrade():
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_column('category')

    project_category_enum = postgresql.ENUM(
        'health',
        'personal',
        'work',
        'learning',
        'career',
        'creative',
        'launch',
        'research',
        'team',
        'home',
        name='project_category',
    )
    project_category_enum.drop(op.get_bind(), checkfirst=True)
