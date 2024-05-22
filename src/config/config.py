import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, StrictStr, Field

current_dir = os.path.dirname(os.path.abspath(__file__))

BOT_REPLIES = {
    'commands': {
        'start': 'Hello! 👋 This bot lets you chat with any persona you like! Just tell me who you want to talk to.',
        'set_persona': {
            'load_name': 'What name would you like to give your new persona? 🤔',
            'load_persona': 'Tell me a bit about the persona you want to create. What are they like?',
            'saved': 'All set! 🎉 You can now chat with your chosen persona. Use /list_personas to view all available personas.'
        },
        'talk_with': {
            'not_provided_name': 'Please provide the name of the persona you want to create. 📝',
            'found': 'Your persona is ready to chat! 🗣️ Try it out! If you want to stop, just say "bye".',
            'not_found': 'Oops, it looks like you don’t have that persona. 😢',
            'bye': 'Have a nice day! Goodbye! 👋'
        },
        'help': 'Need some guidance? 🤔 Here’s what you can do: \n'
                '- /start: Kick things off and learn more about how this bot works! 🚀\n'
                '- /set_persona: Create a new persona with a name and personality! 🎭\n'
                '- /talk_with <name_of_persona>: Start a conversation with your chosen persona! 🗣️\n'
                '- /list_personas: Check out all the personas you’ve created! 📜',
        'list_personas': {
            'no_personas': 'You currently have no personas created. 😕 Use /set_persona to create one! 🌟',
            'header': 'Here are all the personas you can talk to: 📜',
            'footer': 'You can start chatting with any of these personas using /talk_with <name_of_persona>. 🗣️'
        }
    },
    'general': {
        'bot_is_not_allowed': 'Sorry, it looks like this bot isn’t allowed for you. 🚫'
    }
}


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DATABASE_URL: StrictStr
    GPT_TOKEN: SecretStr

    # class Config:
    #     # Assuming 'current_dir' is defined; otherwise, you might use os.getcwd() or similar
    #     env_file = os.path.join(current_dir, '.env')
    #     env_file_encoding = 'utf-8'
    #     # Use environment variables if .env file does not exist
    #     env_file_encoding = 'utf-8'
    #     if not os.path.isfile(env_file):
    #         env_file = None  # This disables loading from a non-existent .env file


# Usage
config = Settings()