import aiohttp

from src.config.config import config


class GptAPI:
    _url = 'https://api.openai.com/v1/chat/completions'
    _headers = {
        'Authorization': f'Bearer {config.GPT_TOKEN.get_secret_value()}',
        'Content-Type': 'application/json'
    }
    _payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': None},
            # {'role': 'user', 'content': None}
        ]
    }

    async def _make_request(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self._url, headers=self._headers, json=self._payload, ssl=False) as response:
                assert response.status == 200
                data = await response.json()
                return data['choices'][0]['message']['content']

    def _set_payload(self, messages: list[str], name: str, persona: str):
        self._payload['messages'][0]['content'] = 'You are friend(not assistant) that chats with his friend. ' \
                                                  'You have name {}. You have following persona: {}'.format(name,
                                                                                                            persona)
        for idx, message in enumerate(messages):
            self._payload['messages'].append(
                {'role': 'user' if idx % 2 == 0 else 'system', 'content': message}
            )
        assert self._payload['messages'][-1]['role'] == 'user'

    async def ask(self, name: str, persona: str, messages: list) -> str:
        self._set_payload(messages, name, persona)
        return await self._make_request()


async def main():
    name = 'Historic'
    prompt = 'Can you explain the main causes of World War I?'
    persona = 'You are an assistant who is always polite and knowledgeable about global history.'
    response = await GptAPI().ask(persona, name, prompt)
    assert response is not None


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
