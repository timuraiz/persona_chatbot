import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, StrictStr

current_dir = os.path.dirname(os.path.abspath(__file__))

BOT_REPLIES = {
    'commands': {
        'start': 'Hello! This bot provides an opportunity to talk with any persona that you want!',
        'set_persona': {
            'load_name': 'Give name to new persona',
            'load_persona': 'Provide me description of persona that you want to talk with',
            'saved': 'Now you are able to talk with desired personality. '
                     'Use /list_personas to see all available personas'
        },
        'talk_with': {
            'found': 'Your persona is ready. Try it! If you want to stop, say "bye"',
            'not_found': 'You do not have such persona',
            'bye': 'Have a nice day. Bye!'
        }
    },
    'general': {
        'bot_is_not_allowed': 'This bot isn\'t allowed to you'
    }
}


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DATABASE_URL: StrictStr
    GPT_TOKEN: SecretStr

    model_config = SettingsConfigDict(env_file=f'{current_dir}/.env',
                                      env_file_encoding='utf-8')


config = Settings()
