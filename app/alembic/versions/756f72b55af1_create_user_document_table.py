"""Create user_document table

Revision ID: 756f72b55af1
Revises: 774c58b35136
Create Date: 2021-04-29 14:23:18.176615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '756f72b55af1'
down_revision = '774c58b35136'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('hashed_password', sa.String(100)),
        sa.Column('is_active', sa.Boolean(100)),
    )

    op.create_table(
        'documents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(50), nullable=False),
        sa.Column('owner_id', sa.Integer),

    )


def downgrade():
    pass
