"""Add user_photo and profile_color fields to User model

Revision ID: a3b4c5d6e7f8
Revises: 29c2fde25c94
Create Date: 2026-04-26 10:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3b4c5d6e7f8'
down_revision = '29c2fde25c94'
branch_labels = None
depends_on = None


def upgrade():
    # Add user_photo column to users table
    op.add_column('users', sa.Column('user_photo', sa.String(length=255), nullable=True))

    # Add profile_color column to users table with default value
    op.add_column('users', sa.Column('profile_color', sa.String(length=7), nullable=True, server_default='#667eea'))


def downgrade():
    # Remove the columns in reverse order
    op.drop_column('users', 'profile_color')
    op.drop_column('users', 'user_photo')
