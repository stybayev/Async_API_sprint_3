"""Create files table

Revision ID: <your_revision_id>
Revises:
Create Date: 2024-06-02 21:13:05.183146

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '<851a5e8dc27d>'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'files',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('path_in_storage', sa.String(length=255), nullable=False, unique=True),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('size', sa.Integer, nullable=False),
        sa.Column('file_type', sa.String(length=100), nullable=True),
        sa.Column('short_name', sa.String(length=24), nullable=False, unique=True),
        sa.Column('created', sa.DateTime, default=sa.func.current_timestamp()),
        schema='content'
    )
    op.create_index('idx_file_path', 'files', ['path_in_storage'], unique=True, schema='content')
    op.create_index('idx_file_short_name', 'files', ['short_name'], unique=True, schema='content')


def downgrade() -> None:
    op.drop_index('idx_file_path', table_name='files', schema='content')
    op.drop_index('idx_file_short_name', table_name='files', schema='content')
    op.drop_table('files', schema='content')
