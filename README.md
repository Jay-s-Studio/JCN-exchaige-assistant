# JCN ExchAIge Assistant

## Data migration instructions

The database is based on alembic

### Automatically create versions
alembic revision --autogenerate -m "initdb"
alembic revision --autogenerate -m "create_surround"

### Update to the latest version

alembic upgrade heads

### Update database

alembic upgrade 版本号

### Downgrade database

alembic downgrade -1  # 降一个版本
alembic downgrade 版本号(如:e54fe6ba468d)