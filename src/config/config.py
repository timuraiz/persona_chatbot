import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

current_dir = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr

    model_config = SettingsConfigDict(env_file=f'{current_dir}/.env',
                                      env_file_encoding='utf-8')


config = Settings()
