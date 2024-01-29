"""initdb

Revision ID: a903f02e95e3
Revises: 
Create Date: 2024-01-29 15:36:18.493100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a903f02e95e3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Primary Key'),
    sa.Column('symbol', sa.String(length=16), nullable=False, comment='Symbol'),
    sa.Column('type', sa.String(length=32), server_default=sa.text("'general'"), nullable=False, comment='Type'),
    sa.Column('path', sa.String(length=128), nullable=False, comment='Path(Up to two levels), e.g. currency.id/currency.id'),
    sa.Column('parent_id', postgresql.UUID(), nullable=True, comment='Parent ID'),
    sa.Column('created_by_id', postgresql.UUID(), nullable=True, comment='Create User ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Create Date'),
    sa.Column('created_by', sa.String(length=64), nullable=False, comment='Create User Name'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Update Date'),
    sa.Column('updated_by_id', postgresql.UUID(), nullable=True, comment='Update User ID'),
    sa.Column('updated_by', sa.String(length=32), nullable=False, comment='Update User Name'),
    sa.Column('delete_reason', sa.String(length=64), nullable=True, comment='Delete Reason'),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Is Deleted(Logical Delete)'),
    sa.Column('description', sa.Text(), nullable=True, comment='Description'),
    sa.Column('sequence', sa.Float(), server_default=sa.text('extract(epoch from now())'), nullable=True, comment='Display sort, small to large, positive sort, default value current timestamp'),
    sa.ForeignKeyConstraint(['parent_id'], ['public.currency.id'], name='currency_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('telegram_account',
    sa.Column('id', sa.BigInteger(), nullable=False, comment='Account ID'),
    sa.Column('username', sa.String(length=255), nullable=True, comment='Username'),
    sa.Column('first_name', sa.String(length=255), nullable=True, comment='First Name'),
    sa.Column('last_name', sa.String(length=255), nullable=True, comment='Last Name'),
    sa.Column('full_name', sa.String(length=255), nullable=True, comment='Full Name'),
    sa.Column('name', sa.String(length=255), nullable=True, comment='Name'),
    sa.Column('language_code', sa.String(length=255), nullable=True, comment='Language Code'),
    sa.Column('is_bot', sa.Boolean(), nullable=True, comment='Is Bot'),
    sa.Column('is_premium', sa.Boolean(), nullable=True, comment='Is Premium'),
    sa.Column('link', sa.String(length=255), nullable=True, comment='Link'),
    sa.Column('created_by_id', postgresql.UUID(), nullable=True, comment='Create User ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Create Date'),
    sa.Column('created_by', sa.String(length=64), nullable=False, comment='Create User Name'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Update Date'),
    sa.Column('updated_by_id', postgresql.UUID(), nullable=True, comment='Update User ID'),
    sa.Column('updated_by', sa.String(length=32), nullable=False, comment='Update User Name'),
    sa.Column('delete_reason', sa.String(length=64), nullable=True, comment='Delete Reason'),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Is Deleted(Logical Delete)'),
    sa.Column('description', sa.Text(), nullable=True, comment='Description'),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('telegram_chat_group',
    sa.Column('id', sa.BigInteger(), nullable=False, comment='Chat Group ID'),
    sa.Column('title', sa.String(length=255), nullable=True, comment='Title'),
    sa.Column('type', sa.String(length=255), nullable=True, comment='Type'),
    sa.Column('in_group', sa.Boolean(), nullable=True, comment='In Group'),
    sa.Column('bot_type', sa.String(length=255), nullable=True, comment='Bot Type'),
    sa.Column('created_by_id', postgresql.UUID(), nullable=True, comment='Create User ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Create Date'),
    sa.Column('created_by', sa.String(length=64), nullable=False, comment='Create User Name'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Update Date'),
    sa.Column('updated_by_id', postgresql.UUID(), nullable=True, comment='Update User ID'),
    sa.Column('updated_by', sa.String(length=32), nullable=False, comment='Update User Name'),
    sa.Column('delete_reason', sa.String(length=64), nullable=True, comment='Delete Reason'),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Is Deleted(Logical Delete)'),
    sa.Column('description', sa.Text(), nullable=True, comment='Description'),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Primary Key'),
    sa.Column('username', sa.String(length=255), nullable=True, comment='Username'),
    sa.Column('display_name', sa.String(length=255), nullable=True, comment='Display Name'),
    sa.Column('hash_password', sa.String(length=255), nullable=True, comment='Hash Password'),
    sa.Column('password_salt', sa.String(length=255), nullable=True, comment='Password Salt'),
    sa.Column('is_superuser', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Is Superuser'),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Is Active'),
    sa.Column('gac', sa.String(length=16), nullable=True, comment='Google verification code secret_key'),
    sa.Column('last_login_at', sa.DateTime(), nullable=True, comment='最登入时间'),
    sa.Column('created_by_id', postgresql.UUID(), nullable=True, comment='Create User ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Create Date'),
    sa.Column('created_by', sa.String(length=64), nullable=False, comment='Create User Name'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Update Date'),
    sa.Column('updated_by_id', postgresql.UUID(), nullable=True, comment='Update User ID'),
    sa.Column('updated_by', sa.String(length=32), nullable=False, comment='Update User Name'),
    sa.Column('delete_reason', sa.String(length=64), nullable=True, comment='Delete Reason'),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Is Deleted(Logical Delete)'),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('exchange_rate',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Primary Key'),
    sa.Column('telegram_chat_group_id', sa.BigInteger(), nullable=False, comment='Telegram Chat Group ID'),
    sa.Column('currency_id', postgresql.UUID(), nullable=False, comment='Currency ID'),
    sa.Column('buy_rate', sa.Float(), nullable=True, comment='Buy Rate'),
    sa.Column('sell_rate', sa.Float(), nullable=True, comment='Sell Rate'),
    sa.Column('created_by_id', postgresql.UUID(), nullable=True, comment='Create User ID'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Create Date'),
    sa.Column('created_by', sa.String(length=64), nullable=False, comment='Create User Name'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Update Date'),
    sa.Column('updated_by_id', postgresql.UUID(), nullable=True, comment='Update User ID'),
    sa.Column('updated_by', sa.String(length=32), nullable=False, comment='Update User Name'),
    sa.ForeignKeyConstraint(['currency_id'], ['public.currency.id'], name='exchange_rate_currency_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['telegram_chat_group_id'], ['public.telegram_chat_group.id'], name='exchange_rate_telegram_chat_group_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('telegram_account_group_relation',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Primary Key'),
    sa.Column('account_id', sa.BigInteger(), nullable=False, comment='Account ID'),
    sa.Column('chat_group_id', sa.BigInteger(), nullable=False, comment='Chat Group ID'),
    sa.ForeignKeyConstraint(['account_id'], ['public.telegram_account.id'], name='telegram_account_relation_account_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['chat_group_id'], ['public.telegram_chat_group.id'], name='telegram_account_relation_chat_group_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account_id', 'chat_group_id', name='unique_telegram_account_group_relation_uc'),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('telegram_account_group_relation', schema='public')
    op.drop_table('exchange_rate', schema='public')
    op.drop_table('user', schema='public')
    op.drop_table('telegram_chat_group', schema='public')
    op.drop_table('telegram_account', schema='public')
    op.drop_table('currency', schema='public')
    # ### end Alembic commands ###