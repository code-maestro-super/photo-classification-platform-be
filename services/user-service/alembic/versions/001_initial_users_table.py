"""initial users table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    # Create enum only if it doesn't exist (idempotent for restarts)
    op.execute("""
    DO $$ BEGIN
        CREATE TYPE userrole AS ENUM ('user', 'admin');
    EXCEPTION
        WHEN duplicate_object THEN NULL;
    END $$;
    """)
    # Skip table creation if users table already exists (e.g. after stamp head)
    has_users = conn.execute(sa.text(
        "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='users'"
    )).scalar()
    if has_users:
        return
    userrole_enum = postgresql.ENUM('user', 'admin', name='userrole', create_type=False)
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('role', userrole_enum, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.execute('DROP TYPE userrole')

