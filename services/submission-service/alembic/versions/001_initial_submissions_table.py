"""initial submissions table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'submissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('place_of_living', sa.String(), nullable=False),
        sa.Column('gender', sa.String(), nullable=False),
        sa.Column('country_of_origin', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('photo_path', sa.String(), nullable=False),
        sa.Column('classification_result', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )
    op.create_index(op.f('ix_submissions_id'), 'submissions', ['id'], unique=False)
    op.create_index(op.f('ix_submissions_user_id'), 'submissions', ['user_id'], unique=False)
    op.create_index(op.f('ix_submissions_age'), 'submissions', ['age'], unique=False)
    op.create_index(op.f('ix_submissions_gender'), 'submissions', ['gender'], unique=False)
    op.create_index(op.f('ix_submissions_place_of_living'), 'submissions', ['place_of_living'], unique=False)
    op.create_index(op.f('ix_submissions_country_of_origin'), 'submissions', ['country_of_origin'], unique=False)
    op.create_index(op.f('ix_submissions_created_at'), 'submissions', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_submissions_created_at'), table_name='submissions')
    op.drop_index(op.f('ix_submissions_country_of_origin'), table_name='submissions')
    op.drop_index(op.f('ix_submissions_place_of_living'), table_name='submissions')
    op.drop_index(op.f('ix_submissions_gender'), table_name='submissions')
    op.drop_index(op.f('ix_submissions_age'), table_name='submissions')
    op.drop_index(op.f('ix_submissions_user_id'), table_name='submissions')
    op.drop_index(op.f('ix_submissions_id'), table_name='submissions')
    op.drop_table('submissions')

