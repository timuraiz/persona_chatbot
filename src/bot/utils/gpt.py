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
            {'role': 'user', 'content': None}
        ]
    }

    async def _make_request(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self._url, headers=self._headers, json=self._payload, ssl=False) as response:
                print(response)
                assert response.status == 200
                data = await response.json()
                return data['choices'][0]['message']['content']

    def _set_payload(self, user_msg: str, persona: str):
        self._payload['messages'][0]['content'] = 'You are friend that chats with his friend.' \
                                                  ' You have following persona: {}'.format(persona)
        self._payload['messages'][1]['content'] = user_msg

    async def ask(self, persona: str, user_msg: str) -> str:
        self._set_payload(user_msg, persona)
        return await self._make_request()


async def main():
    prompt = 'Can you explain the main causes of World War I?'
    persona = 'You are an assistant who is always polite and knowledgeable about global history.'
    response = await GptAPI.ask(persona, prompt)
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
