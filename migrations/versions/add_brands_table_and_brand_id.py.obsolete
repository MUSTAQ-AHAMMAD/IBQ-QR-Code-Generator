"""Add brands table and brand_id to qr_codes, company_logo to users

Revision ID: b5c6d7e8f9g0
Revises: a3b4c5d6e7f8
Create Date: 2026-05-13 10:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5c6d7e8f9g0'
down_revision = 'a3b4c5d6e7f8'
branch_labels = None
depends_on = None


def upgrade():
    # Create brands table
    op.create_table('brands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('website', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('logo', sa.String(length=255), nullable=True),
    sa.Column('primary_color', sa.String(length=7), nullable=True),
    sa.Column('secondary_color', sa.String(length=7), nullable=True),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('brands', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_brands_user_id'), ['user_id'], unique=False)

    # Add brand_id column to qr_codes table
    with op.batch_alter_table('qr_codes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('brand_id', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_qr_codes_brand_id'), ['brand_id'], unique=False)
        batch_op.create_foreign_key('fk_qr_codes_brand_id', 'brands', ['brand_id'], ['id'])

    # Add company_logo column to users table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company_logo', sa.String(length=255), nullable=True))


def downgrade():
    # Remove company_logo from users
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('company_logo')

    # Remove brand_id from qr_codes
    with op.batch_alter_table('qr_codes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_qr_codes_brand_id', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_qr_codes_brand_id'))
        batch_op.drop_column('brand_id')

    # Drop brands table
    with op.batch_alter_table('brands', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_brands_user_id'))
    op.drop_table('brands')
