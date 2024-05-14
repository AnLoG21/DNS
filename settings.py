from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str('REAL_DATABASE_URL',
                            default='postgresql+asyncpg://postgres:Log680968amr@localhost:5432/postgres')