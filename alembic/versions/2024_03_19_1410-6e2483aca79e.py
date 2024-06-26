"""Implement telegram group type and message related table

Revision ID: 6e2483aca79e
Revises: 0eff7b099d95
Create Date: 2024-03-19 14:10:45.153466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6e2483aca79e'
down_revision: Union[str, None] = '0eff7b099d95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Primary Key'),
    sa.Column('content', sa.Text(), nullable=True, comment='Content'),
    sa.Column('type', sa.String(length=16), nullable=True, comment='Type'),
    sa.Column('created_by_id', postgresql.UUID(), nullable=True, comment='Create User ID'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Create Date'),
    sa.Column('created_by', sa.String(length=64), nullable=False, comment='Create User Name'),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Update Date'),
    sa.Column('updated_by_id', postgresql.UUID(), nullable=True, comment='Update User ID'),
    sa.Column('updated_by', sa.String(length=32), nullable=False, comment='Update User Name'),
    sa.Column('delete_reason', sa.String(length=64), nullable=True, comment='Delete Reason'),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Is Deleted(Logical Delete)'),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('message_history',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Primary Key'),
    sa.Column('message_id', postgresql.UUID(), nullable=False, comment='Message ID'),
    sa.Column('chat_group_id', sa.BigInteger(), nullable=False, comment='Chat Group ID'),
    sa.Column('status', sa.String(length=16), nullable=True, comment='Status'),
    sa.Column('telegram_message_id', sa.BigInteger(), nullable=True, comment='Telegram Message ID'),
    sa.Column('telegram_error_code', sa.BigInteger(), nullable=True, comment='Telegram Error Code'),
    sa.Column('telegram_error_description', sa.Text(), nullable=True, comment='Telegram Error Description'),
    sa.Column('created_by_id', postgresql.UUID(), nullable=True, comment='Create User ID'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Create Date'),
    sa.Column('created_by', sa.String(length=64), nullable=False, comment='Create User Name'),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Update Date'),
    sa.Column('updated_by_id', postgresql.UUID(), nullable=True, comment='Update User ID'),
    sa.Column('updated_by', sa.String(length=32), nullable=False, comment='Update User Name'),
    sa.Column('delete_reason', sa.String(length=64), nullable=True, comment='Delete Reason'),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Is Deleted(Logical Delete)'),
    sa.ForeignKeyConstraint(['chat_group_id'], ['public.telegram_chat_group.id'], name='message_history_relation_chat_group_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['message_id'], ['public.message.id'], name='message_history_relation_message_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('message_id', 'chat_group_id', name='unique_message_history_key'),
    schema='public'
    )
    op.create_table('telegram_chat_group_type',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Primary Key'),
    sa.Column('name', sa.String(length=16), nullable=True, comment='Name'),
    sa.Column('created_by_id', postgresql.UUID(), nullable=True, comment='Create User ID'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Create Date'),
    sa.Column('created_by', sa.String(length=64), nullable=False, comment='Create User Name'),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Update Date'),
    sa.Column('updated_by_id', postgresql.UUID(), nullable=True, comment='Update User ID'),
    sa.Column('updated_by', sa.String(length=32), nullable=False, comment='Update User Name'),
    sa.Column('delete_reason', sa.String(length=64), nullable=True, comment='Delete Reason'),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Is Deleted(Logical Delete)'),
    sa.Column('remark', sa.String(length=256), nullable=True, comment='Remark'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='unique_telegram_chat_group_type_name_key'),
    schema='public'
    )
    op.create_table('telegram_chat_group_type_relation',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Primary Key'),
    sa.Column('chat_group_id', sa.BigInteger(), nullable=False, comment='Chat Group ID'),
    sa.Column('chat_group_type_id', postgresql.UUID(), nullable=False, comment='Chat Group Type ID'),
    sa.ForeignKeyConstraint(['chat_group_id'], ['public.telegram_chat_group.id'], name='telegram_chat_group_relation_chat_group_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['chat_group_type_id'], ['public.telegram_chat_group_type.id'], name='telegram_chat_group_relation_chat_group_type_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('chat_group_id', 'chat_group_type_id', name='unique_telegram_chat_group_type_relation_key'),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('telegram_chat_group_type_relation', schema='public')
    op.drop_table('message_history', schema='public')
    op.drop_table('telegram_chat_group_type', schema='public')
    op.drop_table('message', schema='public')
    # ### end Alembic commands ###
