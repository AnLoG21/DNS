from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str('REAL_DATABASE_URL',
                            default='postgresql+asyncpg://postgres:Log680968amr@localhost:5432/postgres')

REAL_DATABASE_URL2 = env.str('REAL_DATABASE_URL2',
                            default='jdbc:sqlite:C:\\Users\\analo\\PycharmProjects\\PetProg\\gg')

TEST_DATABASE_URL = env.str('TEST_DATABASE_URL',
                            default='postgresql+asyncpg://postgres_test:Log680968amr_test@localhost:5433/postgres_test')