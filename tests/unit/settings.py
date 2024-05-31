from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    # MinIO настройки
    minio_host: str = 'localhost:9000'
    minio_root_user: str = 'testuser'
    minio_root_password: str = 'testpassword'
    bucket_name: str = 'test-bucket'

    # PostgreSQL настройки
    db_user: str = 'testuser'
    db_password: str = 'testpassword'
    db_name: str = 'testdb'
    db_host: str = 'localhost'
    db_port: int = 5432

    service_url: str = 'http://127.0.0.1:8000'

    class Config:
        env_file = '.env.test'
        env_prefix = 'TEST_'

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


test_settings = TestSettings()
