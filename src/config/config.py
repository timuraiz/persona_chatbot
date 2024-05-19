import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, StrictStr

current_dir = os.path.dirname(os.path.abspath(__file__))

BOT_REPLIES = {
    'commands': {
        'start': 'Hello! This bot provides an opportunity to talk with any persona that you want!',
        'set_persona': 'Provide me description of persona that you want to talk with'
    }
}


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DATABASE_URL: StrictStr

    model_config = SettingsConfigDict(env_file=f'{current_dir}/.env',
                                      env_file_encoding='utf-8')


config = Settings()
